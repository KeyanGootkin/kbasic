# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from kbasic.typing import Number
from typing import Any

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Functions                            <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def parse_user_input(response: str, sep: str = ',') -> Any:
    try: return Number(response)
    except ValueError: i=0
    match response:
        case str(x) if ',' in x: 
            return tuple(parse_user_input(xi.strip(), sep=sep) for xi in response.split(sep))
        case _: 
            return response.lower().strip()
def yesno(prompt: str):
    """
    prompt the user to either reply yes or no
    :param prompt: the yes/no question to be answered
    :return: True if yes False if no
    """
    response = input(prompt).lower()
    if 'y' in response and not 'n' in response:
        return True
    elif 'n' in response and not 'y' in response:
        return False
    else:
        def retry_yesno():
            retry_prompt = "Sorry I couldn't read that please respond with yes or no\n" + prompt
            retry_response = input(retry_prompt).lower()
            if 'y' in retry_response and not 'n' in retry_response:
                return True
            elif 'n' in retry_response and not 'y' in retry_response:
                return False
            else:
                raise ValueError("need a response with either y or n in it.")

        return retry_yesno()
def interactive_set_attribute(obj: Any, attr: str, default_answer: str = "") -> None:
    res: Any = parse_user_input(input(f"Set a value for {repr(obj)}.{attr}:\n\t"))
    setattr(obj, attr, res)