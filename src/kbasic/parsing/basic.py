"""
the bulk of kbasics path logic lives here. File and Folder will both work for anything that accepts
an os.PathLike argument, such as the builtin open function.
"""
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                                    Imports                                     <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from os import remove, system
from os.path import split, splitext, splitroot, exists, isdir, isfile, abspath, expanduser,\
    expandvars
from shutil import copy, move, copytree, rmtree
from typing import Self, Optional
from glob import glob
from pathlib import Path as builtinPath
from kbasic.parsing.utils import ensure_path
from kbasic.user_input import yesno
from kbasic.strings import cyan
from kbasic.typing import Array

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                           Definitions                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
unreadable_file_types: list[str] = ['.gz', '.tar', '.zip']

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Classes                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
class File:
    def __init__(
        self, path: str | Self,
        master: Optional[Self] = None, verbose: bool = False
    ) -> None:
        """A convenience class to deal with file io

        Args:
            path (str): the location of the file.
            master (str, optional): the path to the template to restore this file 
                                    from if necessary. Defaults to None.
            verbose (bool, optional): should this file be annoying. Defaults to 
                                        False.
        """
        self.loaded: bool = False
        if path is None: return None
        if type(path)==type(self):
            self.path = path.path
        else:
            self.path: str = abspath(expandvars(expanduser(path)))
        self.master = File(master)
        self.verbose = verbose
        parentpath, self.name = split(self.path)
        self.title, self.extension = splitext(self.name)
        self.drive, self.root, _ = splitroot(self.path)
        self.parent = Folder(parentpath)
        self.lines = []
    def __repr__(self) -> str: return self.path
    def __str__(self) -> str: return self.path
    def __eq__(self, other) -> bool:
        if type(other) != File: return False
        return (self.path == other.path) & (self.lines == other.lines)
    def __add__(self, other):
        match other:
            case list():
                other.append(self)
                return other
            case File(): return [self, other]
            case _:
                raise NotImplementedError(
                f"can't add object of type: {type(other)} to a Folder object: {repr(self)}"
                )
    def __radd__(self, other):
        if other==0: return self
        return self.__add__(other)
    def __fspath__(self) -> str: return self.path
    @property
    def exists(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        return exists(self.path)
    @property
    def writable(self) -> bool:
        """whether or not we can write this type of file with this object"""
        return self.extension not in unreadable_file_types
    def copy(self, destination: Optional[str] = None):
        """_summary_

        Args:
            destination (str): _description_
        """
        if destination is None:
            destination = str(self.parent / f"{self.title}-copy{self.extension}")
        copy(self.path, destination)
        return File(destination, verbose=self.verbose, master=self)
    def move(self, destination:str):
        """_summary_

        Args:
            destination (str): _description_
        """
        if self.verbose: print(cyan(f'moving {self.path} to {destination}...'))
        move(self.path, destination)
        self.__init__(destination, master=self.master)
    def update(self) -> None: # think of a better name for this function
        """_summary_
        """
        if self.verbose: print(cyan(f'updating {self.name}...'))
        assert self.master is not None, "No master copy to update from."
        if self.exists: self.delete(interactive=False)
        self.master.copy(self.path)
        self.__init__(self.path, master=self.master)
    def delete(self, interactive=True) -> None:
        """summary"""
        if interactive and not yesno(
            f"Are you sure you want to permanently delete {self.path} and all of its contents?\n"
            ):
            return None
        remove(self.path)
    def read(self) -> None:
        """summary"""
        if not self.exists or self.extension in unreadable_file_types: return []
        with open(self.path, 'r') as file:
            self.lines = [f.strip('\n') for f in file.readlines()]
            if self.lines==['']: self.lines = []
        self.loaded = True
    def load(self) -> None:
        """docstring"""
        self.read()
    def save(self, interactive=True) -> None:
        """summary"""
        if interactive and not yesno(
            f"Are you sure you want to permanently overwrite {self.path}?\n"
            ):
            return None
        with open(self.path, 'w+') as file:
            if not self.writable:
                raise PermissionError(
                    f"attempted to save unwritable file: {self.path}"
                    )
            if len(self.lines) > 0: file.writelines("\n".join(self.lines))
            return None
    def write(self, text: str | Array, interactive=False) -> None:
        """add text to this File.lines then save the file"""
        match text:
            case str():
                self.lines.append(text)
            case _ if type(text) in Array.types:
                self.lines += list(text)
            case _:
                raise TypeError(f"""
                    must supply either string or an array of strings
                    was given text of type: {type(text)}
                """)
        self.save(interactive=interactive)
    def touch(self) -> None:
        """summary"""
        system(f"touch {self.path}")

class Folder:
    def __init__(
        self, path: str|Self,
        master: Optional[Self] = None
    ) -> None:
        if path is None: return None
        if type(path)==type(self):
            path = path.path
        self.path = abspath(expandvars(expanduser(path)))
        self.master = master if not isinstance(master, str) else Folder(master)
        self.parentpath, self.name = split(self.path)
    def __repr__(self) -> str: return self.path
    def __str__(self) -> str: return self.path
    def __len__(self) -> int: return len(self.children)
    def __iter__(self):
        self.index = 0
        return self
    def __next__(self):
        if self.index < len(self):
            i = self.index
            self.index += 1
            return self.children[i]
        raise StopIteration
    def __add__(self, other):
        match other:
            case str():
                return Path(f"{self.path}/{other}")
            case File():
                return self.children+[other]
            case Folder():
                return self.children + other.children
            case list():
                return self.children + other
            case _:
                raise NotImplementedError(
                    f"can't add object of type: {type(other)} to a Folder object: {repr(self)}"
                    )
    def __radd__(self, other):
        if other==0: return [self]
        return self.__add__(other)
    def __truediv__(self, other):
        match other:
            case str(): return Path(f"{self.path}/{other}")
    def __fspath__(self) -> str: return self.path
    @property
    def parent(self) -> Self:
        """summary"""
        return Folder(self.parentpath) if len(self.parentpath) > 3 else None
    @property
    def exists(self) -> bool:
        """summary"""
        return exists(self.path)
    def glob(self, pattern: str, recursive=True):
        """summary"""
        return glob(self.path+'/'+pattern, recursive=recursive)
    @property
    def children(self) -> list:
        """summary"""
        return [Path(p) for p in self.glob("*")]
    def ls(self) -> None:
        """summary"""
        print("\n".join([p.path for p in self.children]))
    def make(self) -> None:
        """summary"""
        ensure_path(self.path)
    def copy(self, destination:str) -> None:
        """summary"""
        if destination is None: destination = str(self.parent / f"{self.name}-copy")
        copytree(self.path, destination)
        return File(destination, verbose=self.verbose, master=self)
    def revert(self) -> None:
        """summary"""
        assert self.master is not None, "No master copy to update from."
        if self.exists: self.delete(interactive=False)
        self.master.copy(self.path)
        self = Folder(self.path, master=self.master)
    def delete(self, interactive=True) -> None:
        """summary"""
        if interactive and not yesno(
            f"Are you sure you want to permanently delete {self.path} and all of its contents?\n"
            ):
            return None
        rmtree(self.path)

class Path:
    """
    A constructor to return either a kbasic.Folder, kbasic.File, or a pathlib.Path.
    """
    def __new__(cls, path: str, *args, **kwds):
        if isdir(path): return Folder(path, *args, **kwds)
        if isfile(path): return File(path, *args, **kwds)
        return builtinPath(path)
