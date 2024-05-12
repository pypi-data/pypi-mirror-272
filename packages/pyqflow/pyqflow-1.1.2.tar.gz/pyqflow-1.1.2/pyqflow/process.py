# external imports
import abc
import heapq
import time
from functools import partial, reduce
from typing import Any, Callable, List, Tuple, Union

from pyqflow.actor import QActor, QControl
import logging
import asyncio

# internal imports
from pyqflow.asynchronous import Queue, async_wrap, create_task, gather
from pyqflow.constants import (
    BRANCH,
    BULLET,
    CAT,
    CTRL,
    DEFAULT_BATCH,
    DEFAULT_INFLIGHT_BATCH,
    MAX_BUFFER_SIZE,
    OF,
    SEP,
    Key,
    State,
    Value,
)
from pyqflow.remote import HttpSession, request_broadcast, trace_config


class QProcess:
    """Link of the workflow pipeline.

    This entity represents a link in the workflow DAG.
    It transforms data from an input actor and produces to an output actor.
    """

    def __init__(self, name: str):
        """Creates an workflow process.

        Args:
            name (str): Identifier for this process.
        """
        self.name = name

    def __call__(self, node: QActor) -> QActor:
        """Applies the process to a input actor stream.

        Args:
            node (QActor): Input actor stream.

        Returns:
            outputnode (QActor): Output actor stream.
        """

        outnode = QBridge(
            # f"{node}{SEP}{self.name}{SEP}",
            self.name,
            process=self,
        )

        outnode.add_parent(node)
        node.add_child(outnode)

        return outnode

    def __or__(self, other):
        if isinstance(other, QProcess):
            return QProcessUnion(self, other)
        else:
            raise TypeError(
                f"unsupported operand type(s) for |: '{self.__class__.__name__}' and '{other.__class__.__name__}'"
            )

    @abc.abstractmethod
    async def execute(self, **kwargs):
        """Implements this process async execution function."""
        raise NotImplementedError()


class QProcessUnion(QProcess):
    def __init__(self, process1, process2):
        super().__init__(name="union")
        self.process1 = process1
        self.process2 = process2

    def __call__(self, *node: List[QActor]):
        return self.process2(self.process1(*node))


class QBridge(QActor):
    """Actor stream that is the result of applying a process."""

    def __init__(self, name: str, process: QProcess, buffer_size: int = DEFAULT_BATCH):
        """creates a bridge actor stream.

        Args:
            name (str): Identifier for this actor stream.
            process (QProcess): Process that transforms the input actor stream and produces data into this actor stream.
        """
        super().__init__(name, source=False, buffer_size=buffer_size)

        self.op = process

    def execution_context(self) -> Tuple[QProcess, List[QActor]]:
        """Returns the execution context of this actor stream. The execution context is a tuple containing the process and the list of input actor streams.

        Returns:
            Tuple[QProcess,List[QActor]]: _description_
        """
        return self.op, self.parents


class QControlBridge(QControl):
    """Actor stream that is the result of applying a process."""

    def __init__(self, name: str, process: QProcess):
        """creates a bridge actor stream.

        Args:
            name (str): Identifier for this actor stream.
            process (QProcess): Process that transforms the input actor stream and produces data into this actor stream.
        """
        super().__init__(name, source=False)

        self.op = process

    def execution_context(self) -> Tuple[QProcess, List[QActor]]:
        """Returns the execution context of this actor stream. The execution context is a tuple containing the process and the list of input actor streams.

        Returns:
            Tuple[QProcess,List[QActor]]: _description_
        """
        return self.op, self.parents


