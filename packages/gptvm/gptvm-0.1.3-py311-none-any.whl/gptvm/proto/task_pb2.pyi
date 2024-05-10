from google.protobuf import timestamp_pb2 as _timestamp_pb2
from gptvm.proto import common_pb2 as _common_pb2
from gptvm.proto import app_version_pb2 as _app_version_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TaskState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CREATED: _ClassVar[TaskState]
    STARTING: _ClassVar[TaskState]
    QUEUED: _ClassVar[TaskState]
    RUNNING: _ClassVar[TaskState]
    STOPPED: _ClassVar[TaskState]
CREATED: TaskState
STARTING: TaskState
QUEUED: TaskState
RUNNING: TaskState
STOPPED: TaskState

class Task(_message.Message):
    __slots__ = ("id", "pid", "application_id", "app_version_id", "name", "description", "status", "info", "suid", "created_at", "updated_at", "app_version")
    ID_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    APP_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    SUID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    APP_VERSION_FIELD_NUMBER: _ClassVar[int]
    id: str
    pid: str
    application_id: str
    app_version_id: str
    name: str
    description: str
    status: int
    info: str
    suid: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    app_version: _app_version_pb2.AppVer
    def __init__(self, id: _Optional[str] = ..., pid: _Optional[str] = ..., application_id: _Optional[str] = ..., app_version_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., status: _Optional[int] = ..., info: _Optional[str] = ..., suid: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., app_version: _Optional[_Union[_app_version_pb2.AppVer, _Mapping]] = ...) -> None: ...

class ListReq(_message.Message):
    __slots__ = ("app_id",)
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    def __init__(self, app_id: _Optional[str] = ...) -> None: ...

class ListRes(_message.Message):
    __slots__ = ("code", "msg", "tasks")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    TASKS_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    tasks: _containers.RepeatedCompositeFieldContainer[Task]
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., tasks: _Optional[_Iterable[_Union[Task, _Mapping]]] = ...) -> None: ...

class InfoReq(_message.Message):
    __slots__ = ("id", "only_latest_task")
    ID_FIELD_NUMBER: _ClassVar[int]
    ONLY_LATEST_TASK_FIELD_NUMBER: _ClassVar[int]
    id: str
    only_latest_task: bool
    def __init__(self, id: _Optional[str] = ..., only_latest_task: bool = ...) -> None: ...

class InfoRes(_message.Message):
    __slots__ = ("code", "msg", "task")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    task: Task
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., task: _Optional[_Union[Task, _Mapping]] = ...) -> None: ...

class GetLogsReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetLogsRes(_message.Message):
    __slots__ = ("code", "msg", "log")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    LOG_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    log: str
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., log: _Optional[str] = ...) -> None: ...

class StartReq(_message.Message):
    __slots__ = ("app_id", "code_location", "name", "image", "pid", "desc")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    DESC_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    code_location: str
    name: str
    image: str
    pid: str
    desc: str
    def __init__(self, app_id: _Optional[str] = ..., code_location: _Optional[str] = ..., name: _Optional[str] = ..., image: _Optional[str] = ..., pid: _Optional[str] = ..., desc: _Optional[str] = ...) -> None: ...

class StartRes(_message.Message):
    __slots__ = ("code", "msg", "task")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    task: Task
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., task: _Optional[_Union[Task, _Mapping]] = ...) -> None: ...

class StopReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class StopRes(_message.Message):
    __slots__ = ("code", "msg", "task")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    task: Task
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., task: _Optional[_Union[Task, _Mapping]] = ...) -> None: ...

class RestartReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class RestartRes(_message.Message):
    __slots__ = ("code", "msg", "task")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    task: Task
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., task: _Optional[_Union[Task, _Mapping]] = ...) -> None: ...
