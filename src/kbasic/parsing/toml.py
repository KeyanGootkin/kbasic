"""implement a toml class that loads the variables into its __dict__"""
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from tomllib import load as tomlload
from kbasic.parsing.basic import File

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Classes                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
class TOML(File):
    def __init__(
        self, path: str, 
        verbose: bool = False
    ) -> None:
        File.__init__(self, path, verbose=verbose)
        if self.exists: self.read()
    def read(self):
        """summary"""
        self.loaded = True
        with open(self.path, 'rb') as f:
            self._attrs = tomlload(f)
        self.__dict__ |= self._attrs
        self.lines = [f"{k}={v}" for k,v in self._attrs.items()]
