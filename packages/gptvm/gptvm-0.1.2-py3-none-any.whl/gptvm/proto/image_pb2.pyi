from gptvm.proto import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Image(_message.Message):
    __slots__ = ("id", "name", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class ListReq(_message.Message):
    __slots__ = ("req",)
    REQ_FIELD_NUMBER: _ClassVar[int]
    req: _common_pb2.CommonReq
    def __init__(self, req: _Optional[_Union[_common_pb2.CommonReq, _Mapping]] = ...) -> None: ...

class ListRes(_message.Message):
    __slots__ = ("res", "images")
    RES_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    res: _common_pb2.CommonRes
    images: _containers.RepeatedCompositeFieldContainer[Image]
    def __init__(self, res: _Optional[_Union[_common_pb2.CommonRes, _Mapping]] = ..., images: _Optional[_Iterable[_Union[Image, _Mapping]]] = ...) -> None: ...

class UploadReq(_message.Message):
    __slots__ = ("req", "image")
    REQ_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    req: _common_pb2.CommonReq
    image: Image
    def __init__(self, req: _Optional[_Union[_common_pb2.CommonReq, _Mapping]] = ..., image: _Optional[_Union[Image, _Mapping]] = ...) -> None: ...

class UploadRes(_message.Message):
    __slots__ = ("res", "image")
    RES_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    res: _common_pb2.CommonRes
    image: Image
    def __init__(self, res: _Optional[_Union[_common_pb2.CommonRes, _Mapping]] = ..., image: _Optional[_Union[Image, _Mapping]] = ...) -> None: ...

class DeleteReq(_message.Message):
    __slots__ = ("req", "id")
    REQ_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    req: _common_pb2.CommonReq
    id: str
    def __init__(self, req: _Optional[_Union[_common_pb2.CommonReq, _Mapping]] = ..., id: _Optional[str] = ...) -> None: ...

class DeleteRes(_message.Message):
    __slots__ = ("res",)
    RES_FIELD_NUMBER: _ClassVar[int]
    res: _common_pb2.CommonRes
    def __init__(self, res: _Optional[_Union[_common_pb2.CommonRes, _Mapping]] = ...) -> None: ...
