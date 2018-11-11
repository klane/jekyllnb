import os
import pytest
from difflib import Differ
from pprint import pprint


FILE_NAME = 'hello-world'
SITE_DIR = 'docs'
OUTPUT_DIR = '_pages'
IMAGE_DIR = os.path.join('assets', 'images', FILE_NAME)

class Config(object):
    def image_exists(self, image_dir):
        assert os.path.isdir(image_dir.strpath)
        assert os.path.isfile(image_dir.join(FILE_NAME + '_4_0.png').strpath)

    def file_contents_match(self, test_file):
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
