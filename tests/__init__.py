import os
from abc import abstractmethod
from collections import namedtuple
from difflib import Differ
from pprint import pprint
from subprocess import call

import pytest

try:
    from abc import ABC
except ImportError:
    from abc import ABCMeta

    class ABC(object):
        __metaclass__ = ABCMeta

FILE_NAME = 'hello-world'
SITE_DIR = 'docs'
OUTPUT_DIR = '_pages'
IMAGE_DIR = os.path.join('assets', 'images')


class AbstractConfig(ABC):
    @abstractmethod
    def args(self):
        pass

    @pytest.fixture
    def app(self, args):
        self._app.launch_instance(args)

    @pytest.fixture
    def command_line(self, args):
        call(['jupyter', self._command] + args)

    @pytest.fixture
    def package(self, args):
        call(['python', '-m', self._command] + args)

    @pytest.fixture(autouse=True,
                    params=[pytest.lazy_fixture('app'),
                            pytest.lazy_fixture('command_line'),
                            pytest.param(
                                pytest.lazy_fixture('package'),
                                marks=pytest.mark.unix
                            )]
                    )
    def engine(self, request):
        yield request.param
        self._app.clear_instance()

    @pytest.fixture
    def target_contents(self):
        target_file = os.path.join(os.path.dirname(__file__),
                                   'resources', FILE_NAME + '.md')

        with open(target_file) as target:
            return parse_file(target)

    @pytest.fixture
    def test_contents(self, test_file):
        return parse_file(test_file)


class Config(AbstractConfig):
    def test_file_exists(self, test_file):
        assert test_file.check()

    def test_image_exists(self, image_dir):
        assert os.path.isdir(image_dir.strpath)
        assert os.path.isfile(image_dir.join(FILE_NAME + '_4_0.png').strpath)

    def test_file_header(self, test_contents, target_contents):
        try:
            assert all(line in target_contents.header for line in test_contents.header)
        except AssertionError:
            print_diff(test_contents.header, target_contents.header)
            raise

    def test_file_body(self, test_contents, target_contents):
        try:
            assert all(a == b for a, b in zip(test_contents.body, target_contents.body))
        except AssertionError:
            print_diff(test_contents.body, target_contents.body)
            raise


def parse_file(file):
    lines = file.read().splitlines()
    index = [i for i, x in enumerate(lines) if x == '---']
    header, body = lines[index[0]+1:index[1]], lines[index[1]+1:]
    contents = namedtuple('contents', 'header body')

    return contents(header, body)


def print_diff(test_lines, target_lines):
    differ = Differ()
    diff = differ.compare(test_lines, target_lines)
    pprint(list(diff))
