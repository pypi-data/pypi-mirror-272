# Devinci PyConfig

Devinci PyConfig is a Python toolkit for managing configuration properties in Python applications. It provides a simple way to load configuration settings from a configuration file and access them as attributes.

## Installation

You can install Devinci PyConfig using pip:

```bash
pip install devinci_pyconfig
```

## Usage

### Importing

You can import the `Config` class from the package:

```python
from devinci_pyconfig import PyConfig
```

### Initializing

To use the `Config` class, you can initialize it with the path to your configuration file (optional, defaults to 'config.ini'):

```python
config = PyConfig()
```

### Accessing Configuration Settings

Once initialized, you can access your configuration settings as attributes of the `Config` instance. For example, if your configuration file (`config.ini`) contains the following:

```ini
[Database]
host = localhost
port = 5432
username = user
password = password123
```

You can access these settings in your Python code like this:

```python
print(config.database_host)  # Output: localhost
print(config.database_port)  # Output: 5432
print(config.database_username)  # Output: user
print(config.database_password)  # Output: password123
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to customize this README with additional information or instructions specific to your package.