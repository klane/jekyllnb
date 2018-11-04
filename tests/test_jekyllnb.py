import os
import pytest
from difflib import Differ
from jekyllnb.jekyllnb import jekyllpath
from nbconvert.nbconvertapp import NbConvertApp
from pprint import pprint


FILE_NAME = 'hello-world'
IMG_DIR = os.path.join('assets', 'images', FILE_NAME)

@pytest.fixture
def test_file(tmpdir):
    test_file_name = tmpdir.join(FILE_NAME + '.md')

    NbConvertApp.launch_instance(['--to', 'jekyll', '--output-dir', test_file_name.dirname,
        '--NbConvertApp.output_files_dir=' + IMG_DIR,
        os.path.join(os.path.dirname(__file__), 'resources', FILE_NAME + '.ipynb')])

    return test_file_name

def test_file_exists(test_file):
    img_dir = os.path.join(test_file.dirname, IMG_DIR)

    assert test_file.check()
    assert os.path.isdir(img_dir)
    assert os.path.isfile(os.path.join(img_dir, FILE_NAME + '_3_0.png'))

def test_jekyllnb(test_file):
    test_lines = test_file.readlines()
    target_file = os.path.join(os.path.dirname(__file__), 'resources', FILE_NAME + '.md')

    with open(target_file) as target:
        target_lines = target.readlines()

    try:
        assert all(a == b for a, b in zip(test_lines, target_lines))
    except AssertionError:
        differ = Differ()
        diff = differ.compare(test_lines, target_lines)
        pprint(list(diff))
        raise

def test_jekyllpath():
    assert jekyllpath('assets\\images') == '{{ site.baseurl }}/assets/images'
