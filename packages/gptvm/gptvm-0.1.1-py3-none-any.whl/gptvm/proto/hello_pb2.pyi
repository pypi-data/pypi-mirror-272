from gptvm.proto import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HelloReq(_message.Message):
    __slots__ = ("name", "hi")
    NAME_FIELD_NUMBER: _ClassVar[int]
    HI_FIELD_NUMBER: _ClassVar[int]
    name: str
    hi: str
    def __init__(self, name: _Optional[str] = ..., hi: _Optional[str] = ...) -> None: ...

class HelloRes(_message.Message):
    __slots__ = ("hi", "res")
    HI_FIELD_NUMBER: _ClassVar[int]
    RES_FIELD_NUMBER: _ClassVar[int]
    hi: str
    res: _common_pb2.CommonRes
    def __init__(self, hi: _Optional[str] = ..., res: _Optional[_Union[_common_pb2.CommonRes, _Mapping]] = ...) -> None: ...
