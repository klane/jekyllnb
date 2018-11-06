import os
import pytest
from difflib import Differ
from jekyllnb.jekyllnb import jekyllpath, JekyllNB
from pprint import pprint


FILE_NAME = 'hello-world'
SITE_DIR = 'docs'
OUTPUT_DIR = '_pages'
IMAGE_DIR = os.path.join('assets', 'images', FILE_NAME)

@pytest.fixture
def site_dir(tmpdir):
    return tmpdir.join(SITE_DIR)

@pytest.fixture
def image_dir(site_dir):
    return site_dir.join(IMAGE_DIR)

@pytest.fixture
def test_file(site_dir):
    JekyllNB.launch_instance([
        '--site-dir', site_dir.strpath,
        '--output-dir', OUTPUT_DIR,
        '--image-dir', IMAGE_DIR,
        os.path.join(os.path.dirname(__file__), 'resources', FILE_NAME + '.ipynb')
    ])

    return site_dir.join(OUTPUT_DIR, FILE_NAME + '.md')

def test_file_exists(test_file):
    assert test_file.check()

def test_image_exists(test_file, image_dir):
    assert os.path.isdir(image_dir.strpath)
    assert os.path.isfile(image_dir.join(FILE_NAME + '_4_0.png').strpath)

def test_file_contents(test_file):
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