import os
from pathlib import Path

import pytest
from nbconvert.nbconvertapp import NbConvertApp

from tests import FILE_NAME, IMAGE_DIR, PAGE_DIR, SITE_DIR, Config


@pytest.fixture
def site_dir(tmp_path: Path) -> Path:
    return tmp_path / SITE_DIR / PAGE_DIR


@pytest.fixture
def image_dir(site_dir: Path) -> Path:
    return site_dir / IMAGE_DIR / FILE_NAME


@pytest.fixture
def output_file(site_dir: Path) -> Path:
    return site_dir / (FILE_NAME + ".md")


class TestNbConvert(Config):
    _app = NbConvertApp
    _command = "nbconvert"

    @pytest.fixture
    def args(self, site_dir: Path, input_file: Path) -> list[str]:
        return [
            "--to",
            "jekyll",
            "--output-dir",
            str(site_dir),
            "--NbConvertApp.output_files_dir=" + os.path.join(IMAGE_DIR, FILE_NAME),
            str(input_file),
        ]
