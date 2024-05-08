
---

# LibConfig

LibConfig is a Python library for working with YAML configuration files.

## Installation

You can install LibConfig using pip:

```
pip install libconfig-py
```

## Usage

Here's how you can use LibConfig in your Python projects:

```python
from libconfig import LibConfig

# Initialize LibConfig with the path to your YAML file
yaml_file = "config.yaml"
lib_config = LibConfig(yaml_file)

# Get a configuration value by key
value = lib_config.get("key")
print("Value:", value)

# Set a configuration value by key
lib_config.set("key", "new_value")

# Get the updated value
updated_value = lib_config.get("key")
print("Updated Value:", updated_value)
```

## Contributing

Contributions to LibConfig are welcome! To contribute, please follow these guidelines:

- Fork the repository and clone it locally.
- Create a new branch for your feature or bug fix.
- Make your changes and ensure that tests pass.
- Commit your changes and push them to your fork.
- Submit a pull request with a clear description of your changes.

Before submitting a pull request, please make sure to run tests and linting using the following commands:

```
pytest
flake8
```

For more information, please read the [Contribution Guidelines](link_to_contributing_guide).

## License

LibConfig is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, feel free to reach out to the project maintainer

---
