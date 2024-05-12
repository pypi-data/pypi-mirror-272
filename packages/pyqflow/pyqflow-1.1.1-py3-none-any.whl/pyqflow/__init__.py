from pyqflow.actor import QFileSource, QIterable, QVideo
from pyqflow.process import (
    QAggregate,
    QBarrier,
    QBatching,
    QCallback,
    QClassicMap,
    QCombine,
    QControlledMap,
    QFlatMap,
    QJoin,
    QNativeMap,
    QRemoteMap,
    QStatefulBarrier,
    QUnBatching,
    QMap,
)
from pyqflow.workflow import QSequential, QUnitaryWorkflow, QWorkFlow

(
    NativeMap,
    RemoteMap,
    Barrier,
    StatefulBarrier,
    Combine,
    Batching,
    Join,
    ClassicMap,
    Aggregate,
    UnBatching,
    Callback,
    ControlledMap,
    FlatMap,
) = (
    QNativeMap,
    QRemoteMap,
    QBarrier,
    QStatefulBarrier,
    QCombine,
    QBatching,
    QJoin,
    QClassicMap,
    QAggregate,
    QUnBatching,
    QCallback,
    QControlledMap,
    QFlatMap,
)

Iterable, Video, FileSource = QIterable, QVideo, QFileSource
WorkFlow, Sequential, UnitaryWorkflow = QWorkFlow, QSequential, QUnitaryWorkflow
