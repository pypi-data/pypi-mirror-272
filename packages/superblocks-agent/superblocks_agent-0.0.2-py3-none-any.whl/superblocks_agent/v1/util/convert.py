from typing import Optional

import google.protobuf.struct_pb2 as struct_pb2
from google.protobuf.struct_pb2 import ListValue, Struct, Value


# NOTE: (joey) theres likely some existing automatic way to do this but for now this works
def to_protobuf_value(data: Optional[bool | int | float | str | dict | list]) -> Value:
    value = Value()
    match data:
        case None:
            value.null_value = 0  # NullValue enum
        case True | False:
            value.bool_value = data
        case _ if isinstance(data, int) | isinstance(data, float):
            value.number_value = data
        case _ if isinstance(data, str):
            value.string_value = data
        case _ if isinstance(data, dict):
            struct_value = Struct()
            for key, item in data.items():
                struct_value.fields[key].CopyFrom(to_protobuf_value(item))
            value.struct_value.CopyFrom(struct_value)
        case _ if isinstance(data, list):
            list_value = ListValue()
            list_value.values.extend(to_protobuf_value(item) for item in data)
            value.list_value.CopyFrom(list_value)
        case _:
            raise TypeError(f"Unsupported type: {type(data)}")
    return value


def from_protobuf_value(
    proto_value: struct_pb2.Value,
) -> Optional[int | float | str | bool | dict | list]:
    """Extracts native Python value from a protobuf Value object."""
    kind = proto_value.WhichOneof("kind")
    if kind == "null_value":
        return None
    elif kind == "number_value":
        return proto_value.number_value
    elif kind == "string_value":
        return proto_value.string_value
    elif kind == "bool_value":
        return proto_value.bool_value
    elif kind == "struct_value":
        return {k: from_protobuf_value(v) for k, v in proto_value.struct_value.fields.items()}
    elif kind == "list_value":
        return [from_protobuf_value(item) for item in proto_value.list_value.values]
    else:
        raise ValueError("Unknown type of value")
