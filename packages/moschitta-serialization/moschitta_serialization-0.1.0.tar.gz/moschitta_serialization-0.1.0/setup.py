# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moschitta_serialization']

package_data = \
{'': ['*']}

install_requires = \
['msgpack>=1.0.8,<2.0.0', 'protobuf>=5.26.1,<6.0.0', 'pyyaml>=6.0.1,<7.0.0']

entry_points = \
{'console_scripts': ['compile-protos = python compile_protos.py']}

setup_kwargs = {
    'name': 'moschitta-serialization',
    'version': '0.1.0',
    'description': '',
    'long_description': 'Here\'s the README for the `moschitta-serialization` package, formatted similarly to the `moschitta-routing` README:\n\n---\n\n# Moschitta Serialization\n\n`moschitta-serialization` is a Python package that provides serializers for converting data to and from various formats, including JSON, MessagePack, YAML, and Protobuf.\n\n## Table of Contents\n\n- [Installation](#installation)\n- [Usage](#usage)\n- [Protobuf Serialization](#protobuf-serialization)\n- [Testing](#testing)\n- [Contributing](#contributing)\n- [License](#license)\n\n## Installation\n\nTo install `moschitta-serialization`, you\'ll need Python 3.7 or higher, as well as Poetry for dependency management and building the package.\n\n1. **Install Poetry**: If you haven\'t already, install Poetry, a tool for dependency management and building Python packages. You can install it with the following command:\n\n    ```bash\n    curl -sSL https://install.python-poetry.org | python -\n    ```\n\n2. **Install Protobuf Compiler**: The Protobuf compiler (`protoc`) is required for compiling `.proto` files into Python code. You can install it as follows:\n\n    - On Ubuntu/Debian:\n\n        ```bash\n        sudo apt-get install protobuf-compiler\n        ```\n\n    - On macOS:\n\n        ```bash\n        brew install protobuf\n        ```\n\n    - On Windows, download pre-compiled binaries from the [Protocol Buffers GitHub repository](https://github.com/protocolbuffers/protobuf/releases). After downloading and unzipping the archive, add the `bin/` directory to your PATH.\n\n3. **Install the Package**: Navigate to the root directory of the `moschitta-serialization` package and run the following command to install the package and its dependencies:\n\n    ```bash\n    poetry install\n    ```\n\n## Usage\n\nThe `moschitta-serialization` package provides several serializers that you can use in your application. Here\'s an example of how to use the `JSONSerializer`:\n\n```python\nfrom moschitta_serialization.json_serializer import JSONSerializer\n\nserializer = JSONSerializer()\ndata = {"name": "John", "age": 30}\nserialized_data = serializer.serialize(data)\nprint(serialized_data)  # \'{"name": "John", "age": 30}\'\n```\n\nYou can use the other serializers in a similar way.\n\n## Protobuf Serialization\n\nTo use the `ProtobufSerializer`, you\'ll need to define your Protobuf messages in `.proto` files, compile these files into Python code, and import the generated classes in your application.\n\n1. **Define Protobuf Messages**: Create a `.proto` file in the `proto/` directory and define your Protobuf messages in it.\n\n2. **Compile `.proto` Files**: Run the `compile_protos.py` script to compile the `.proto` files into Python code:\n\n    ```bash\n    python compile_protos.py\n    ```\n\n3. **Import Message Types**: In your Python code, import the generated classes from the Python files:\n\n    ```python\n    from proto.person_pb2 import Person\n    ```\n\nYou can then use these classes with the `ProtobufSerializer`.\n\n## Testing\n\nThe `moschitta-serialization` package includes a suite of tests that you can run with pytest. To run the tests, navigate to the root directory of the package and run the following command:\n\n```bash\npoetry run pytest\n```\n\n## Contributing\n\nContributions to the `moschitta-serialization` package are welcome! Please submit a pull request or open an issue on the [GitHub repository](https://github.com/MoschittaFramework/moschitta-serialization).\n\n## License\n\nThis project is licensed under the terms of the [MIT License](LICENSE).\n\n',
    'author': 'Skyler Saville',
    'author_email': 'skylersaville@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
