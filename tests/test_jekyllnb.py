import os
import sys
from contextlib import ExitStack as does_not_raise
from pathlib import Path
from subprocess import PIPE, CalledProcessError, Popen, check_output
from typing import Callable, ContextManager

import pytest
from pytest import FixtureRequest

from jekyllnb import __version__
from jekyllnb.jekyllnb import JekyllNB
from tests import FILE_NAME, IMAGE_DIR, PAGE_DIR, SITE_DIR, Config


@pytest.fixture
def site_dir(tmp_path: Path) -> Path:
    return tmp_path / SITE_DIR


@pytest.fixture
def image_dir(site_dir: Path) -> Path:
    return site_dir / IMAGE_DIR / FILE_NAME


@pytest.fixture
def output_file(site_dir: Path) -> Path:
    return site_dir / PAGE_DIR / (FILE_NAME + ".md")


@pytest.fixture
def default_args(site_dir: Path, input_file: Path) -> list[str]:
    return [
        "--site-dir",
        str(site_dir),
        "--page-dir",
        PAGE_DIR,
        str(input_file),
    ]


@pytest.fixture(
    params=[
        pytest.param([IMAGE_DIR], id="auto"),
        pytest.param(
            [os.path.join(IMAGE_DIR, FILE_NAME), "--no-auto-folder"], id="man"
        ),
    ]
)
def image_args(request: FixtureRequest) -> list[str]:
    return ["--image-dir", *request.param]


class JekyllConfig:
    _app = JekyllNB
    _command = "jekyllnb"


class TestJekyllNB(JekyllConfig, Config):
    @pytest.fixture(
        params=[
            pytest.param([], id="empty"),
            pytest.param(["--to", "jekyll"], id="lower"),
            pytest.param(["--to", "Jekyll"], id="upper"),
        ]
    )
    def args(
        self, default_args: list[str], image_args: list[str], request: FixtureRequest
    ) -> list[str]:
        return request.param + image_args + default_args


@pytest.mark.parametrize(
    "args,expectation",
    [
        ([], does_not_raise()),
        (["--to", "jekyll"], does_not_raise()),
        (["--to", "markdown"], pytest.raises((ValueError, CalledProcessError))),
    ],
    ids=["empty", "jekyll", "markdown"],
)
class TestException(JekyllConfig):
    @pytest.mark.parametrize(
        "engine",
        [
            pytest.param(lambda self, args: self._app.launch_instance(args), id="app"),
            pytest.param(
                lambda self, args: check_output(["jupyter", self._command, *args]),
                id="cmd",
            ),
            pytest.param(
                lambda self, args: check_output(["python", "-m", self._command, *args]),
                id="pkg",
                marks=pytest.mark.skipif(
                    sys.platform.startswith("win"), reason="fails on windows"
                ),
            ),
        ],
    )
    def test_exception(
        self,
        engine: Callable[[JekyllConfig, list[str]], None],
        args: list[str],
        expectation: ContextManager,
        default_args: list[str],
    ):
        with expectation:
            engine(self, args + default_args)

    @pytest.fixture(autouse=True)
    def cleanup(self) -> None:
        self._app.clear_instance()


class TestVersion(JekyllConfig):
    @pytest.mark.parametrize(
        "engine",
        [
            pytest.param(["jupyter"], id="cmd"),
            pytest.param(
                ["python", "-m"],
                id="pkg",
                marks=pytest.mark.skipif(
                    sys.platform.startswith("win"), reason="fails on windows"
                ),
            ),
        ],
    )
    def test_version(self, engine: list[str]):
        process = Popen([*engine, self._command, "--version"], stdout=PIPE)

        if process.stdout:
            assert process.stdout.readline().decode("UTF8").strip() == __version__
        else:
            pytest.fail("stdout has no output")
