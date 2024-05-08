import os


class IO:
    """
    A utility class for performing common I/O operations.
    """

    @staticmethod
    def read_file(file_path: str) -> str:
        """
        Reads a file and returns its content as a string.

        Parameters:
        file_path (str): The path to the file to read.

        Returns:
        str: The content of the file.
        """
        with open(file_path, 'r') as file:
            return file.read()

    @staticmethod
    def write_file(file_path: str, content: str) -> None:
        """
        Writes a string to a file.

        Parameters:
        file_path (str): The path to the file to write to.
        content (str): The content to write to the file.
        """
        with open(file_path, 'w') as file:
            file.write(content)

    @staticmethod
    def create_folder_if_not_exists(folder_path: str) -> None:
        """
        Creates a folder if it does not already exist.

        Parameters:
        folder_path (str): The path to the folder to create.
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
