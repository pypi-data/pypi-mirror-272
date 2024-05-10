import json
from typing import Any, Union

from .base_serializer import BaseSerializer


class JSONSerializer(BaseSerializer):
    def serialize(self, data: Any) -> str:
        """
        Serialize the input data into a JSON string.

        Parameters:
            data (Any): The data to be serialized.

        Returns:
            str: The serialized JSON string.
        """
        return json.dumps(data)

    def deserialize(self, serialized_data: str) -> Any:
        """
        Deserialize the input JSON string into its original form.

        Parameters:
            serialized_data (str): The serialized JSON string.

        Returns:
            Any: The deserialized data.
        """
        return json.loads(serialized_data)
