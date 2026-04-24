"""test the parsing part of kbasic"""
# pylint: skip-file
import sys
import os
import os.path
import pathlib
import pytest
import tempfile
from glob import glob
from kbasic.parsing.utils import ensure_path, could_be_path
from kbasic.parsing.basic import File, Folder, Path
from kbasic.user_input import simulate_user_input

# a path that already exists
REAL_PATH = __file__
# a path that doesn't exist
OUT_PATH = "/".join(__file__.split('/')[:-1]+["output"])
output = Folder(OUT_PATH)
# a path we can't make
BAD_PATH = "/Users/bernie/nuclear_codes"
TEST_PATHS = [REAL_PATH, BAD_PATH, OUT_PATH]
# a string that can't be interpreted as a path
RANDOM_STR = "the 1% are stealing my gpus >:("

def test_utils():
    """testing the utils file"""
    # could_be_path
    assert could_be_path(REAL_PATH)
    assert could_be_path(OUT_PATH)
    assert not could_be_path(BAD_PATH)
    assert not could_be_path(RANDOM_STR)
    # ensure path
    os.system(f"rm -r {OUT_PATH}")
    assert not os.path.exists(OUT_PATH)
    ensure_path(OUT_PATH)
    assert os.path.exists(OUT_PATH)

def test_File():
    # !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
    # File Basics
    # !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
    """testing the basic objects"""
    f = File(OUT_PATH+'/example.txt', verbose=True)
    assert not f.exists
    f.touch()
    assert f.exists
    f_same = File(f) # should work
    assert repr(f) == f.path
    assert str(f)=='' # loads file
    assert f.loaded and f.lines==[]
    # file add
    assert f + [] == [f]
    assert [] + f == [f]
    f2 = File(OUT_PATH+'/example2')
    assert f + f2 == [f, f2]
    with pytest.raises(NotImplementedError): assert f + 2
    assert sum((f, f2))==[f,f2]
    # test interactive mode
    with simulate_user_input('n', 'n'):
        f.lines.append('hi')
        f.save()
        f.delete()
    # do not save unwritable files
    with pytest.raises(PermissionError): 
        z = File('x.zip')
        z.write(['h', 'i'])
        z.save(interactive=False)
    with pytest.raises(TypeError): z.write(2)
    f3 = f.copy()
    assert f3.title==f.title+'-copy'
    f3.move(f3.parent / "example3.txt")
    assert f3.title=='example3'
    # update f3
    f.write('written in example.txt')
    f3.master = f
    f3.update()
    f3.load()
    assert 'written in example.txt' in f3.lines
    assert f != f3
    assert f != 2
    fagain = output / "example.txt"
    fagain.load()
    assert f == fagain

def test_Folder():
    # !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
    # Folder Basics
    # !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
    assert output.parent.path == Folder('./tests').path
    output_again = Folder(output)
    example = output / "example.txt"
    example3 = output / "example3.txt"
    assert example.exists and example3.exists
    for fi in output: 
        assert fi in [example, example3]
    f4 = File(output.path+'/example4.txt')
    f4.touch() # so Path recognizes it as a file
    assert output + '/example4.txt' == f4
    assert output + f4 == output.children + [f4]
    assert output + [output/'example4.txt',] == output.children + [f4]
    for pa in [
        Path(pi) for pi in glob('./tests/output/*')+glob('./src/kbasic/*') if os.path.isfile(pi)
        ]:
        assert pa in output+Folder('./src/kbasic')
    with pytest.raises(NotImplementedError): assert output + 2
    assert sum([output, example])==[output, example]
    # check ls
    orig = sys.stdout
    ls_output_file = File(output / "ls_output.txt")
    ls_output_file.touch()
    sys.stdout = open(ls_output_file.path, 'a+')
    output.ls()
    sys.stdout = orig
    ls_output_file.read() # read the output of ls
    assert ls_output_file.lines == output.glob('*')

    

#     # with open(out.path, 'a+') as outfile:
#     #     orig = sys.stdout
#     #     sys.stdout = outfile
#     #     f.ls()
#     #     sys.stdout = orig
#     # addition
#     assert f + 'example.txt' == Path(f.path+'/example.txt')
#     assert f + File('/x') == f.children+['/x']
#     assert f + [2, 1] == f.children + [2, 1]
#     with pytest.raises(NotImplementedError): assert f + 2

# def test_parse():
#     # !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
#     # Parsing Paths
#     # !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
#     ensure_path(OUT_PATH)
#     fo = Path(OUT_PATH)
#     fo_again = Folder(fo) # this is valid too
#     # since the path exists and is a directory,
#     # Path should return a Folder object
#     assert type(fo)==Folder
#     p = fo / "test.txt"
#     assert type(p)==type(pathlib.Path(os.path.expanduser('~')))
#     p.touch()
#     fi = fo / "test.txt"
#     assert type(fi)==File, f"{type(fi)}"
#     # test File inits cleanly
#     assert fi.parent.path == fo.path
#     assert fi.title == 'test'
#     assert fi.extension == '.txt'
#     assert not fi.loaded
#     assert fi.writable
#     assert fi.lines == []
#     # test file writing
#     fi.write("test line")
#     # make sure File.lines updates
#     assert fi.lines == ["test line"]
#     new_file = File(fo.path+'/test.txt')
#     new_file.load()
#     # make sure a new File object at the same address reads the same thing
#     assert new_file.lines == fi.lines
#     new_file.write("second line from new file object")
#     # File.write updates the object you write from but not others
#     assert new_file.lines != fi.lines
#     # test File.copy
#     fi2 = fi.copy()
#     assert fi2.title == fi.title + "-copy"
#     fi.load()
#     fi2.load()
#     assert fi.lines == fi2.lines
#     # test File.move by using it to rename the file
#     fi.move(str(fo / "original_test_file.txt"))
#     assert fi.title == "original_test_file"
#     # test master functionality
#     fi2.master = fi
#     assert fi2.master == fi
#     fi2.write('third line that should be thrown away soon')
#     assert fi2.lines != fi.lines
#     fi2.update()
#     assert fi2.lines == fi.lines
