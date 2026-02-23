# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
#pysim imports
from kbasic.user_input import yesno
#nonpysim imports
import numpy as np
from glob import glob 
from shutil import copy, move, copytree, rmtree
from os.path import isdir, isfile, exists, abspath
from os import mkdir, remove
from functools import cached_property
import tomllib

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                           Definitions                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
unreadable_file_types = ['gz', 'tar', 'zip']

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Functions                            <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def ensure_path(path: str) -> None:
    """make sure that a path exists

    Args:
        path (str): the path you want to exist
    """
    parts = abspath(path).strip().split('/')[1:]
    for i in range(len(parts)+1):
        pi = "/"+"/".join(parts[:i])
        if pi in "/home/x-kgootkin/": continue
        if not exists(pi):
            mkdir(pi)
def could_be_path(path: str) -> bool: return isdir('/'.join(path.split('/')[:2])) 

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Classes                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
class File:
    def __init__(self, path:str, master=None, executable:bool=False, verbose:bool=False) -> None:
        """A convenience class to deal with file io

        Args:
            path (str): the location of the file.
            master (str, optional): the path to the template to restore this file from if necessary. Defaults to None.
            executable (bool, optional): is this file an executable. Defaults to False.
            verbose (bool, optional): should this file be annoying. Defaults to False.
        """
        self.path: str = abspath(path.replace("\\", "/").replace('//', '/'))
        pathlist: list[str] = self.path.split("/")
        self.parent = Folder("/".join(pathlist[:-1]))
        self.grandparent = Folder("/".join(pathlist[:-2])) if len(pathlist)>3 else None
        self.greatgrandparent = Folder("/".join(pathlist[:-3])) if len(pathlist)>4 else None
        self.name = self.path.split("/")[-1]
        self.extension = self.name.split(".")[-1] if "." in self.name else None
        self.master = master if not isinstance(master, str) else File(master)
        self.executable = executable
        self.verbose = verbose
    def __repr__(self) -> str: return self.path
    def __str__(self) -> str: return "\n".join(self.lines)
    def __add__(self, other):
        match other: 
            case list():
                other.append(self)
                return other
            case File(): return [self, other]
             
            case _: raise NotImplementedError(f"can't add object of type: {type(other)} to a Folder object: {repr(self)}")
    def __radd__(self, other):
        if other==0: return self 
        return self.__add__(other)
    @property
    def exists(self) -> bool: return exists(self.path)
    def copy(self, destination:str): copy(self.path, destination)
    def move(self, destination:str): 
        move(self.path, destination)
        self = File.__init__(destination, master=self.master, executable=self.executable)
    def update(self) -> None:
        if self.verbose: print(f'updating {self.name}...')
        assert self.master is not None, "No master copy to update from."
        if self.exists: self.delete(interactive=False)
        self.master.copy(self.path)
        self = File(self.path, master=self.master)
    def delete(self, interactive=True) -> None:
        if interactive and not yesno(f"Are you sure you want to permanently delete {self.path} and all of its contents?\n"): return None
        else: remove(self.path)     
    def read(self) -> None: 
        if not self.exists: return []
        with open(self.path, 'r') as file: 
            self.lines = [f.strip('\n') for f in file.readlines()]   
    def save(self, interactive=True):
        if interactive and not yesno(f"Are you sure you want to permanently overwrite {self.path}?\n"):
            return None
        with open(self.path, 'w+') as file:
            if not file.writable: raise PermissionError(f"attempted to save unwritable file: {self.path}")
            file.writelines("\n".join(self.lines))
class TOML(File):
    def __init__(self, path: str, verbose: bool = False):
        File.__init__(self, path, verbose=verbose)
    def read(self):
        self.__dict__ |= tomllib.load(open(self.path, 'rb'))
class Folder:
    def __init__(self, path:str, master=None) -> None:
        self.path = '/' if path=='' else abspath(path.replace("\\", "/").replace('//', '/'))
        self.name = self.path.split("/")[-1] if len(self.path.split('/')[-1])>0 else self.path.split("/")[-2]
        self.master = master if not isinstance(master, str) else Folder(master)
    def __repr__(self) -> str: return self.path
    def __len__(self) -> int: return len(self.children)
    def __iter__(self):
        self.index = 0 
        return self
    def __next__(self):
        if self.index < len(self):
            i = self.index 
            self.index += 1 
            return Folder(self.children[i]) if isdir(self.children[i]) else File(self.children[i])
        else: raise StopIteration
    def __add__(self, other):
        match other:
            case str():
                p = f"{self.path}/{other}"
                return Folder(p) if isdir(p) else File(p) if isfile(p) else None
            case File(): return self.children+[other]
            case Folder(): return self.children + other.children
            case list(): return self.children + other
            case _: raise NotImplementedError(f"can't add object of type: {type(other)} to a Folder object: {repr(self)}")
    def __radd__(self, other):
        if other==0: return [self]
        return self.__add__(other)
    @property
    def exists(self) -> bool: return exists(self.path)
    @property
    def children(self) -> list: return glob(self.path+"/*" if self.path!='/' else "/*")
    def ls(self) -> None: print("\n".join(self.children))
    def make(self) -> None: ensure_path(self.path)
    def copy(self, destination:str) -> None: copytree(self.path, destination)
    def revert(self) -> None:
        assert self.master is not None, "No master copy to update from."
        if self.exists: self.delete(interactive=False)
        self.master.copy(self.path)
        self = Folder(self.path, master=self.master)
    def delete(self, interactive=True) -> None:
        if interactive and not yesno(f"Are you sure you want to permanently delete {self.path} and all of its contents?\n"): 
            return None
        rmtree(self.path)

def parse(path: str | list[str]) -> Folder | File:
    """take a path or list of paths and turn them into Folder or File objects as appropriate.

    Args:
        path (str | list[str]): the path you want to be a File/Folder object

    Raises:
        FileNotFoundError: if you can't match path

    Returns:
        Folder | File: path as a Folder/File.
    """
    match path:
        case str():
            if isdir(path): return Folder(path)
            if isfile(path): 
                return TOML(path) if path.split('.')[-1]=='toml' else File(path)
        case list()|np.ndarray():
            return [Folder(p) if isdir(p) else File(p) if isfile(p) else None for p in path]
    raise FileNotFoundError(f"Unable to parse path(s): {path}")