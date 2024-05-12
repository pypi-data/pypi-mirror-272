import yaml
from typing import Any, Union
from .base_serializer import BaseSerializer

class YAMLSerializer(BaseSerializer):
    def serialize(self, data: Any) -> str:
        """
        Serialize the input data into a YAML string.

        Parameters:
            data (Any): The data to be serialized.

        Returns:
            str: The serialized YAML string.
        """
        return yaml.dump(data)

    def deserialize(self, serialized_data: str) -> Any:
        """
        Deserialize the input YAML string into its original form.

        Parameters:
            serialized_data (str): The serialized YAML string.

        Returns:
            Any: The deserialized data.
        """
        return yaml.load(serialized_data, Loader=yaml.Loader)
