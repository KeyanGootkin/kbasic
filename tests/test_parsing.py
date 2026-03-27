"""test the parsing part of kbasic"""
# pylint: skip-file
import os
import os.path
import pathlib
import pytest
from kbasic.parsing.utils import ensure_path, could_be_path
from kbasic.parsing.basic import File, Folder, Path

# a path that already exists
REAL_PATH = __file__
# a path that doesn't exist
NOT_PATH = "/".join(__file__.split('/')[:-1]+["output"])
# a path we can't make
BAD_PATH = "/Users/bernie/nuclear_codes"
TEST_PATHS = [REAL_PATH, BAD_PATH, NOT_PATH]
# a string that can't be interpreted as a path
RANDOM_STR = "the 1% are stealing my gpus >:("

def test_utils():
    """testing the utils file"""
    # could_be_path
    assert could_be_path(REAL_PATH)
    assert could_be_path(NOT_PATH)
    assert not could_be_path(BAD_PATH)
    assert not could_be_path(RANDOM_STR)
    # ensure path
    os.system(f"rm -r {NOT_PATH}")
    assert not os.path.exists(NOT_PATH)
    ensure_path(NOT_PATH)
    assert os.path.exists(NOT_PATH)
    os.system(f'rm -r {NOT_PATH}')
    assert not os.path.exists(NOT_PATH)

def test_basic():
    """testing the basic object"""
    # do we correctly parse things
    ensure_path(NOT_PATH)
    fo = Path(NOT_PATH)
    # since the path exists and is a directory,
    # Path should return a Folder object
    assert type(fo)==Folder
    p = fo / "test.txt"
    assert type(p)==type(pathlib.Path(os.path.expanduser('~')))
    p.touch()
    fi = fo / "test.txt"
    assert type(fi)==File, f"{type(fi)}"
    # test File inits cleanly
    assert fi.parent.path == fo.path
    assert fi.title == 'test'
    assert fi.extension == '.txt'
    assert not fi.loaded
    assert fi.writable
    assert fi.lines == []
    # test file writing
    fi.write("test line")
    # make sure File.lines updates
    assert fi.lines == ["test line"]
    new_file = File(fo.path+'/test.txt')
    new_file.load()
    # make sure a new File object at the same address reads the same thing
    assert new_file.lines == fi.lines
    new_file.write("second line from new file object")
    # File.write updates the object you write from but not others
    assert new_file.lines != fi.lines
    # test File.copy
    fi2 = fi.copy()
    assert fi2.title == fi.title + "-copy"
    fi.load()
    fi2.load()
    assert fi.lines == fi2.lines
    # test File.move by using it to rename the file
    fi.move(str(fo / "original_test_file.txt"))
    assert fi.title == "original_test_file"
    # test master functionality
    fi2.master = fi
    assert fi2.master == fi
    fi2.write('third line that should be thrown away soon')
    assert fi2.lines != fi.lines
    fi2.update()
    assert fi2.lines == fi.lines
