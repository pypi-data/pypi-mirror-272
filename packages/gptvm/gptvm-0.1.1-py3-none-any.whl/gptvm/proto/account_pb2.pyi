from gptvm.proto import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Account(_message.Message):
    __slots__ = ("balance",)
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    balance: float
    def __init__(self, balance: _Optional[float] = ...) -> None: ...

class InfoReq(_message.Message):
    __slots__ = ("workgroup_id",)
    WORKGROUP_ID_FIELD_NUMBER: _ClassVar[int]
    workgroup_id: str
    def __init__(self, workgroup_id: _Optional[str] = ...) -> None: ...

class InfoRes(_message.Message):
    __slots__ = ("code", "message", "account")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    message: str
    account: Account
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., message: _Optional[str] = ..., account: _Optional[_Union[Account, _Mapping]] = ...) -> None: ...
