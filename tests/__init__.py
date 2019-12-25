import os
from abc import ABC, abstractmethod
from difflib import Differ
from pprint import pprint
from subprocess import call

import pytest

FILE_NAME = "hello-world"
SITE_DIR = "docs"
PAGE_DIR = "_pages"
IMAGE_DIR = os.path.join("assets", "images")


class AbstractConfig(ABC):
    @abstractmethod
    @pytest.fixture
    def args(self):
        pass

    @pytest.fixture
    def app(self, args):
        self._app.launch_instance(args)

    @pytest.fixture
    def command(self, args):
        call(["jupyter", self._command] + args)

    @pytest.fixture
    def package(self, args):
        call(["python", "-m", self._command] + args)

    @pytest.fixture(autouse=True)
    def cleanup(self):
        self._app.clear_instance()


class Config(AbstractConfig):  # skipcq: PYL-W0223
    def test_file(self, output_file):  # skipcq: PYL-R0201
        assert output_file.check()

    def test_image(self, image_dir):  # skipcq: PYL-R0201
        assert os.path.isdir(image_dir.strpath)
        assert os.path.isfile(image_dir.join(FILE_NAME + "_4_0.png").strpath)

    def test_header(self, file_contents, target_contents):  # skipcq: PYL-R0201
        try:
            assert all(line in target_contents.header for line in file_contents.header)
        except AssertionError:
            print_diff(file_contents.header, target_contents.header)
            raise

    def test_body(self, file_contents, target_contents):  # skipcq: PYL-R0201
        try:
            assert all(a == b for a, b in zip(file_contents.body, target_contents.body))
        except AssertionError:
            print_diff(file_contents.body, target_contents.body)
            raise


def print_diff(test_lines, target_lines):
    differ = Differ()
    diff = differ.compare(test_lines, target_lines)
    pprint(list(diff))
