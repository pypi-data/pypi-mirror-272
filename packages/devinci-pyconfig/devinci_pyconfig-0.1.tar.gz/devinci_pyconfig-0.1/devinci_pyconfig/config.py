import os
from configparser import ConfigParser

class Config:
    """
    A singleton class for managing configuration settings.

    Attributes:
        _instance (Config): Singleton instance of the Config class.
    """

    _instance = None

    def __new__(cls, config_file=None):
        """
        Create a new instance of the Config class or return the existing instance.

        Args:
            config_file (str, optional): Path to the configuration file. Default is 'config.ini'.

        Returns:
            Config: The singleton instance of the Config class.
        """
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config(config_file)
        return cls._instance

    def _load_config(self, config_file=None):
        """
        Load configuration settings from the specified configuration file.

        Args:
            config_file (str, optional): Path to the configuration file. Default is 'config.ini'.
        """
        if config_file is None:
            config_file = 'config.ini'  # Default config file path

        self._check_config_file(config_file)  # Check if config file exists

        config_parser = ConfigParser()
        config_parser.read(
            config_file)  # Read configuration from config.ini file

        # Load configuration values from config.ini and set them as attributes in the instance
        self._load_config_from_config_parser(config_parser)

    def _check_config_file(self, config_file):
        """
        Check if the specified configuration file exists.

        Args:
            config_file (str): Path to the configuration file.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
        """
        if not os.path.isfile(config_file):
            raise FileNotFoundError(
                f"Configuration file '{config_file}' not found.")

    def _load_config_from_config_parser(self, config_parser):
        """
        Load configuration settings from the ConfigParser object and set them as attributes.

        Args:
            config_parser (ConfigParser): ConfigParser object containing configuration settings.
        """
        # Load configuration values from config.ini and set them as attributes in the instance
        for section in config_parser.sections():
            for key, value in config_parser.items(section):
                setattr(self, f"{section.lower()}_{key.lower()}", value)