class QControlProcess(QProcess):
    """Control process.

    This process is used to control the workflow and gather metadata.
    """

    def __init__(self, name: str):
        """Creates a control process.

        Args:
            name (str): Identifier for this process.
        """
        super().__init__(name)

    def __call__(self, node: QActor) -> QActor:
        """Applies the process to a input actor stream.

        Args:
            node (QActor): Input actor stream.

        Returns:
            outputnode (QActor): Output actor stream.
        """

        outnode = QControlBridge(
            # f"{node}{SEP}{self.name}{SEP}",
            self.name,
            process=self,
        )

        outnode.add_parent(node)

        node.add_child(outnode)
        node.add_child(outnode.control, limitless=True)

        return outnode

    async def execute(self, input: QActor, output: QControlBridge) -> bool:
        """Executes the mapping process.

        Args:
            input (QActor): Input actor stream to consume.
            output (QActor): Output actor stream to produce.

        Returns:
            bool : True if sucefull.
        """

        return await self.control_execute(
            input=input, output=output, control=output.control
        )

    async def control_execute(
        self, input: QActor, output: QActor, control: QActor
    ) -> bool:
        """Executes the controlled execute function.

        Args:
            input (QActor): Input actor stream to consume.
            output (QActor): Output actor stream to produce.
            control (QActor): Control actor stream to produce.

        Returns:
            bool : True if sucefull.
        """
        raise NotImplementedError()


class QJunction(QProcess):
    """Fork of the workflow pipeline."""

    def __init__(self, name: str):
        """Creates a fork of the workflow pipeline.

        Args:
            name (str): Identifier for this fork.
        """

        super().__init__(name)

    def __call__(self, *nodes: List[QActor]) -> QActor:
        """_summary_

        Args:
            nodes (List[QActor]): _description_

        Returns:
            _type_: _description_
        """

        outnode = QBridge(
            # f"{nodes}{SEP}{self.name}{SEP}",
            self.name,
            process=self,
            buffer_size=MAX_BUFFER_SIZE,
        )

        jointq = Queue()

        for i, node in enumerate(nodes):
            outnode.add_parent(node)
            node.add_child(outnode, queue=jointq, qindex=i)

        return outnode


class QMap(QProcess):
    """This process applies a particular async function to each element of the input stream."""

    def __init__(
        self,
        func: Callable[[Value], Value],
        many: bool = True,
        name: Union[None, str] = None,
    ):
        """Creates a map process.

        Args:
            func (function): async function to apply.
            many (bool): If true does a flatMap. Defaults to True.
        """

        if name is None:
            name = f"Map:{func}:"

        super().__init__(name)
        self.func = func
        if many:
            self.func_applier = func_applier_many
        else:
            self.func_applier = func_applier

        def wraped_applied(*args, **kwargs):
            try:
                return self.func_applier(*args, **kwargs)
            except:
                logging.exception("Unexecpeted error coccured!!!")

        self.wraped_applier = wraped_applied

    async def execute(self, input: QActor, output: QActor) -> bool:
        """Executes the mapping process.

        Args:
            input (QActor): Input actor stream to consume.
            output (QActor): Output actor stream to produce.

        Returns:
            bool : True if sucefull.
        """

        inflight = Queue(maxsize=DEFAULT_BATCH)

        runs = []

        async for id, data in input.iterable(output):
            if BULLET in id:
                # nao processa.
                await output.commit(id, data)
            else:
                await inflight.put(1)

                runs.append(
                    create_task(
                        self.wraped_applier(self.func, id, data, output, inflight)
                    )
                )

        await gather(*runs)
        await output.stop()

        return True


class QCallback(QControlProcess):
    """This process applies a particular function to each element of the input stream that collects metrics."""

    def __init__(
        self,
        func: Callable[[Key, Value, State], State],
        initstate: State,
        name: Union[None, str] = None,
    ):
        """Creates a calback process.

        Args:
            func (function): async function to apply.
            initstate (Any) : inicial state.
        """

        if name is None:
            name = f"Callback:{func}:"

        super().__init__(name)
        self.func = func
        self.initstate = initstate
        # self.states = {}

    async def control_execute(
        self, input: QActor, output: QActor, control: QActor
    ) -> bool:
        """Executes the callback process.

        Args:
            input (QActor): Input actor stream to consume.
            output (QActor): Output actor stream to produce.

        Returns:
            bool : True if sucefull.
        """

        state = self.initstate
        async for id, data in input.iterable(output):
            state = self.func(id, data, state)
            await output.commit(id, data)

        await control.commit(self.name, state)
        await output.stop()
        await control.stop()

        return True


