from gptvm.proto import common_pb2 as _common_pb2
from gptvm.proto import workspace_pb2 as _workspace_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Workgroup(_message.Message):
    __slots__ = ("id", "name", "workspaces")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACES_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    workspaces: _containers.RepeatedCompositeFieldContainer[_workspace_pb2.Workspace]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., workspaces: _Optional[_Iterable[_Union[_workspace_pb2.Workspace, _Mapping]]] = ...) -> None: ...

class ListReq(_message.Message):
    __slots__ = ("page", "size")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    page: int
    size: int
    def __init__(self, page: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...

class ListRes(_message.Message):
    __slots__ = ("code", "message", "workgroups", "total", "page", "size")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    WORKGROUPS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    message: str
    workgroups: _containers.RepeatedCompositeFieldContainer[Workgroup]
    total: int
    page: int
    size: int
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., message: _Optional[str] = ..., workgroups: _Optional[_Iterable[_Union[Workgroup, _Mapping]]] = ..., total: _Optional[int] = ..., page: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...
