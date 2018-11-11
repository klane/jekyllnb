from conditional import conditional
from jekyllnb import JekyllNB
from jekyllnb.jekyllnb import jekyllpath
from subprocess import CalledProcessError, check_output
from tests import *


def jekyllnb_app(params):
    JekyllNB.launch_instance(params)
    JekyllNB.clear_instance()

def jekyllnb_command_line(params):
    check_output(['jupyter', 'jekyllnb'] + params)
    JekyllNB.clear_instance()

@pytest.fixture
def site_dir(tmpdir):
    return tmpdir.join(SITE_DIR)

@pytest.fixture
def image_dir(site_dir):
    return site_dir.join(IMAGE_DIR)

@pytest.fixture
def jekyllnb_file(site_dir):
    return site_dir.join(OUTPUT_DIR, FILE_NAME + '.md')

@pytest.fixture
def jekyllnb_args(site_dir):
    def _jekyllnb_args(argv=[]):
        params = argv + [
            '--site-dir', site_dir.strpath,
            '--output-dir', OUTPUT_DIR,
            '--image-dir', IMAGE_DIR,
            os.path.join(os.path.dirname(__file__), 'resources', FILE_NAME + '.ipynb')
        ]

        return params

    yield _jekyllnb_args

@pytest.fixture
def jekyllnb_execute(jekyllnb_args, request):
    def _jekyllnb_execute(argv):
        params = jekyllnb_args(argv)
        request.param(params)

    yield _jekyllnb_execute
    JekyllNB.clear_instance()

@pytest.mark.parametrize('jekyllnb_execute', [
    jekyllnb_app,
    jekyllnb_command_line
], indirect=True)
class Config(object): pass

@pytest.mark.parametrize('argv', [
    [],
    ['--to', 'jekyll'],
    ['--to', 'Jekyll']
])
class TestJekyllNB(Config):
    def test_jekyllnb_file_exists(self, jekyllnb_execute, jekyllnb_file, argv):
        jekyllnb_execute(argv)
        jekyllnb_file.check()

    def test_jekyllnb_image_exists(self, jekyllnb_execute, image_dir, argv):
        jekyllnb_execute(argv)
        assert os.path.isdir(image_dir.strpath)
        assert os.path.isfile(image_dir.join(FILE_NAME + '_4_0.png').strpath)

    def test_jekyllnb_file_contents(self, jekyllnb_execute, jekyllnb_file, argv):
        jekyllnb_execute(argv)
        test_lines = jekyllnb_file.readlines()
        target_file = os.path.join(os.path.dirname(__file__), 'resources', FILE_NAME + '.md')

        with open(target_file) as target:
            target_lines = target.readlines()

        try:
            assert all(a == b for a, b in zip(test_lines, target_lines))
        except AssertionError:
            differ = Differ()
            diff = differ.compare(test_lines, target_lines)
            pprint(list(diff))
            raise

@pytest.mark.parametrize('argv', [
    [],
    ['--to', 'markdown'],
    ['--to', 'jekyll']
])
class TestException(Config):
    def test_jekyllnb_format_exception(self, jekyllnb_execute, argv):
        raise_exception = 'jekyll' not in [arg.lower() for arg in argv] and len(argv) > 0
        exceptions = (ValueError, CalledProcessError)
        with conditional(raise_exception, pytest.raises(exceptions)) as e:
            jekyllnb_execute(argv)

def test_jekyllpath():
    assert jekyllpath('assets\\images') == '{{ site.baseurl }}/assets/images'
