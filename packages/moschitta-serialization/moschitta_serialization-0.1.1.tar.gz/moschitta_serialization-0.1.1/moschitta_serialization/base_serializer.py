from typing import Any, Union


class BaseSerializer:
    def serialize(self, data: Any) -> Union[str, bytes]:
        """
        Serialize the input data into a string or bytes representation.

        Parameters:
            data (Any): The data to be serialized.

        Returns:
            Union[str, bytes]: The serialized data.
        """
        raise NotImplementedError()

    def deserialize(self, serialized_data: Union[str, bytes]) -> Any:
        """
        Deserialize the input serialized data into its original form.

        Parameters:
            serialized_data (Union[str, bytes]): The serialized data.

        Returns:
            Any: The deserialized data.
        """
        raise NotImplementedError()