class QCrono(QCallback):
    """This process applies a particular function to each element of the input stream that collects metrics."""

    def __init__(self, name: Union[None, str] = None):
        """Creates a crono process."""
        self.curr_rate = 10
        self.alpha = 0.5
        self.last_time = time.time()

        def append_time(id, data, state):
            now = time()

            elapsed = now - self.last_time

            if elapsed > self.curr_rate * 10:
                self.curr_rate = 10

            self.curr_rate = self.alpha * (self.curr_rate - elapsed) + elapsed
            print(f"crono:{name} >: {1/self.curr_rate}")

            # state.append(elapsed)

            self.last_time = now

            return state

        if name is None:
            name = "Crono"

        super().__init__(func=append_time, initstate=[], name=name)


class QCombine(QProcess):
    """This process combines elements of the input stream.

    Given a depth level this process combines all of the input elements that share a portion of the hierachical key.
    """

    def __init__(self, depth: int = 1, name: str = "combine", unbatch: bool = True):
        """Creates a combine processs given a depth level.

        Args:
            depth (int): level of agregation in the hierarchical key. Defaults to 1.
            unbatch (bool): input stream is batched or not. Defaults to True.
        """

        self.depth = depth
        self.unbatch = unbatch

        super().__init__(name)

    def __parsekey(self, id: str):
        """splits the hierarchical key into superkey and key and counts the number of elements belonging in the superkey hierarchy.

        Args:
            id (str): key to be parsed.

        Returns:
            superkey (str): superkey used for agregation.
            key (str): group id with the superkey hierarchy.
            total (int): number of elements in the superkey hierarchy.
        """
        id_ = id.split(SEP)

        superkey, key = SEP.join(id_[: self.depth]), SEP.join(id_[self.depth :])

        total = reduce(
            lambda a, b: a * b, [int(k.split(OF)[1]) for k in id_[self.depth :]], 1
        )

        return superkey, key, total

    async def execute(self, input: QActor, output: QActor) -> bool:
        """Executes the combine process.

        Args:

            input (QActor): Input actor stream to consume.
            output (QActor): Output actor stream to produce.

        Returns:
            bool : True if there are no elements in cache.
        """

        cache = {}

        async for id_, data_ in input.iterable(output):
            if self.unbatch:
                if BULLET in id_:
                    id_ = id_.replace(BULLET, "")
                    stream = [(id_, data_)]
                else:
                    stream = zip(id_.split(CAT), data_)
            else:
                stream = [(id_, data_)]

            for id, data in stream:
                superkey, key, total = self.__parsekey(id)

                if total == 1:
                    await output.commit(superkey, {key: data, "count": 1})

                else:
                    if superkey in cache:
                        # sp in memory.
                        cache[superkey][key] = data
                        cache[superkey]["count"] += 1

                        if cache[superkey]["count"] == total:
                            # gathered everything.
                            jointdata = cache.pop(superkey, None)

                            await output.commit(superkey, jointdata)

                    else:
                        # sp not in memory.
                        cache[superkey] = {key: data, "count": 1}

        await output.stop()

        return not (len(cache) > 0)


class QBarrier(QProcess):
    """This process creates a synchronization block. It applies a function inorder to the actor stream acording to specified ordering."""

    def __init__(
        self,
        functional: Callable[[Value], List[Value]],
        name: str = "barrier",
        order=int,
    ):
        """Creates a barrier process.

        Args:
            functional (function): Function to be applied in order.
            order (function : key -> int): Ordering criterion. Defaults to int.
        """
        self.functional = functional
        self.order = order

        super().__init__(name)

    async def execute(self, input: QActor, output: QActor, functional=None) -> bool:
        """Executes the barrier process.

        Args:
            input (QActor): Input actor stream to consume.
            output (QActor): Output actor stream to produce.

        Returns:s
        """
        if functional is None:
            functional = self.functional

        mark = 0
        priorityq = []

        async for id, data in input.iterable(output):
            p = self.order(id)

            heapq.heappush(priorityq, (p, id, data))

            while (len(priorityq) > 0) and (priorityq[0][0] == mark):
                _, idj, dataj = heapq.heappop(priorityq)

                mark += 1
                work_units = functional(dataj)
                total = len(work_units)

                for j, wi in enumerate(work_units):
                    await output.commit(f"{idj}{SEP}{j}{OF}{total}", wi)

        await output.stop()

        return True


