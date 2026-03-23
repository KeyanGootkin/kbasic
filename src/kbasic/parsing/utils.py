"""basic utility functions for kbasic.parsing, mostly from os.path"""
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from os import system
from os.path import isdir

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Functions                            <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def ensure_path(path: str) -> None:
    """make sure that a path exists

    Args:
        path (str): the path you ant to exist
    """
    system(f"mkdir -p {path}")
def could_be_path(path: str) -> bool:
    """determine if this is anywhere close to a valid path

    Args:
        path (str): the path (?) to check

    Returns:
        bool: True if the first two members of the path are valid else False.
    """
    return isdir('/'.join(path.split('/')[:3]))
