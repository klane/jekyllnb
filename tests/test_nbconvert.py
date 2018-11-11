from nbconvert.nbconvertapp import NbConvertApp
from subprocess import call
from tests import *


@pytest.fixture
def site_dir(tmpdir):
    return tmpdir.join(SITE_DIR, OUTPUT_DIR)

@pytest.fixture
def image_dir(site_dir):
    return site_dir.join(IMAGE_DIR)

@pytest.fixture
def nbconvert_file(site_dir):
    return site_dir.join(FILE_NAME + '.md')

@pytest.fixture
def nbconvert_execute(site_dir, request):
    params = [
        '--to', 'jekyll',
        '--output-dir', site_dir.strpath,
        '--NbConvertApp.output_files_dir=' + IMAGE_DIR,
        os.path.join(os.path.dirname(__file__), 'resources', FILE_NAME + '.ipynb')
    ]

    request.param(params)
    NbConvertApp.clear_instance()

@pytest.mark.parametrize('nbconvert_execute', [
    lambda params: NbConvertApp.launch_instance(params),
    lambda params: call(['jupyter', 'nbconvert'] + params)
], indirect=True)
class TestNbConvert(Config):
    def test_nbconvert_file_exists(self, nbconvert_execute, nbconvert_file):
        assert nbconvert_file.check()

    def test_nbconvert_image_exists(self, nbconvert_execute, image_dir):
        self.image_exists(image_dir)

    def test_nbconvert_file_contents(self, nbconvert_execute, nbconvert_file):
        self.file_contents_match(nbconvert_file)
