# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from fractions import Fraction
import warnings 
# Syntax warnings show up everytime you \something so we ignore all of em, hope this doesn't fuck anything up!
warnings.filterwarnings(action='ignore', category=SyntaxWarning)
from pylatexenc.latex2text import LatexNodes2Text

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                           Definitions                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
l2t = LatexNodes2Text().latex_to_text

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Functions                            <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def texfraction(num) -> str: 
    f = Fraction(str(num))
    return r"$\frac{" + str(f.numerator) + "}{" + str(f.denominator) + r"}$"

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Classes                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
class Tex(str):
    def __init__(self, x: str) -> None:
        x = x.strip(' $')
        if x[-1]=='\n': x = x[:-1]
        if x[-2:]=='.0': x = x[:-2]
        # replace wonky \ letter commands with raw versions
        # WARNING: DOES NOT WORK WITH \U OR \X BECAUSE THESE ARE UNICODE THINGS AND IDK HOW TO OVERRIDE THAT BEHAVIOR
        x = x.replace("\a", r"\a").replace("\b", r"\b").replace("\f", r"\f").replace("\n", r"\n").replace("\r", r"\r").replace("\t", r"\t").replace("\v", r"\v")
        # make compatible with fstring
        x = x.replace("[", "{").replace("]", "}")
        # get rid of extraneous .0's 
        x = x.replace(".0 ", " ").replace(".0}", "}").replace(".0$", "$").replace(".0\n", "\n")
        self.string = fr"{l2t(x)}"
        self.wrap = "$"+self.string+"$"

    def __repr__(self) -> str: return self.string.strip("$")
    def __str__(self) -> str: return self.string
