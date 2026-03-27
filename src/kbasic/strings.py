# pylint: skip-file
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from colorist import ColorOKLCH

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                           Definitions                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
ansi = {"BLACK": u"\033[0;30m","RED": u"\x1b[0;31m","GREEN": u"\033[0;32m","YELLOW": u"\033[0;33m","BLUE": u"\033[0;34m","PURPLE": u"\033[0;35m","CYAN": u"\033[0;36m","WHITE": u"\033[0;37m",
    "BOLD": u"\033[1m","BOLD BLACK": u"\033[1;30m","BOLD RED": u"\x1b[1;31m","BOLD GREEN": u"\033[1;32m","BOLD YELLOW": u"\033[1;33m","BOLD BLUE": u"\033[1;34m","BOLD PURPLE": u"\033[1;35m","BOLD CYAN": u"\033[1;36m","BOLD WHITE": u"\033[1;37m",
    "ITALIC": u"\033[3m","ITALIC BLACK": u"\033[3;30m","ITALIC RED": u"\x1b[3;31m","ITALIC GREEN": u"\033[3;32m","ITALIC YELLOW": u"\033[3;33m","ITALIC BLUE": u"\033[3;34m","ITALIC PURPLE": u"\033[3;35m","ITALIC CYAN": u"\033[3;36m","ITALIC WHITE": u"\033[3;37m",
    "UNDERLINE": u"\033[4m","UNDERLINE BLACK": u"\033[4;30m","UNDERLINE RED": u"\x1b[4;31m","UNDERLINE GREEN": u"\033[4;32m","UNDERLINE YELLOW": u"\033[4;33m","UNDERLINE BLUE": u"\033[4;34m","UNDERLINE PURPLE": u"\033[4;35m","UNDERLINE CYAN": u"\033[4;36m","UNDERLINE WHITE": u"\033[4;37m",
    "BLINK": u"\033[5m","BLINK BLACK": u"\033[5;30m","BLINK RED": u"\x1b[5;31m","BLINK GREEN": u"\033[5;32m","BLINK YELLOW": u"\033[5;33m","BLINK BLUE": u"\033[5;34m","BLINK PURPLE": u"\033[5;35m","BLINK CYAN": u"\033[5;36m","BLINK WHITE": u"\033[5;37m",
    "NEGATIVE": u"\033[7m","BLACK BACKGROUND": u"\033[7;30m","RED BACKGROUND": u"\x1b[7;31m","GREEN BACKGROUND": u"\033[7;32m","YELLOW BACKGROUND": u"\033[7;33m","BLUE BACKGROUND": u"\033[7;34m","PURPLE BACKGROUND": u"\033[7;35m","CYAN BACKGROUND": u"\033[7;36m","WHITE BACKGROUND": u"\033[7;37m",
    "END": u"\033[0m"
}
rgb_string = lambda x, r, g, b: f"\x1b[38;2;{r};{g};{b}m {x} \x1b[0m"
lch_string = lambda x, l, c, h: f"{ColorOKLCH(l, c, h).generate_ansi_code()}{x}\x1b[0m"
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Functions                            <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def color_string(text: str, color: str = 'white', option: str = '') -> str:
    match option.lower():
        case '': fmt = ansi[color.upper()] 
        case 'bold': fmt = ansi[f"BOLD {color.upper()}"]
        case 'negative'|'background': fmt = ansi[f"{color.upper()} BACKGROUND"]
        case 'italic'|'italics'|'cursive': fmt = ansi[f"ITALIC {color.upper()}"]
        case 'underline': fmt = ansi[f'UNDERLINE {color.upper()}']
        case 'blink'|'blinking': fmt = ansi[f"BLINK {color.upper()}"]
    return fmt + text + ansi['END']
def black(text: str, option: str = '') -> str:
    return color_string(text, 'black', option)
def red(text: str, option: str = '') -> str:
    return color_string(text, 'red', option)
def green(text: str, option: str = '') -> str:
    return color_string(text, 'green', option)
def yellow(text: str, option: str = '') -> str:
    return color_string(text, 'yellow', option)
def blue(text: str, option: str = '') -> str:
    return color_string(text, 'blue', option)
def purple(text: str, option: str = '') -> str:
    return color_string(text, 'purple', option)
def cyan(text: str, option: str = '') -> str:
    return color_string(text, 'cyan', option)
def italic(text: str, color: str = 'white') -> str:
    return color_string(text, color, 'italic')
def bold(text: str, color: str = 'white') -> str:
    return color_string(text, color, 'bold')
def blink(text: str, color: str = 'white') -> str:
    return color_string(text, color, 'blink')
def underline(text: str, color: str = 'white') -> str:
    return color_string(text, color, 'underline')
def negative(text: str, color: str = 'white') -> str:
    return color_string(text, color, 'negative')
