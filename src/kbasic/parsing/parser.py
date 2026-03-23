"""a handler to take a path and deliver the correct object to the user"""
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from os.path import isfile, isdir
from kbasic.typing import Array
from kbasic.parsing.basic import File, Folder
from kbasic.parsing.toml import TOML
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Functions                            <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def parse(path: str | list[str]) -> Folder | File | list[Folder | File]:
    """take a path or list of paths and turn them into Folder or File objects as appropriate.

    Args:
        path (str | list[str]): the path you want to be a File/Folder object

    Raises:
        FileNotFoundError: if you can't match path

    Returns:
        Folder | File | list[Folder|File]: path(s) as a Folder/File.
    """
    match path:
        case str():
            if isdir(path): return Folder(path)
            if isfile(path):
                return TOML(path) if path.split('.')[-1]=='toml' else File(path)
        case _ if type(path) in Array.types:
            return [Folder(p) if isdir(p) else File(p) if isfile(p) else None for p in path]
    raise FileNotFoundError(f"Unable to parse path(s): {path}")
