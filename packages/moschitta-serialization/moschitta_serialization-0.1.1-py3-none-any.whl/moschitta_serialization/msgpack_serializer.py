import msgpack
from typing import Any, Union
from .base_serializer import BaseSerializer

class MsgPackSerializer(BaseSerializer):
    def serialize(self, data: Any) -> bytes:
        """
        Serialize the input data into a MessagePack binary.

        Parameters:
            data (Any): The data to be serialized.

        Returns:
            bytes: The serialized MessagePack binary.
        """
        return msgpack.packb(data)

    def deserialize(self, serialized_data: bytes) -> Any:
        """
        Deserialize the input MessagePack binary into its original form.

        Parameters:
            serialized_data (bytes): The serialized MessagePack binary.

        Returns:
            Any: The deserialized data.
        """
        return msgpack.unpackb(serialized_data)
