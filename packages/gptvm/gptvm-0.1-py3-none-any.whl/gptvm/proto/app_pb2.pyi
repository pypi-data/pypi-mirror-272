from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from gptvm.proto import common_pb2 as _common_pb2
from gptvm.proto import task_pb2 as _task_pb2
from gptvm.proto import app_version_pb2 as _app_version_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AppState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CREATED: _ClassVar[AppState]
    STARTING: _ClassVar[AppState]
    QUEUED: _ClassVar[AppState]
    RUNNING: _ClassVar[AppState]
    STOPPED: _ClassVar[AppState]

class AppStopReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NORMAL: _ClassVar[AppStopReason]
    CANCELED_BY_CLI: _ClassVar[AppStopReason]
    CANCELED_BY_WEB: _ClassVar[AppStopReason]
    KILLED_BY_CLI: _ClassVar[AppStopReason]
    KILLED_BY_WEB: _ClassVar[AppStopReason]

class UrlType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UPLOAD: _ClassVar[UrlType]
    DOWNLOAD: _ClassVar[UrlType]
    BOTH: _ClassVar[UrlType]

class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    START: _ClassVar[Action]
    STOP: _ClassVar[Action]
    FORCE_STOP: _ClassVar[Action]
    RESTART: _ClassVar[Action]
    FORCE_RESTART: _ClassVar[Action]
    INFO: _ClassVar[Action]
    UPDATE: _ClassVar[Action]
    LOGS: _ClassVar[Action]

class RunRemoteType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FUNCTION: _ClassVar[RunRemoteType]
    CONSTRUCTOR: _ClassVar[RunRemoteType]
    DESTRUCTOR: _ClassVar[RunRemoteType]
    METHOD: _ClassVar[RunRemoteType]

