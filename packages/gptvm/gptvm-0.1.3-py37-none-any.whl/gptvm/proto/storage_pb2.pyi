from gptvm.proto import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Storage(_message.Message):
    __slots__ = ("id", "name", "type")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    type: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class StsToken(_message.Message):
    __slots__ = ("AccessKeyId", "SecretAccessKey", "SessionToken", "Expiration")
    ACCESSKEYID_FIELD_NUMBER: _ClassVar[int]
    SECRETACCESSKEY_FIELD_NUMBER: _ClassVar[int]
    SESSIONTOKEN_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    AccessKeyId: str
    SecretAccessKey: str
    SessionToken: str
    Expiration: str
    def __init__(self, AccessKeyId: _Optional[str] = ..., SecretAccessKey: _Optional[str] = ..., SessionToken: _Optional[str] = ..., Expiration: _Optional[str] = ...) -> None: ...

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
    __slots__ = ("code", "msg", "publicStorage", "privateStorage", "sts_token", "endpoint")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    PUBLICSTORAGE_FIELD_NUMBER: _ClassVar[int]
    PRIVATESTORAGE_FIELD_NUMBER: _ClassVar[int]
    STS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    publicStorage: _containers.RepeatedCompositeFieldContainer[Storage]
    privateStorage: _containers.RepeatedCompositeFieldContainer[Storage]
    sts_token: StsToken
    endpoint: str
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., publicStorage: _Optional[_Iterable[_Union[Storage, _Mapping]]] = ..., privateStorage: _Optional[_Iterable[_Union[Storage, _Mapping]]] = ..., sts_token: _Optional[_Union[StsToken, _Mapping]] = ..., endpoint: _Optional[str] = ...) -> None: ...

class CreateReq(_message.Message):
    __slots__ = ("name", "workgroup_id", "workspace_id", "application_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    WORKGROUP_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    workgroup_id: str
    workspace_id: str
    application_id: str
    def __init__(self, name: _Optional[str] = ..., workgroup_id: _Optional[str] = ..., workspace_id: _Optional[str] = ..., application_id: _Optional[str] = ...) -> None: ...

class CreateRes(_message.Message):
    __slots__ = ("code", "msg", "storage")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    storage: Storage
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ..., storage: _Optional[_Union[Storage, _Mapping]] = ...) -> None: ...

class DeleteReq(_message.Message):
    __slots__ = ("req", "id")
    REQ_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    req: _common_pb2.CommonReq
    id: str
    def __init__(self, req: _Optional[_Union[_common_pb2.CommonReq, _Mapping]] = ..., id: _Optional[str] = ...) -> None: ...

class DeleteRes(_message.Message):
    __slots__ = ("code", "msg")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    code: _common_pb2.Code
    msg: str
    def __init__(self, code: _Optional[_Union[_common_pb2.Code, str]] = ..., msg: _Optional[str] = ...) -> None: ...
