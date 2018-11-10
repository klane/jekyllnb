from conditional import conditional
from jekyllnb.jekyllnb import jekyllpath
from tests import *


@pytest.fixture
def site_dir(tmpdir):
    return tmpdir.join(SITE_DIR)

@pytest.fixture
def image_dir(site_dir):
    return site_dir.join(IMAGE_DIR)

@pytest.fixture
def jekyllnb_file(site_dir):
    from jekyllnb import JekyllNB

    def _jekyllnb_file(argv=[]):
        JekyllNB.launch_instance(argv + [
            '--site-dir', site_dir.strpath,
            '--output-dir', OUTPUT_DIR,
            '--image-dir', IMAGE_DIR,
            os.path.join(os.path.dirname(__file__), 'resources', FILE_NAME + '.ipynb')
        ])

        return site_dir.join(OUTPUT_DIR, FILE_NAME + '.md')

    yield _jekyllnb_file
    JekyllNB.clear_instance()

@pytest.mark.parametrize('argv', [
    [],
    ['--to', 'jekyll'],
    ['--to', 'Jekyll'],
    ['--to', 'markdown']
])
def test_jekyllnb_file_exists(jekyllnb_file, argv):
    raise_exception = 'jekyll' not in [arg.lower() for arg in argv] and len(argv) > 0
    with conditional(raise_exception, pytest.raises(ValueError)) as e_info:
        assert jekyllnb_file(argv).check()

def test_jekyllnb_image_exists(jekyllnb_file, image_dir):
    jekyllnb_file()
    assert os.path.isdir(image_dir.strpath)
    assert os.path.isfile(image_dir.join(FILE_NAME + '_4_0.png').strpath)

def test_jekyllnb_file_contents(jekyllnb_file):
    test_lines = jekyllnb_file().readlines()
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

def test_jekyllpath():
    assert jekyllpath('assets\\images') == '{{ site.baseurl }}/assets/images'