class force(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    soft: _ClassVar[force]
    hard: _ClassVar[force]
CREATED: AppState
STARTING: AppState
QUEUED: AppState
RUNNING: AppState
STOPPED: AppState
NORMAL: AppStopReason
CANCELED_BY_CLI: AppStopReason
CANCELED_BY_WEB: AppStopReason
KILLED_BY_CLI: AppStopReason
KILLED_BY_WEB: AppStopReason
UPLOAD: UrlType
DOWNLOAD: UrlType
BOTH: UrlType
START: Action
STOP: Action
FORCE_STOP: Action
RESTART: Action
FORCE_RESTART: Action
INFO: Action
UPDATE: Action
LOGS: Action
FUNCTION: RunRemoteType
CONSTRUCTOR: RunRemoteType
DESTRUCTOR: RunRemoteType
METHOD: RunRemoteType
soft: force
hard: force

class App(_message.Message):
    __slots__ = ("id", "name", "suid", "desc", "type", "status", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SUID_FIELD_NUMBER: _ClassVar[int]
    DESC_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    suid: str
    desc: str
    type: str
    status: int
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., suid: _Optional[str] = ..., desc: _Optional[str] = ..., type: _Optional[str] = ..., status: _Optional[int] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AppLog(_message.Message):
    __slots__ = ("id", "app_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    app_id: str
    def __init__(self, id: _Optional[str] = ..., app_id: _Optional[str] = ...) -> None: ...

class ListReq(_message.Message):
    __slots__ = ("workspace_id", "page", "size")
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    workspace_id: str
    page: int
    size: int
    def __init__(self, workspace_id: _Optional[str] = ..., page: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...

class ListRes(_message.Message):
    __slots__ = ("code", "msg", "apps", "total", "page", "size")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    APPS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    apps: _containers.RepeatedCompositeFieldContainer[App]
    total: int
    page: int
    size: int
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., apps: _Optional[_Iterable[_Union[App, _Mapping]]] = ..., total: _Optional[int] = ..., page: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...

class InfoReq(_message.Message):
    __slots__ = ("suid", "page", "size")
    SUID_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    suid: str
    page: int
    size: int
    def __init__(self, suid: _Optional[str] = ..., page: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...

class InfoRes(_message.Message):
    __slots__ = ("code", "msg", "app", "latest_version", "tasks", "total", "page", "size")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    LATEST_VERSION_FIELD_NUMBER: _ClassVar[int]
    TASKS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    app: App
    latest_version: _app_version_pb2.AppVer
    tasks: _containers.RepeatedCompositeFieldContainer[_task_pb2.Task]
    total: int
    page: int
    size: int
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., app: _Optional[_Union[App, _Mapping]] = ..., latest_version: _Optional[_Union[_app_version_pb2.AppVer, _Mapping]] = ..., tasks: _Optional[_Iterable[_Union[_task_pb2.Task, _Mapping]]] = ..., total: _Optional[int] = ..., page: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...

class CreateReq(_message.Message):
    __slots__ = ("workspace_id", "name", "desc")
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESC_FIELD_NUMBER: _ClassVar[int]
    workspace_id: str
    name: str
    desc: str
    def __init__(self, workspace_id: _Optional[str] = ..., name: _Optional[str] = ..., desc: _Optional[str] = ...) -> None: ...

class CreateRes(_message.Message):
    __slots__ = ("code", "msg", "app", "latest_version", "upload_url")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    LATEST_VERSION_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    app: App
    latest_version: _app_version_pb2.AppVer
    upload_url: str
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., app: _Optional[_Union[App, _Mapping]] = ..., latest_version: _Optional[_Union[_app_version_pb2.AppVer, _Mapping]] = ..., upload_url: _Optional[str] = ...) -> None: ...

class UrlReq(_message.Message):
    __slots__ = ("id", "type")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: UrlType
    def __init__(self, id: _Optional[str] = ..., type: _Optional[_Union[UrlType, str]] = ...) -> None: ...

class UrlRes(_message.Message):
    __slots__ = ("code", "msg", "upload_url", "download_url")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    upload_url: str
    download_url: str
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., upload_url: _Optional[str] = ..., download_url: _Optional[str] = ...) -> None: ...

class UpdateReq(_message.Message):
    __slots__ = ("id", "name", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class UpdateRes(_message.Message):
    __slots__ = ("code", "msg", "app")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    app: App
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., app: _Optional[_Union[App, _Mapping]] = ...) -> None: ...

class TaskResource(_message.Message):
    __slots__ = ("type", "quantity")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    type: str
    quantity: str
    def __init__(self, type: _Optional[str] = ..., quantity: _Optional[str] = ...) -> None: ...

class TaskRequest(_message.Message):
    __slots__ = ("name", "type", "image", "code_location", "description", "suid", "resources", "endpoint")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    CODE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SUID_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: str
    image: str
    code_location: str
    description: str
    suid: str
    resources: _containers.RepeatedCompositeFieldContainer[TaskResource]
    endpoint: str
    def __init__(self, name: _Optional[str] = ..., type: _Optional[str] = ..., image: _Optional[str] = ..., code_location: _Optional[str] = ..., description: _Optional[str] = ..., suid: _Optional[str] = ..., resources: _Optional[_Iterable[_Union[TaskResource, _Mapping]]] = ..., endpoint: _Optional[str] = ...) -> None: ...

class TaskResponse(_message.Message):
    __slots__ = ("name", "type", "endpoint", "status", "message", "suid", "addr")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SUID_FIELD_NUMBER: _ClassVar[int]
    ADDR_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: str
    endpoint: str
    status: str
    message: str
    suid: str
    addr: str
    def __init__(self, name: _Optional[str] = ..., type: _Optional[str] = ..., endpoint: _Optional[str] = ..., status: _Optional[str] = ..., message: _Optional[str] = ..., suid: _Optional[str] = ..., addr: _Optional[str] = ...) -> None: ...

class OperateReq(_message.Message):
    __slots__ = ("id", "action", "task")
    ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    id: str
    action: Action
    task: TaskRequest
    def __init__(self, id: _Optional[str] = ..., action: _Optional[_Union[Action, str]] = ..., task: _Optional[_Union[TaskRequest, _Mapping]] = ...) -> None: ...

class OperateRes(_message.Message):
    __slots__ = ("code", "msg", "app", "task")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    app: App
    task: TaskResponse
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., app: _Optional[_Union[App, _Mapping]] = ..., task: _Optional[_Union[TaskResponse, _Mapping]] = ...) -> None: ...

class RunRemoteReq(_message.Message):
    __slots__ = ("path", "fn", "args", "type", "qid", "addr", "app_id")
    PATH_FIELD_NUMBER: _ClassVar[int]
    FN_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    QID_FIELD_NUMBER: _ClassVar[int]
    ADDR_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    path: str
    fn: str
    args: bytes
    type: RunRemoteType
    qid: int
    addr: str
    app_id: str
    def __init__(self, path: _Optional[str] = ..., fn: _Optional[str] = ..., args: _Optional[bytes] = ..., type: _Optional[_Union[RunRemoteType, str]] = ..., qid: _Optional[int] = ..., addr: _Optional[str] = ..., app_id: _Optional[str] = ...) -> None: ...

class RunRemoteRes(_message.Message):
    __slots__ = ("ret", "stdout", "stderr", "qid", "heartbeat")
    RET_FIELD_NUMBER: _ClassVar[int]
    STDOUT_FIELD_NUMBER: _ClassVar[int]
    STDERR_FIELD_NUMBER: _ClassVar[int]
    QID_FIELD_NUMBER: _ClassVar[int]
    HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    ret: bytes
    stdout: str
    stderr: str
    qid: int
    heartbeat: _empty_pb2.Empty
    def __init__(self, ret: _Optional[bytes] = ..., stdout: _Optional[str] = ..., stderr: _Optional[str] = ..., qid: _Optional[int] = ..., heartbeat: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ...) -> None: ...

class StartReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class StartRes(_message.Message):
    __slots__ = ("code", "msg", "app")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    app: App
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., app: _Optional[_Union[App, _Mapping]] = ...) -> None: ...

class StopReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class StopRes(_message.Message):
    __slots__ = ("code", "msg", "app")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    app: App
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., app: _Optional[_Union[App, _Mapping]] = ...) -> None: ...