class QStatefulBarrier(QBarrier):
    """This process creates a synchronization block. It applies a function inorder to the actor stream acording to specified ordering."""

    class QState:
        def init(self):
            raise NotImplementedError()

        def update(self, data: Value) -> List[Value]:
            raise NotImplementedError()

        def terminate(self):
            raise NotImplementedError()

    def __init__(
        self,
        functional: QState,
        name: str = "barrier",
        order=int,
    ):
        """Creates a barrier process.

        Args:
            functional (function): Function to be applied in order.
            order (function : key -> int): Ordering criterion. Defaults to int.
        """
        self.state_functional = functional
        self.order = order

        super().__init__(name=name, functional=None, order=order)

    async def execute(self, input: QActor, output: QActor) -> bool:
        """Executes the barrier process.

        Args:
            input (QActor): Input actor stream to consume.
            output (QActor): Output actor stream to produce.

        Returns:
            bool : True of sucessful.
        """

        self.state_functional.init()

        results = await super().execute(
            input=input, output=output, functional=self.state_functional.update
        )

        self.state_functional.terminate()

        return results


class QBatching(QProcess):
    """This process produces a batch of elements from the input stream."""

    def __init__(
        self,
        size: int = 8,
        name: str = "batching",
        select: Callable[[Value], bool] = lambda data: not (data is None),
    ):
        """Creates a batching proess.

        Args:
            size (int): Batch size. Defaults to 8.
            select (function): Predicate determining which values to form a batch.
        """

        self.size = size
        self.select = select
        super().__init__(name)

    async def execute(self, input: QActor, output: QActor) -> bool:
        """Executes the batching process.

        Args:
            input (QActor): Input actor stream to consume.
            output (QActor): Output actor stream to produce.

        Returns:
            bool : True if sucefull.
        """

        qdata, qid, qsz = [], [], 0

        async for id, data in input.iterable(output):
            if self.select(data):
                qdata.append(data)
                qid.append(id)
                qsz += 1
            else:
                await output.commit(f"{BULLET}{id}", data)

            if qsz == self.size:
                batch_data = qdata
                batch_id = CAT.join(qid)

                await output.commit(batch_id, batch_data)

                qdata, qid, qsz = [], [], 0

        if qsz > 0:
            batch_data = qdata
            batch_id = CAT.join(qid)
            await output.commit(batch_id, batch_data)

        await output.stop()

        return True


class QUnBatching(QProcess):
    def __init__(self, name: str = "unbatching"):
        super().__init__(name)

    async def execute(self, input: QActor, output: QActor) -> bool:
        """Executes the combine process.

        Args:

            input (QActor): Input actor stream to consume.
            output (QActor): Output actor stream to produce.

        Returns:
            bool : True if there are no elements in cache.
        """

        async for id_, data_ in input.iterable(output):
            if BULLET in id_:
                id_ = id_.replace(BULLET, "")
                stream = [(id_, data_)]
            else:
                stream = zip(id_.split(CAT), data_)

            for key, data in stream:
                await output.commit(key, data)

        await output.stop()

        return True


class QNativeMap(QMap):
    """Applies a function in another process in this machine and async waits for the result."""

    def __init__(
        self,
        func: Callable[[Value], Value],
        many: bool,
        name: Union[str, None] = None,
    ):
        """Create a native map process.

        Args:
            func (function): Function to be applied.
            many (bool): Whether to do a flat map or not.
        """

        _func = async_wrap(func)

        super().__init__(func=_func, many=many, name=name)


