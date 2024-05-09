from pathlib import Path
from pydbml import PyDBML
from helper.design import Borg

class DBMLDiagramParser(Borg):
    """
    A parser class for DBML (Database Markup Language) files that implements the Borg design pattern
    to share state across instances. It provides functionality to validate file extensions, read file content,
    parse DBML content, and maintain a cache of parsed files to avoid redundant processing.

    Attributes
    ----------
    cache : dict
        A dictionary to cache parsed DBML files. The keys are file paths and the values are the parsed PyDBML objects.

    Methods
    -------
    validate_file_extension(file_path: str)
        Validates that the file at `file_path` has a .dbml extension.

    read_file_content(file_path: str) -> str
        Reads and returns the content of the file at `file_path`.

    parse_dbml_content(content: str) -> PyDBML
        Parses the given DBML content string and returns a PyDBML object.

    read_diagram(file_path: str) -> PyDBML
        Orchestrates the process of reading and parsing a DBML file, including validation and caching.

    Raises
    ------
    ValueError
        If the file does not have a .dbml extension.
    FileNotFoundError
        If the file does not exist at the specified `file_path`.
    """

    def __init__(self):
        """
        Initializes the DBMLDiagramParser instance, setting up the shared cache for parsed files.
        """
        super().__init__()
        self.cache = {}

    def validate_file_extension(self, file_path: str):
        """
        Validates that the specified file has a .dbml extension.

        Parameters
        ----------
        file_path : str
            The path to the file to validate.

        Raises
        ------
        ValueError
            If the file extension is not .dbml.
        """
        if not file_path.lower().endswith('.dbml'):
            raise ValueError(f"The file {file_path} is not a DBML file. Please provide a file with a '.dbml' extension.")

    def read_file_content(self, file_path: str) -> str:
        """
        Reads the content of the specified file.

        Parameters
        ----------
        file_path : str
            The path to the file to read.

        Returns
        -------
        str
            The content of the file.

        Raises
        ------
        FileNotFoundError
            If the file does not exist at `file_path`.
        """
        if not Path(file_path).is_file():
            raise FileNotFoundError(f"DBML file not found at {file_path}")
        
        with open(file_path, "r", encoding="UTF-8") as file:
            return file.read()

    def parse_dbml_content(self, content: str) -> PyDBML:
        """
        Parses the provided DBML content string into a PyDBML object.

        Parameters
        ----------
        content : str
            The DBML content string to parse.

        Returns
        -------
        PyDBML
            The parsed PyDBML object.
        """
        return PyDBML(content)

    def read_diagram(self, file_path: str) -> PyDBML:
        """
        Reads and parses a DBML file, using caching to avoid redundant reads and parses. Validates the file extension
        before reading the file content and parsing it.

        Parameters
        ----------
        file_path : str
            The path to the DBML file to read and parse.

        Returns
        -------
        PyDBML
            The parsed PyDBML object from the DBML file.

        Notes
        -----
        This method will use the cached version of the parsed file if it has been read and parsed previously.
        """
        self.validate_file_extension(file_path)

        if file_path in self.cache:
            print(f"Using cached version of {file_path}")
            return self.cache[file_path]

        print(f"Reading file {file_path}")
        content = self.read_file_content(file_path)
        parsed = self.parse_dbml_content(content)
        self.cache[file_path] = parsed

        return parsed

    def __str__(self):
        """
        Returns the string representation of the object.
        """
        return f"DBMLDiagramParser with {len(self.cache)} cached files"

    def __repr__(self):
        """
        Returns the official representation of the object, showing the cached files.
        """
        cache_repr = ', '.join([f"PyDBML: {Path(key).name}" for key in self.cache])
        return f"{self.__class__.__name__}({cache_repr})"

    def __getitem__(self, file_path):
        """
        Allows direct access to the cache using indexing syntax.

        Parameters
        ----------
        file_path : str
            The file path to access in the cache.

        Returns
        -------
        The cached value for the given file path.
        """
        return self.cache[file_path]

    def __setitem__(self, file_path, value):
        """
        Allows setting values in the cache using indexing syntax.

        Parameters
        ----------
        file_path : str
            The file path to set in the cache.
        value : PyDBML
            The value to set in the cache for the given file path.
        """
        self.cache[file_path] = value

    def __contains__(self, file_path):
        """
        Allows using the `in` keyword to check if a file path is in the cache.

        Parameters
        ----------
        file_path : str
            The file path to check in the cache.

        Returns
        -------
        bool
            True if the file path is in the cache, False otherwise.
        """
        return file_path in self.cache
