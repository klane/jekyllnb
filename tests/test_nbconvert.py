from nbconvert.nbconvertapp import NbConvertApp

from tests import *


@pytest.fixture
def site_dir(tmpdir):
    return tmpdir.join(SITE_DIR, OUTPUT_DIR)


@pytest.fixture
def image_dir(site_dir):
    return site_dir.join(IMAGE_DIR)


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
            '--NbConvertApp.output_files_dir=' + IMAGE_DIR,
            os.path.join(os.path.dirname(__file__), 'resources', FILE_NAME + '.ipynb')
        ]
