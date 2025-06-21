import sys
from pathlib import Path

import pytest
from pytest import FixtureRequest
from pytest_lazy_fixtures import lf

from tests import FILE_NAME, FileContents


def parse_file(file: Path) -> FileContents:
    lines = file.read_text().splitlines()
    index = [i for i, x in enumerate(lines) if x == "---"]
    return FileContents(
        header=lines[index[0] + 1 : index[1]],
        body=lines[index[1] + 1 :],
    )


@pytest.fixture(
    autouse=True,
    params=[
        pytest.param(lf("app"), id="app"),
        pytest.param(lf("command"), id="cmd"),
        pytest.param(
            lf("package"),
            id="pkg",
            marks=pytest.mark.skipif(
                sys.platform.startswith("win"), reason="fails on windows"
            ),
        ),
    ],
)
def engine() -> None:
    # converts the notebook using the specified engine
    ...


@pytest.fixture(
    params=[
        pytest.param(FILE_NAME + ".ipynb", id="file"),
        pytest.param("*.ipynb", id="wild"),
    ]
)
def input_file(request: FixtureRequest) -> Path:
    return Path(__file__).parent / "assets" / request.param


@pytest.fixture
def target_contents() -> FileContents:
    target_file = Path(__file__).parent / "assets" / (FILE_NAME + ".md")
    return parse_file(target_file)


@pytest.fixture
def file_contents(output_file: Path) -> FileContents:
    return parse_file(output_file)
