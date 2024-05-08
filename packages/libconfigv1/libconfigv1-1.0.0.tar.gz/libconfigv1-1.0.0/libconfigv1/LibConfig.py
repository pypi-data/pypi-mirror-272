import os
import yaml

class LibConfig:
    def __init__(self, file):
        """
        Constructor for LibConfig.

        Args:
            file (str): The path to the YAML file.
        """
        self.file = file
        self.data = self.read()

    def get(self, key, default=None):
        """
        Get a configuration value by key.

        Args:
            key (str): The configuration key.
            default (any): The default value if the key is not found.

        Returns:
            any: The configuration value or the default value.
        """
        return self.data.get(key, default)

    def set(self, key, value):
        """
        Set a configuration value by key.

        Args:
            key (str): The configuration key.
            value (any): The value to set.
        """
        self.data[key] = value
        self.save()

    def read(self):
        """
        Read the configuration data from the YAML file.

        Returns:
            dict: The configuration data.
        """
        if os.path.exists(self.file):
            with open(self.file, 'r') as file:
                yaml_data = yaml.safe_load(file)
            return yaml_data
        return {}

    def save(self):
        """
        Save the configuration data to the YAML file.
        """
        with open(self.file, 'w') as file:
            yaml.dump(self.data, file)

