# external imports
import abc
import asyncio
from typing import Any, List

# internal imports
from pyqflow.actor import QActor
from pyqflow.process import QProcess

import json


class QWorkFlow:
    """Pipeline abstract class.

    This entity is an abstract for every pipeline definition.
    """

    def __init__(self, name=""):
        """creates a Workflow object."""
        self.name = name
        self._params = None

    @property
    def params(self):
        if self._params is None:
            self._params = self.__dict__.copy()

        return self._params

    @params.setter
    def params(self, value):
        self._params = value

    def get_metadata(self):
        """
        Get the metadata packet for the DetectionFlow class.

        Returns:
            Tuple[str, str]: A tuple containing the name and the parameters in JSON format.
        """
        return self.name, json.dumps(self.params)

    @abc.abstractmethod
    def forward(self, *args, **kwargs):
        """This function defines the pipeline logic. It must be implemented by any pipeline."""
        raise NotImplementedError()

    def show(self, *args, save_img=False, **kwargs):
        """Plots the workflow diagram.

        Does a reverse breath first transversal to plot the workflow.
        """

        output_node = self.forward(*args, **kwargs)

        if not isinstance(output_node, tuple):
            node_dict = {output_node: {}}
            frontier = [output_node]
        else:
            node_dict = {}
            frontier = []

            for node in output_node:
                node_dict[node] = {}
                frontier.append(node)

        edges = []

        while len(frontier) > 0:
            new_frontier = []

            for leaf in frontier:
                for node in leaf.parents:
                    if node not in node_dict:
                        new_frontier.append(node)
                        node_dict[node] = node.children.keys()

                        for child in node.children.keys():
                            edges.append((node.name, child.name))

            frontier = new_frontier

        try:
            import matplotlib.pyplot as plt
            import networkx as nx
        except ImportError:
            raise ImportError(
                "Matplotlib and Networkx are required to plot the workflow."
            )

        plt.figure(figsize=(18, 18))

        G = nx.DiGraph(edges)
        pos = nx.fruchterman_reingold_layout(G)  # Seed layout for reproducibility
        nx.draw(
            G,
            pos,
            node_color="b",
            node_size=400,
            with_labels=True,
            font_size=12,
        )

        if save_img:
            plt.savefig("workflow.pdf")

        else:
            plt.show()

    async def __call__(self, *args, **kwargs) -> List[Any]:
        """Auxiliary function to define and run the pipeline.

        Returns:
            List[Any]: One result for each output actor of the pipeline.
        """

        output = self.forward(*args, **kwargs)
        return await QWorkFlow.run(output)

    def __or__(self, other):
        if isinstance(other, QWorkFlow):
            return QSequential(self, other)

        elif isinstance(other, QProcess):
            return QSequential(self, QUnitaryWorkflow(other))
        else:
            raise ValueError("Invalid operand type.")

    async def run(*kwargs: List[QActor]) -> List[Any]:
        """Function to run the pipeline.

        Returns:
            List[Any]: One result for each output actor of the pipeline.
        """

        tasks = []
        initial_frontier = []
        visited = set()

        for output in kwargs:
            if isinstance(output, list):
                initial_frontier.extend(output)

            if isinstance(output, tuple):
                initial_frontier.extend(output)

            else:
                initial_frontier.append(output)

        frontier = list(initial_frontier)

        while len(frontier) > 0:
            next_frontier = []

            for node in frontier:
                if node.runnable() or node.source():
                    if node.source():
                        tasks.append(asyncio.create_task(node.feed()))

                    else:
                        op, parents = node.execution_context()

                        for p in parents:
                            if p not in visited:
                                visited.add(p)
                                next_frontier.append(p)

                        tasks.append(
                            asyncio.create_task(op.execute(*parents, output=node))
                        )

            frontier = next_frontier

        for output in initial_frontier:
            tasks.append(asyncio.create_task(output.tolist()))

        noutputs = len(initial_frontier)

        results = await asyncio.gather(*tasks)

        return results[-noutputs:]


class QSequential(QWorkFlow):
    """Workflow generated by the sequenctial composition of workflows."""

    def __init__(self, *flows: List[QWorkFlow]):
        """Creates a sequential workflow.

        Args:
            *flows (List[QWorkFlow]): A list of workflows to be sequencially composed.
        """
        super().__init__(name="Sequential")
        self.flows = flows

    def forward(self, *args, **kwargs) -> QActor:
        """Implements the sequential pipeline definition.

        Returns:
            QActor: output actor of the sequential workflow.
        """

        result = self.flows[0].forward(*args, **kwargs)

        for wf in self.flows[1:]:
            if isinstance(result, tuple):
                result = wf.forward(*result, **kwargs)
            else:
                result = wf.forward(result, **kwargs)

        return result


class QUnitaryWorkflow(QWorkFlow):
    def __init__(self, process: QProcess):
        """Creates a unitary workflow.

        Args:
            process (QProcess): A process to be executed.
        """
        super().__init__(name="Unitary")
        self.process = process

    def forward(self, *args) -> QActor:
        return self.process(*args)
