from gptvm.proto import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Workspace(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class ListReq(_message.Message):
    __slots__ = ("workgroup_id", "page", "size")
    WORKGROUP_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    workgroup_id: str
    page: int
    size: int
    def __init__(self, workgroup_id: _Optional[str] = ..., page: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...

class ListRes(_message.Message):
    __slots__ = ("code", "message", "workspaces", "total", "page", "size")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    message: str
    workspaces: _containers.RepeatedCompositeFieldContainer[Workspace]
    total: int
    page: int
    size: int
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., message: _Optional[str] = ..., workspaces: _Optional[_Iterable[_Union[Workspace, _Mapping]]] = ..., total: _Optional[int] = ..., page: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...

class CreateReq(_message.Message):
    __slots__ = ("name", "workgroup_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    WORKGROUP_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    workgroup_id: str
    def __init__(self, name: _Optional[str] = ..., workgroup_id: _Optional[str] = ...) -> None: ...

class CreateRes(_message.Message):
    __slots__ = ("code", "message", "workspace")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    message: str
    workspace: Workspace
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., message: _Optional[str] = ..., workspace: _Optional[_Union[Workspace, _Mapping]] = ...) -> None: ...

class DeleteReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteRes(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    message: str
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., message: _Optional[str] = ...) -> None: ...