class QClassicMap(QNativeMap):
    """Applies a function another process in this machine and async waits for the result.

    It's a Native map with many=False.
    """

    def __init__(self, func: Callable[[Value], Value], name: Union[str, None] = None):
        """Creates a classic map process.

        Args:
            func (function): Function to be applied.
        """
        super().__init__(func=func, name=name, many=False)


class QFlatMap(QNativeMap):
    """Applies a function that produces a sequence of elements and adds each element to the output actor stream."""

    def __init__(self, func: Callable[[Value], List[Value]]):
        """Creates a flat map process.

        Args:
            func (function): Function to be applied.
        """
        super().__init__(func=func, many=True)


class QRemoteMap(QMap):
    """Applies a function in another machine and waits async for the result."""

    def __init__(
        self,
        url: str,
        pack_function: Callable[[Value], bytes] = lambda data: data,
        unpack_function: Callable[
            [Value, Value], Value
        ] = lambda input, predictions, kwargs: predictions,
        name: Union[str, None] = None,
        many: bool = True,
        inflight_batch: int = DEFAULT_INFLIGHT_BATCH,
        **kwargs,
    ):
        """Creates a remote map process.

        Args:
            url (str): http url of the target service.
            pack_function (function): Transforms each element into a serializable object.
            unpack_function (_type_): Integrates the function map results and stream elements into a single object.
        """

        self.inflight_batch = inflight_batch

        super().__init__(
            func=request_broadcast(
                url=url, pack_function=pack_function, unpack_function=unpack_function,**kwargs
            ),
            many=many,
            name=f"RemoteMap:{url}",
        )

    async def execute(self, input: QActor, output: QActor) -> bool:
        """Executes the remote mapping process.

        Args:
            input (QActor): Input actor stream to consume.
            output (QActor): Output actor stream to produce.

        Returns:
            bool : True if sucefull.
        """
        inflight = Queue(maxsize=self.inflight_batch)

        runs = []

        async with HttpSession(trace_configs=[trace_config]) as session:
            async for id, data in input.iterable(output):
                if BULLET in id:
                    # nao processa.
                    await output.commit(id, data)
                else:
                    await inflight.put(1)

                    runs.append(
                        create_task(
                            self.func_applier(
                                partial(self.func, session=session),
                                id,
                                data,
                                output,
                                inflight,
                            )
                        )
                    )

            await gather(*runs)
            await output.stop()

        return True


class QAggregate(QJunction):
    def __init__(self, key_factory: Callable[[Value], Key], name: str = "aggregate"):
        super().__init__(name)
        self.key_factory = key_factory

    async def execute(self, *inputs: List[QActor], output: QActor) -> bool:
        cache = {}

        for input in inputs:
            async for id_, data in input.iterable(output):
                key = self.key_factory(data)

                if key in cache:
                    # sp in memory.
                    cache[key].append(data)

                else:
                    # sp not in memory.
                    cache[key] = [data]

        for key, data in cache.items():
            await output.commit(key, data)

        await output.stop()

        return len(cache) > 0


class QControlledMap(QJunction):
    class QControlledFunc:
        def configure(self, controls: List[Tuple[Key, Value]]):
            raise NotImplementedError()

        def apply(self, value: Value) -> Value:
            raise NotImplementedError()

    def __init__(self, func: QControlledFunc, name: str = "controlled_map"):
        super().__init__(name)
        self.func = func

    async def execute(self, *inputs: List[QActor], output: QActor) -> bool:
        """Executes the junction process.

        Args:
            inputs (List[QActor]): Input actor streams to consume.
            output (QActor): Output actor stream to produce.

        Returns:
            bool : True if sucefull.
        """
        runs = []
        controls = []
        data_cache = []
        remote_func = None
        # ensure list
        inputs = list(inputs)

        inputs.sort(
            key=lambda x: int(x.control()),
            reverse=True,
        )  # run the controls first.

        missing_control_packets = len([1 for input in inputs if input.control()])

        total = len(inputs)

        for input in inputs:
            if input.control():
                missing_control_packets -= 1

            async for id, data in input.iterable(output):
                if input.control():
                    if CTRL in id:
                        controls.append((id.split(CTRL)[1], data))
                    else:
                        data_cache.append((id.split(BRANCH)[1], data))

                else:
                    # data_cache.append((id.split(BRANCH)[1], data))
                    runs.append(
                        create_task(func_applier(remote_func, id, data, output))
                    )

            if missing_control_packets == 0:
                missing_control_packets -= 1

                self.func.configure(controls)
                func_ = lambda x: self.func.apply(x)

                remote_func = async_wrap(func_)

                for idj, dataj in data_cache:
                    runs.append(
                        create_task(func_applier(remote_func, idj, dataj, output))
                    )

                data_cache = []

        assert missing_control_packets == -1, "Missing control packets."

        await gather(*runs)
        await output.stop()

        return True


