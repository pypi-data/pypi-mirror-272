"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import google.protobuf.timestamp_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class DataType(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INT_TYPE_FIELD_NUMBER: builtins.int
    DOUBLE_TYPE_FIELD_NUMBER: builtins.int
    STRING_TYPE_FIELD_NUMBER: builtins.int
    BOOL_TYPE_FIELD_NUMBER: builtins.int
    TIMESTAMP_TYPE_FIELD_NUMBER: builtins.int
    ARRAY_TYPE_FIELD_NUMBER: builtins.int
    MAP_TYPE_FIELD_NUMBER: builtins.int
    EMBEDDING_TYPE_FIELD_NUMBER: builtins.int
    BETWEEN_TYPE_FIELD_NUMBER: builtins.int
    ONE_OF_TYPE_FIELD_NUMBER: builtins.int
    REGEX_TYPE_FIELD_NUMBER: builtins.int
    OPTIONAL_TYPE_FIELD_NUMBER: builtins.int
    STRUCT_TYPE_FIELD_NUMBER: builtins.int
    DECIMAL_TYPE_FIELD_NUMBER: builtins.int
    @property
    def int_type(self) -> global___IntType: ...
    @property
    def double_type(self) -> global___DoubleType: ...
    @property
    def string_type(self) -> global___StringType: ...
    @property
    def bool_type(self) -> global___BoolType: ...
    @property
    def timestamp_type(self) -> global___TimestampType: ...
    @property
    def array_type(self) -> global___ArrayType: ...
    @property
    def map_type(self) -> global___MapType: ...
    @property
    def embedding_type(self) -> global___EmbeddingType: ...
    @property
    def between_type(self) -> global___Between: ...
    @property
    def one_of_type(self) -> global___OneOf: ...
    @property
    def regex_type(self) -> global___RegexType: ...
    @property
    def optional_type(self) -> global___OptionalType: ...
    @property
    def struct_type(self) -> global___StructType: ...
    @property
    def decimal_type(self) -> global___DecimalType: ...
    def __init__(
        self,
        *,
        int_type: global___IntType | None = ...,
        double_type: global___DoubleType | None = ...,
        string_type: global___StringType | None = ...,
        bool_type: global___BoolType | None = ...,
        timestamp_type: global___TimestampType | None = ...,
        array_type: global___ArrayType | None = ...,
        map_type: global___MapType | None = ...,
        embedding_type: global___EmbeddingType | None = ...,
        between_type: global___Between | None = ...,
        one_of_type: global___OneOf | None = ...,
        regex_type: global___RegexType | None = ...,
        optional_type: global___OptionalType | None = ...,
        struct_type: global___StructType | None = ...,
        decimal_type: global___DecimalType | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["array_type", b"array_type", "between_type", b"between_type", "bool_type", b"bool_type", "decimal_type", b"decimal_type", "double_type", b"double_type", "dtype", b"dtype", "embedding_type", b"embedding_type", "int_type", b"int_type", "map_type", b"map_type", "one_of_type", b"one_of_type", "optional_type", b"optional_type", "regex_type", b"regex_type", "string_type", b"string_type", "struct_type", b"struct_type", "timestamp_type", b"timestamp_type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["array_type", b"array_type", "between_type", b"between_type", "bool_type", b"bool_type", "decimal_type", b"decimal_type", "double_type", b"double_type", "dtype", b"dtype", "embedding_type", b"embedding_type", "int_type", b"int_type", "map_type", b"map_type", "one_of_type", b"one_of_type", "optional_type", b"optional_type", "regex_type", b"regex_type", "string_type", b"string_type", "struct_type", b"struct_type", "timestamp_type", b"timestamp_type"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["dtype", b"dtype"]) -> typing_extensions.Literal["int_type", "double_type", "string_type", "bool_type", "timestamp_type", "array_type", "map_type", "embedding_type", "between_type", "one_of_type", "regex_type", "optional_type", "struct_type", "decimal_type"] | None: ...

global___DataType = DataType

@typing_extensions.final
class Field(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    DTYPE_FIELD_NUMBER: builtins.int
    name: builtins.str
    @property
    def dtype(self) -> global___DataType: ...
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        dtype: global___DataType | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["dtype", b"dtype"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["dtype", b"dtype", "name", b"name"]) -> None: ...

global___Field = Field

@typing_extensions.final
class IntType(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___IntType = IntType

@typing_extensions.final
class DoubleType(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___DoubleType = DoubleType

@typing_extensions.final
class StringType(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___StringType = StringType

@typing_extensions.final
class BoolType(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___BoolType = BoolType

@typing_extensions.final
class TimestampType(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___TimestampType = TimestampType

@typing_extensions.final
class RegexType(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PATTERN_FIELD_NUMBER: builtins.int
    pattern: builtins.str
    def __init__(
        self,
        *,
        pattern: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["pattern", b"pattern"]) -> None: ...

global___RegexType = RegexType

@typing_extensions.final
class ArrayType(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    OF_FIELD_NUMBER: builtins.int
    @property
    def of(self) -> global___DataType: ...
    def __init__(
        self,
        *,
        of: global___DataType | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["of", b"of"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["of", b"of"]) -> None: ...

global___ArrayType = ArrayType

@typing_extensions.final
class EmbeddingType(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EMBEDDING_SIZE_FIELD_NUMBER: builtins.int
    embedding_size: builtins.int
    def __init__(
        self,
        *,
        embedding_size: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["embedding_size", b"embedding_size"]) -> None: ...

global___EmbeddingType = EmbeddingType

@typing_extensions.final
class MapType(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KEY_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    @property
    def key(self) -> global___DataType: ...
    @property
    def value(self) -> global___DataType: ...
    def __init__(
        self,
        *,
        key: global___DataType | None = ...,
        value: global___DataType | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

global___MapType = MapType

@typing_extensions.final
class StructType(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    FIELDS_FIELD_NUMBER: builtins.int
    name: builtins.str
    @property
    def fields(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Field]: ...
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        fields: collections.abc.Iterable[global___Field] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["fields", b"fields", "name", b"name"]) -> None: ...

global___StructType = StructType

@typing_extensions.final
class Between(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DTYPE_FIELD_NUMBER: builtins.int
    MIN_FIELD_NUMBER: builtins.int
    MAX_FIELD_NUMBER: builtins.int
    STRICT_MIN_FIELD_NUMBER: builtins.int
    STRICT_MAX_FIELD_NUMBER: builtins.int
    @property
    def dtype(self) -> global___DataType: ...
    @property
    def min(self) -> global___Value: ...
    @property
    def max(self) -> global___Value: ...
    strict_min: builtins.bool
    strict_max: builtins.bool
    def __init__(
        self,
        *,
        dtype: global___DataType | None = ...,
        min: global___Value | None = ...,
        max: global___Value | None = ...,
        strict_min: builtins.bool = ...,
        strict_max: builtins.bool = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["dtype", b"dtype", "max", b"max", "min", b"min"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["dtype", b"dtype", "max", b"max", "min", b"min", "strict_max", b"strict_max", "strict_min", b"strict_min"]) -> None: ...

global___Between = Between

@typing_extensions.final
class OneOf(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    OF_FIELD_NUMBER: builtins.int
    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def of(self) -> global___DataType: ...
    @property
    def options(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Value]: ...
    def __init__(
        self,
        *,
        of: global___DataType | None = ...,
        options: collections.abc.Iterable[global___Value] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["of", b"of"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["of", b"of", "options", b"options"]) -> None: ...

global___OneOf = OneOf

@typing_extensions.final
class OptionalType(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    OF_FIELD_NUMBER: builtins.int
    @property
    def of(self) -> global___DataType: ...
    def __init__(
        self,
        *,
        of: global___DataType | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["of", b"of"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["of", b"of"]) -> None: ...

global___OptionalType = OptionalType

@typing_extensions.final
class DecimalType(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SCALE_FIELD_NUMBER: builtins.int
    scale: builtins.int
    def __init__(
        self,
        *,
        scale: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["scale", b"scale"]) -> None: ...

global___DecimalType = DecimalType

@typing_extensions.final
class Schema(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FIELDS_FIELD_NUMBER: builtins.int
    @property
    def fields(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Field]: ...
    def __init__(
        self,
        *,
        fields: collections.abc.Iterable[global___Field] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["fields", b"fields"]) -> None: ...

global___Schema = Schema

@typing_extensions.final
class DSSchema(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KEYS_FIELD_NUMBER: builtins.int
    VALUES_FIELD_NUMBER: builtins.int
    TIMESTAMP_FIELD_NUMBER: builtins.int
    ERASE_KEYS_FIELD_NUMBER: builtins.int
    @property
    def keys(self) -> global___Schema: ...
    @property
    def values(self) -> global___Schema: ...
    timestamp: builtins.str
    @property
    def erase_keys(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        keys: global___Schema | None = ...,
        values: global___Schema | None = ...,
        timestamp: builtins.str = ...,
        erase_keys: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["keys", b"keys", "values", b"values"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["erase_keys", b"erase_keys", "keys", b"keys", "timestamp", b"timestamp", "values", b"values"]) -> None: ...

global___DSSchema = DSSchema

@typing_extensions.final
class Value(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NONE_FIELD_NUMBER: builtins.int
    BOOL_FIELD_NUMBER: builtins.int
    INT_FIELD_NUMBER: builtins.int
    FLOAT_FIELD_NUMBER: builtins.int
    STRING_FIELD_NUMBER: builtins.int
    TIMESTAMP_FIELD_NUMBER: builtins.int
    EMBEDDING_FIELD_NUMBER: builtins.int
    LIST_FIELD_NUMBER: builtins.int
    MAP_FIELD_NUMBER: builtins.int
    STRUCT_FIELD_NUMBER: builtins.int
    DECIMAL_FIELD_NUMBER: builtins.int
    @property
    def none(self) -> global____r_None: ...
    bool: builtins.bool
    int: builtins.int
    float: builtins.float
    string: builtins.str
    @property
    def timestamp(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    @property
    def embedding(self) -> global___Embedding: ...
    @property
    def list(self) -> global___List: ...
    @property
    def map(self) -> global___Map: ...
    @property
    def struct(self) -> global___StructValue: ...
    @property
    def decimal(self) -> global___Decimal: ...
    def __init__(
        self,
        *,
        none: global____r_None | None = ...,
        bool: builtins.bool = ...,
        int: builtins.int = ...,
        float: builtins.float = ...,
        string: builtins.str = ...,
        timestamp: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        embedding: global___Embedding | None = ...,
        list: global___List | None = ...,
        map: global___Map | None = ...,
        struct: global___StructValue | None = ...,
        decimal: global___Decimal | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["bool", b"bool", "decimal", b"decimal", "embedding", b"embedding", "float", b"float", "int", b"int", "list", b"list", "map", b"map", "none", b"none", "string", b"string", "struct", b"struct", "timestamp", b"timestamp", "variant", b"variant"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["bool", b"bool", "decimal", b"decimal", "embedding", b"embedding", "float", b"float", "int", b"int", "list", b"list", "map", b"map", "none", b"none", "string", b"string", "struct", b"struct", "timestamp", b"timestamp", "variant", b"variant"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["variant", b"variant"]) -> typing_extensions.Literal["none", "bool", "int", "float", "string", "timestamp", "embedding", "list", "map", "struct", "decimal"] | None: ...

global___Value = Value

@typing_extensions.final
class Embedding(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
    def __init__(
        self,
        *,
        values: collections.abc.Iterable[builtins.float] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["values", b"values"]) -> None: ...

global___Embedding = Embedding

@typing_extensions.final
class List(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DTYPE_FIELD_NUMBER: builtins.int
    VALUES_FIELD_NUMBER: builtins.int
    @property
    def dtype(self) -> global___DataType: ...
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Value]: ...
    def __init__(
        self,
        *,
        dtype: global___DataType | None = ...,
        values: collections.abc.Iterable[global___Value] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["dtype", b"dtype"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["dtype", b"dtype", "values", b"values"]) -> None: ...

global___List = List

@typing_extensions.final
class Map(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class Entry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        @property
        def key(self) -> global___Value: ...
        @property
        def value(self) -> global___Value: ...
        def __init__(
            self,
            *,
            key: global___Value | None = ...,
            value: global___Value | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    KEY_DTYPE_FIELD_NUMBER: builtins.int
    VALUE_DTYPE_FIELD_NUMBER: builtins.int
    ENTRIES_FIELD_NUMBER: builtins.int
    @property
    def key_dtype(self) -> global___DataType: ...
    @property
    def value_dtype(self) -> global___DataType: ...
    @property
    def entries(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Map.Entry]: ...
    def __init__(
        self,
        *,
        key_dtype: global___DataType | None = ...,
        value_dtype: global___DataType | None = ...,
        entries: collections.abc.Iterable[global___Map.Entry] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["key_dtype", b"key_dtype", "value_dtype", b"value_dtype"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["entries", b"entries", "key_dtype", b"key_dtype", "value_dtype", b"value_dtype"]) -> None: ...

global___Map = Map

@typing_extensions.final
class StructValue(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class Entry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        NAME_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        name: builtins.str
        @property
        def value(self) -> global___Value: ...
        def __init__(
            self,
            *,
            name: builtins.str = ...,
            value: global___Value | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "value", b"value"]) -> None: ...

    FIELDS_FIELD_NUMBER: builtins.int
    @property
    def fields(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___StructValue.Entry]: ...
    def __init__(
        self,
        *,
        fields: collections.abc.Iterable[global___StructValue.Entry] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["fields", b"fields"]) -> None: ...

global___StructValue = StructValue

@typing_extensions.final
class Decimal(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SCALE_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    scale: builtins.int
    value: builtins.int
    def __init__(
        self,
        *,
        scale: builtins.int = ...,
        value: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["scale", b"scale", "value", b"value"]) -> None: ...

global___Decimal = Decimal

@typing_extensions.final
class _r_None(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global____r_None = _r_None