class RestartReq(_message.Message):
    __slots__ = ("id", "force")
    ID_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    force: force
    def __init__(self, id: _Optional[str] = ..., force: _Optional[_Union[force, str]] = ...) -> None: ...

class RestartRes(_message.Message):
    __slots__ = ("code", "msg", "app")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    app: App
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., app: _Optional[_Union[App, _Mapping]] = ...) -> None: ...

class PublishReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class PublishRes(_message.Message):
    __slots__ = ("code", "msg", "app")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    app: App
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., app: _Optional[_Union[App, _Mapping]] = ...) -> None: ...

class UnpublishReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class UnpublishRes(_message.Message):
    __slots__ = ("code", "msg", "app")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    app: App
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., app: _Optional[_Union[App, _Mapping]] = ...) -> None: ...

class GetLogsReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetLogsRes(_message.Message):
    __slots__ = ("code", "msg", "logs")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    logs: _containers.RepeatedCompositeFieldContainer[AppLog]
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., logs: _Optional[_Iterable[_Union[AppLog, _Mapping]]] = ...) -> None: ...

class RunCmdReq(_message.Message):
    __slots__ = ("id", "cmd")
    ID_FIELD_NUMBER: _ClassVar[int]
    CMD_FIELD_NUMBER: _ClassVar[int]
    id: str
    cmd: str
    def __init__(self, id: _Optional[str] = ..., cmd: _Optional[str] = ...) -> None: ...

class RunCmdRes(_message.Message):
    __slots__ = ("code", "msg")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ...) -> None: ...

class RunScriptReq(_message.Message):
    __slots__ = ("id", "script")
    ID_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_FIELD_NUMBER: _ClassVar[int]
    id: str
    script: str
    def __init__(self, id: _Optional[str] = ..., script: _Optional[str] = ...) -> None: ...

class RunScriptRes(_message.Message):
    __slots__ = ("code", "msg")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ...) -> None: ...
