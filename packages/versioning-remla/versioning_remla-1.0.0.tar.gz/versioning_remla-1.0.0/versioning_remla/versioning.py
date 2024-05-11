""" Utlility class to make this package version-aware"""
from importlib_resources import files


class VersionUtil:
    """Utlility class to make this package version-aware"""
    def get_version(self) -> str:
        """This library is version-aware. This method fetches the current version from the project metadata and returns it.
        Returns:
            str: Returns the version of this library.
        """
        version = files('resources').joinpath('version.txt').read_text()
        return version
