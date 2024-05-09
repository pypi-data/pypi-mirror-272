from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Code(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SUCC: _ClassVar[Code]
    FAIL: _ClassVar[Code]

class Err(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERR_UNKNOWN: _ClassVar[Err]
    INVALID_PARAM: _ClassVar[Err]
    NOT_FOUND: _ClassVar[Err]
    NOT_ALLOWED: _ClassVar[Err]
    NOT_AUTHORIZED: _ClassVar[Err]
    NOT_ENOUGH_QUOTA: _ClassVar[Err]
    NOT_ENOUGH_BALANCE: _ClassVar[Err]
    NOT_ENOUGH_STORAGE: _ClassVar[Err]
    NOT_ENOUGH_RESOURCE: _ClassVar[Err]
SUCC: Code
FAIL: Code
ERR_UNKNOWN: Err
INVALID_PARAM: Err
NOT_FOUND: Err
NOT_ALLOWED: Err
NOT_AUTHORIZED: Err
NOT_ENOUGH_QUOTA: Err
NOT_ENOUGH_BALANCE: Err
NOT_ENOUGH_STORAGE: Err
NOT_ENOUGH_RESOURCE: Err

class CommonReq(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class CommonRes(_message.Message):
    __slots__ = ("code", "msg", "data")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    code: str
    msg: str
    data: str
    def __init__(self, code: _Optional[str] = ..., msg: _Optional[str] = ..., data: _Optional[str] = ...) -> None: ...

class PaginationReq(_message.Message):
    __slots__ = ("page_num", "page_size")
    PAGE_NUM_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    page_num: int
    page_size: int
    def __init__(self, page_num: _Optional[int] = ..., page_size: _Optional[int] = ...) -> None: ...

class PaginationRes(_message.Message):
    __slots__ = ("page_num", "page_size", "total")
    PAGE_NUM_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    page_num: int
    page_size: int
    total: int
    def __init__(self, page_num: _Optional[int] = ..., page_size: _Optional[int] = ..., total: _Optional[int] = ...) -> None: ...
