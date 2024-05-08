# nix-python-utils

**Description**:
A collection of versatile classes, methods and decorators that I frequently use across my work projects.

## Content

- [Install](#Install)
- [Classes](#Classes)
- [Decorators](#Decorators)
- [Licence](#Licence)

##Install

```bash
pip install nix-python-utils
```

## Classes

For use classes you need to import them from the package:

```python
import nix.classes as classes
```

| Method                           | Parameters                                               | Returns | Description                                                               |
|----------------------------------|----------------------------------------------------------|---------|---------------------------------------------------------------------------|
| `IO.read_file`                   | - `file_path` (str): The path to the file to read.       | `str`   | Reads a file from the specified path and returns its content as a string. |
| `IO.write_file`                  | - `file_path` (str): The path to the file to write to.   | `None`  | Writes the given content to the specified file.                           |
|                                  | - `content` (str): The content to write to the file.     |         |                                                                           |
| `IO.create_folder_if_not_exists` | - `folder_path` (str): The path to the folder to create. | `None`  | Creates a folder at the specified path if it does not already exist.      |

## Decorators

For use decorators you need to import them from the package:

```python
import nix.utils.decorators as decorators
```

| Decorator         | Arguments                                                                                                                                                                                                                                             | Description                                                                                                                                                                                                                                                                                                                                                     |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| @retry            | - `max_retries` (int, default=3) <br> - `delay` (int, default=2) <br> - `exceptions` (Exception or tuple of Exceptions, default=Exception) <br> - `backoff_factor` (int, default=1) <br> - `logger` (Logger, optional)                                | A decorator that retries a function upon failure. You can customize the maximum number of retries, the delay between retries, the type of exceptions to catch, and the backoff factor to increase the delay with each retry. If a logger is provided, exceptions are logged.                                                                                    |
| @thread_pool      | - `num_threads` (int, default=4) <br> - `exceptions` (Exception or tuple of Exceptions, default=Exception) <br> - `raise_first_exception` (bool, default=False) <br> - `logger` (Logger, optional)                                                    | A decorator that runs a function in a thread pool with a specified number of threads. It collects results from all tasks and returns them as a list. It also handles exceptions, with an option to re-raise the first exception or just log it.                                                                                                                 |
| @handle_exception | - `handler` (Callable[[Exception], Any], optional) <br> - `exceptions` (Exception or tuple of Exceptions, default=Exception) <br> - `default_value` (Any, optional) <br> - `raise_exception` (bool, default=False) <br> - `logger` (Logger, optional) | A decorator for handling exceptions in a function. You can specify a custom exception handler, the type of exceptions to catch, a default return value if exceptions occur, and whether to re-raise exceptions. Logging is optional and can be controlled with a logger. It also supports additional arguments and keyword arguments for the exception handler. |

## Licence

This project is licensed under the MIT License. See the LICENSE file for more details.