import itertools
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

@pytest.fixture(params=itertools.product([
    jekyllnb_app,
    jekyllnb_command_line], [
    [],
    ['--to', 'jekyll'],
    ['--to', 'Jekyll']
]))
def jekyllnb_execute(jekyllnb_args, request):
    fixture, params = request.param
    fixture(jekyllnb_args(params))

@pytest.fixture
def jekyllnb_execute2(jekyllnb_args, request):
    def _jekyllnb_execute2(argv):
        params = jekyllnb_args(argv)
        request.param(params)

    yield _jekyllnb_execute2
    JekyllNB.clear_instance()

def test_jekyllnb_file_exists(jekyllnb_execute, jekyllnb_file):
    assert jekyllnb_file.check()

def test_jekyllnb_image_exists(jekyllnb_execute, image_dir):
    assert os.path.isdir(image_dir.strpath)
    assert os.path.isfile(image_dir.join(FILE_NAME + '_4_0.png').strpath)

def test_jekyllnb_file_contents(jekyllnb_execute, jekyllnb_file):
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

@pytest.mark.parametrize('jekyllnb_execute2', [
    jekyllnb_app,
    jekyllnb_command_line
], indirect=True)
@pytest.mark.parametrize('argv', [
    [],
    ['--to', 'jekyll'],
    ['--to', 'Jekyll']
])
class TestJekyllNB(object):
    def test_jekyllnb_file_exists2(self, jekyllnb_execute2, jekyllnb_file, argv):
        jekyllnb_execute2(argv)
        jekyllnb_file.check()

    def test_jekyllnb_image_exists2(self, jekyllnb_execute2, image_dir, argv):
        jekyllnb_execute2(argv)
        assert os.path.isdir(image_dir.strpath)
        assert os.path.isfile(image_dir.join(FILE_NAME + '_4_0.png').strpath)

    def test_jekyllnb_file_contents2(self, jekyllnb_execute2, jekyllnb_file, argv):
        jekyllnb_execute2(argv)
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

@pytest.mark.parametrize('engine', [
    jekyllnb_app,
    jekyllnb_command_line
])
@pytest.mark.parametrize('argv', [
    [],
    ['--to', 'markdown'],
    ['--to', 'jekyll']
])
def test_jekyllnb_format_exception(jekyllnb_args, engine, argv):
    raise_exception = 'jekyll' not in [arg.lower() for arg in argv] and len(argv) > 0
    exceptions = (ValueError, CalledProcessError)
    with conditional(raise_exception, pytest.raises(exceptions)) as e:
        engine(jekyllnb_args(argv))

def test_jekyllpath():
    assert jekyllpath('assets\\images') == '{{ site.baseurl }}/assets/images'
