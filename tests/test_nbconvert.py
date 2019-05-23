import os

import pytest
from nbconvert.nbconvertapp import NbConvertApp

from tests import (
    Config,
    FILE_NAME,
    IMAGE_DIR,
    OUTPUT_DIR,
    SITE_DIR
)


@pytest.fixture
def site_dir(tmpdir):
    return tmpdir.join(SITE_DIR, OUTPUT_DIR)


@pytest.fixture
def image_dir(site_dir):
    return site_dir.join(IMAGE_DIR, FILE_NAME)


@pytest.fixture
def test_file(site_dir):
    return site_dir.join(FILE_NAME + '.md')


class TestNbConvert(Config):
    _app = NbConvertApp
    _command = 'nbconvert'

    @pytest.fixture(autouse=True)
    def args(self, site_dir):
        return [
            '--to', 'jekyll',
            '--output-dir', site_dir.strpath,
            '--NbConvertApp.output_files_dir=' + os.path.join(IMAGE_DIR, FILE_NAME),
            os.path.join(os.path.dirname(__file__), 'resources', FILE_NAME + '.ipynb')
        ]
