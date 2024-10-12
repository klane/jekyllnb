import os
from abc import ABC, abstractmethod
from collections.abc import Sequence
from difflib import Differ
from pathlib import Path
from pprint import pprint
from subprocess import call
from typing import NamedTuple, Type

import pytest
from nbconvert.nbconvertapp import NbConvertApp

FILE_NAME = "hello-world"
SITE_DIR = "docs"
PAGE_DIR = "_pages"
IMAGE_DIR = os.path.join("assets", "images")


class FileContents(NamedTuple):
    header: list[str]
    body: list[str]


class AbstractConfig(ABC):
    _app: Type[NbConvertApp]
    _command: str

    @abstractmethod
    @pytest.fixture
    def args(self) -> list[str]:
        pass

    @pytest.fixture
    def app(self, args: list[str]) -> None:
        self._app.launch_instance(args)

    @pytest.fixture
    def command(self, args: list[str]) -> None:
        call(["jupyter", self._command, *args])

    @pytest.fixture
    def package(self, args: list[str]) -> None:
        call(["python", "-m", self._command, *args])

    @pytest.fixture(autouse=True)
    def cleanup(self) -> None:
        self._app.clear_instance()


class Config(AbstractConfig):
    def test_file(self, output_file: Path):
        assert output_file.exists()

    def test_image(self, image_dir: Path):
        assert image_dir.is_dir()
        image = image_dir / (FILE_NAME + "_4_0.png")
        assert image.is_file()

    def test_header(self, file_contents: FileContents, target_contents: FileContents):
        try:
            assert all(line in target_contents.header for line in file_contents.header)
        except AssertionError:
            print_diff(file_contents.header, target_contents.header)
            raise

    def test_body(self, file_contents: FileContents, target_contents: FileContents):
        try:
            assert all(a == b for a, b in zip(file_contents.body, target_contents.body))
        except AssertionError:
            print_diff(file_contents.body, target_contents.body)
            raise


def print_diff(test_lines: Sequence[str], target_lines: Sequence[str]) -> None:
    differ = Differ()
    diff = differ.compare(test_lines, target_lines)
    pprint(list(diff))
