from google.protobuf.message import Message
from google.protobuf.json_format import MessageToJson, Parse
from typing import Type
from .base_serializer import BaseSerializer

class ProtobufSerializer(BaseSerializer):
    def serialize(self, data: Message) -> str:
        """
        Serialize the protobuf Message into a JSON string representation.

        Parameters:
            data (Message): The protobuf Message to be serialized.

        Returns:
            str: The serialized data.
        """
        return MessageToJson(data)

    def deserialize(self, serialized_data: str, message_type: Type[Message]) -> Message:
        """
        Deserialize the input serialized data into a protobuf Message.

        Parameters:
            serialized_data (str): The serialized data.
            message_type (Type[Message]): The type of the protobuf Message.

        Returns:
            Message: The deserialized data.
        """
        return Parse(serialized_data, message_type())
