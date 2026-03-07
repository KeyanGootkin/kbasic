# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from kbasic.typing import Number
from kbasic.strings import green, yellow, black
from collections.abc import Iterable
from contextlib import contextmanager
import inspect
from tqdm import tqdm

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                              Types                              <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                           Definitions                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Functions                            <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def bar(
        x: Number, total: Number, 
        width: int = 20, border: str = "|", block: str = "▉", color: str = 'white'
) -> str:
    """create a string representing a progress bar set at 100 * x / total % full.

    Args:
        x (Number): x out of total
        total (_type_): x out of total
        width (int, optional): how many characters wide the bar should be. Defaults to 20.
        border (str, optional): the character to represent the border of the bar. Defaults to "|".
        block (str, optional): the character representing a full part of the bar. Defaults to "▉".

    Returns:
        str: a progress bar
    """
    full = int((x/total) * width // 1)
    empty = width - full
    bar = border + (full-1)*green(block) + yellow(block) + empty*black(block, "faint") + border 
    return bar
@contextmanager
def redirect_to_tqdm():
    """maybe make print statements show up below the bar without fucking everything up?
    idk tbh im not sure how this works exactly I got it from stack exchange.
    """
    # Store builtin print
    old_print = print
    def new_print(*args, **kwargs):
        # If tqdm.tqdm.write raises error, use builtin print
        try:
            tqdm.write(*args, **kwargs)
        except:
            old_print(*args, ** kwargs)

    try:
        # Globaly replace print with new_print
        inspect.builtins.print = new_print
        yield
    finally:
        inspect.builtins.print = old_print
def progress_bar(iterator: Iterable, **kwargs):
    """tqdm with print redirected to tqdm.write
    """
    with redirect_to_tqdm():
        for x in tqdm(iterator, **kwargs):
            yield x
def verbose_bar(iterator: Iterable, verbose: bool, **kwargs):
    """just a progress bar if verbose is true.
    """
    return progress_bar(iterator, **kwargs) if verbose else iterator

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Decorators                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Classes                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
class ProgressBar(tqdm):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.iter = self.initial
    def update(self, iter: int): 
        super().update(n=iter-self.iter)
        self.iter = iter