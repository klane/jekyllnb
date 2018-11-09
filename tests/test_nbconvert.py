import os
import pytest
from difflib import Differ
from nbconvert.nbconvertapp import NbConvertApp
from pprint import pprint


FILE_NAME = 'hello-world'
SITE_DIR = 'docs'
OUTPUT_DIR = '_pages'
IMAGE_DIR = os.path.join('assets', 'images', FILE_NAME)

@pytest.fixture
def site_dir(tmpdir):
    return tmpdir.join(SITE_DIR, OUTPUT_DIR)

@pytest.fixture
def image_dir(site_dir):
    return site_dir.join(IMAGE_DIR)

@pytest.fixture
def nbconvert_file(site_dir):
    NbConvertApp.launch_instance([
        '--to', 'jekyll',
        '--output-dir', site_dir.strpath,
        '--NbConvertApp.output_files_dir=' + IMAGE_DIR,
        os.path.join(os.path.dirname(__file__), 'resources', FILE_NAME + '.ipynb')
    ])

    yield site_dir.join(FILE_NAME + '.md')
    NbConvertApp.clear_instance()

def test_nbconvert_file_exists(nbconvert_file):
    assert nbconvert_file.check()

def test_nbconvert_image_exists(nbconvert_file, image_dir):
    assert os.path.isdir(image_dir.strpath)
    assert os.path.isfile(image_dir.join(FILE_NAME + '_4_0.png').strpath)

def test_nbconvert_file_contents(nbconvert_file):
    test_lines = nbconvert_file.readlines()
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
