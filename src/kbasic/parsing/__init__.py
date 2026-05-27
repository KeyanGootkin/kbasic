"""
kbasic.parsing is a module designed to deal with i/o in an object oriented way.
"""
from kbasic.parsing.utils import could_be_path, ensure_path
from kbasic.parsing.basic import File, Folder, Path
from kbasic.parsing.parser import parse
from kbasic.parsing.logging import configure_log
