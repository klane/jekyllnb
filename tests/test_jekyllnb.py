import filecmp
import os
import pytest
from difflib import Differ
from jekyllnb.jekyllnb import jekyllpath
from nbconvert.nbconvertapp import NbConvertApp
from pprint import pprint


FILE_NAME = 'hello-world'

@pytest.fixture
def test_file(tmpdir):
    test_file_name = tmpdir.join(FILE_NAME + '.md')

    NbConvertApp.launch_instance(['--to', 'jekyll', '--output-dir', test_file_name.dirname,
        os.path.join(os.path.dirname(__file__), 'resources', FILE_NAME + '.ipynb')])

    contents = test_file_name.read()

    with open(test_file_name.strpath, 'w', newline='\n') as f:
        f.write(contents)

    return test_file_name

def test_file_exists(test_file):
    assert test_file.check()

#TODO ignore whitespace in comparison or remove it after print statement in conversion
def test_jekyllnb(test_file):
    target_file = os.path.join(os.path.dirname(__file__), 'resources', FILE_NAME + '.md')

    try:
        assert filecmp.cmp(test_file, target_file, shallow=False)
    except AssertionError:
        with open(target_file) as target:
            differ = Differ()
            diff = differ.compare(test_file.readlines(), target.readlines())
            pprint(list(diff))
            raise

def test_jekyllpath():
    assert jekyllpath('assets\\images') == '{{ site.baseurl }}/assets/images'
