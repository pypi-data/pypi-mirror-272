from gptvm.proto import common_pb2 as _common_pb2
from gptvm.proto import account_pb2 as _account_pb2
from gptvm.proto import workspace_pb2 as _workspace_pb2
from gptvm.proto import workgroup_pb2 as _workgroup_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("sn", "username", "email", "phone")
    SN_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    sn: str
    username: str
    email: str
    phone: str
    def __init__(self, sn: _Optional[str] = ..., username: _Optional[str] = ..., email: _Optional[str] = ..., phone: _Optional[str] = ...) -> None: ...

class LoginReq(_message.Message):
    __slots__ = ("email", "password")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class LoginRes(_message.Message):
    __slots__ = ("token", "user_info", "account", "default_group", "default_space")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    USER_INFO_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_GROUP_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_SPACE_FIELD_NUMBER: _ClassVar[int]
    token: str
    user_info: User
    account: _account_pb2.Account
    default_group: _workgroup_pb2.Workgroup
    default_space: _workspace_pb2.Workspace
    def __init__(self, token: _Optional[str] = ..., user_info: _Optional[_Union[User, _Mapping]] = ..., account: _Optional[_Union[_account_pb2.Account, _Mapping]] = ..., default_group: _Optional[_Union[_workgroup_pb2.Workgroup, _Mapping]] = ..., default_space: _Optional[_Union[_workspace_pb2.Workspace, _Mapping]] = ...) -> None: ...

class LogoutReq(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class LogoutRes(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    message: str
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., message: _Optional[str] = ...) -> None: ...

class InfoReq(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class InfoRes(_message.Message):
    __slots__ = ("code", "message", "profile")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    message: str
    profile: User
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., message: _Optional[str] = ..., profile: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class GetGroupsReq(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class GetGroupsRes(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    message: str
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., message: _Optional[str] = ...) -> None: ...

class GetOwnGroupsReq(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class GetOwnGroupsRes(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    message: str
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., message: _Optional[str] = ...) -> None: ...