class QJoin(QJunction):
    """Joins two streams."""

    def __init__(
        self,
        name: str = "join",
        join_function: Callable[[Value, Value], Value] = lambda x, y: (x, y),
    ):
        """Creates a join process.

        Args:
            name (str): Name of the process.
            join_function (function): Function to join the two streams.
        """

        self.join_function = join_function
        self.inner = False
        super().__init__(name)

    async def execute(self, *inputs: List[QActor], output: QActor) -> bool:
        """Executes the join process.

        Args:
            inputs (List[QActor]): Input actor streams to consume.
            output (QActor): Output actor stream to produce.

        Returns:
            bool : True if sucefull.
        """
        cache = {}
        # ensure list

        total = len(inputs)

        # ALL OF THE INPUTS SHARE THE SAME QUEUE OBJECT.

        for input in inputs:
            async for id, data in input.iterable(output):
                fid, key = id.split(BRANCH)

                if key in cache:
                    cache[key][fid] = data
                else:
                    cache[key] = {fid: data}

                if len(cache[key]) == total:
                    data = cache.pop(key, None)

                    await output.commit(key, self.__put_args_inorder(data))

        if not self.inner:
            for key, data in cache.items():
                total_keys = {str(i) for i in range(total)}

                missing_keys = total_keys - total_keys.intersection(data.keys())

                for missing_key in missing_keys:
                    data[missing_key] = None

                await output.commit(key, self.__put_args_inorder(data))

        await output.stop()

        return len(cache) == 0

    def __put_args_inorder(self, data):
        args = list(data.items())

        args.sort(key=lambda x: int(x[0]))

        args = [arg for _, arg in args]

        return self.join_function(*args)


async def func_applier_many(
    func,
    id: str,
    data: Any,
    output: QActor,
    unsubscribe: Union[Queue, None] = None,
) -> bool:
    """This function applies a function to a sequence of elements and adds each element to the output actor stream.

    Args:
        func (function): Function to be applied. ( Any -> List[Any] )
        id (str): element key.
        data (Any): element value.
        output (QActor): Output actor stream.
        unsubscribe (Union[Queue, None]) : Unsubscribe queue.
    """

    if asyncio.iscoroutinefunction(func):
        outputs = await func(data)
    else:
        outputs = func(data)
    n = len(outputs)

    for i, output_data in enumerate(outputs):
        await output.commit(f"{id}{SEP}{i}{OF}{n}", output_data)

    if unsubscribe:
        _ = await unsubscribe.get()


async def func_applier(
    func,
    id: str,
    data: Any,
    output: QActor,
    unsubscribe: Union[Queue, None] = None,
) -> bool:
    """This function applies a function to a single element and awaits the result.
    func (function): Function to be applied. ( Any -> Any )
    id (str): element key.
    data (Any): element value.
    output (QActor): Output actor stream.
    unsubscribe (Union[Queue, None]) : Rate Limiter Queue.
    """

    if asyncio.iscoroutinefunction(func):
        output_data = await func(data)
    else:
        output_data = func(data)

    await output.commit(id, output_data)

    if unsubscribe:
        _ = await unsubscribe.get()
