import os
import sys
from collections import namedtuple

import pytest
from pytest_lazyfixture import lazy_fixture

from tests import FILE_NAME


def parse_file(file):
    lines = file.read().splitlines()
    index = [i for i, x in enumerate(lines) if x == "---"]
    header, body = lines[index[0] + 1 : index[1]], lines[index[1] + 1 :]
    contents = namedtuple("contents", "header body")

    return contents(header, body)


@pytest.fixture(
    autouse=True,
    params=[
        pytest.param(lazy_fixture("app"), id="app"),
        pytest.param(lazy_fixture("command"), id="cmd"),
        pytest.param(
            lazy_fixture("package"),
            id="pkg",
            marks=pytest.mark.skipif(
                sys.platform.startswith("win"), reason="fails on windows"
            ),
        ),
    ],
)
def engine():
    pass


@pytest.fixture(
    params=[
        pytest.param(FILE_NAME + ".ipynb", id="file"),
        pytest.param("*.ipynb", id="wild"),
    ]
)
def input_file(request):
    return os.path.join(os.path.dirname(__file__), "assets", request.param)


@pytest.fixture
def target_contents():
    target_file = os.path.join(os.path.dirname(__file__), "assets", FILE_NAME + ".md")

    with open(target_file) as target:
        return parse_file(target)


@pytest.fixture
def file_contents(output_file):
    return parse_file(output_file)
