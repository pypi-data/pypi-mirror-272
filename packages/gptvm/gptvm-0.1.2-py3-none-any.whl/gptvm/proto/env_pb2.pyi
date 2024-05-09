from gptvm.proto import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Env(_message.Message):
    __slots__ = ("id", "name", "value", "is_secret")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    IS_SECRET_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    value: str
    is_secret: bool
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., value: _Optional[str] = ..., is_secret: bool = ...) -> None: ...

class ListReq(_message.Message):
    __slots__ = ("workgroup_id", "workspace_id", "application_id")
    WORKGROUP_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    workgroup_id: str
    workspace_id: str
    application_id: str
    def __init__(self, workgroup_id: _Optional[str] = ..., workspace_id: _Optional[str] = ..., application_id: _Optional[str] = ...) -> None: ...

class ListRes(_message.Message):
    __slots__ = ("code", "msg", "envs")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    ENVS_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    envs: _containers.RepeatedCompositeFieldContainer[Env]
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., envs: _Optional[_Iterable[_Union[Env, _Mapping]]] = ...) -> None: ...

class CreateReq(_message.Message):
    __slots__ = ("name", "value", "is_secret", "workgroup_id", "workspace_id", "application_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    IS_SECRET_FIELD_NUMBER: _ClassVar[int]
    WORKGROUP_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    is_secret: bool
    workgroup_id: str
    workspace_id: str
    application_id: str
    def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ..., is_secret: bool = ..., workgroup_id: _Optional[str] = ..., workspace_id: _Optional[str] = ..., application_id: _Optional[str] = ...) -> None: ...

class CreateRes(_message.Message):
    __slots__ = ("code", "msg", "env")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    env: Env
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., env: _Optional[_Union[Env, _Mapping]] = ...) -> None: ...

class DeleteReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteRes(_message.Message):
    __slots__ = ("code", "msg")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ...) -> None: ...

class UpdateReq(_message.Message):
    __slots__ = ("id", "name", "value", "is_secret")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    IS_SECRET_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    value: str
    is_secret: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., value: _Optional[str] = ..., is_secret: _Optional[str] = ...) -> None: ...

class UpdateRes(_message.Message):
    __slots__ = ("code", "msg", "env")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    env: Env
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., env: _Optional[_Union[Env, _Mapping]] = ...) -> None: ...
