from jekyllnb import JekyllNB
from jekyllnb.jekyllnb import jekyllpath
from tests import *


@pytest.fixture
def site_dir(tmpdir):
    return tmpdir.join(SITE_DIR)

@pytest.fixture
def image_dir(site_dir):
    return site_dir.join(IMAGE_DIR)

@pytest.fixture
def test_file(site_dir):
    return site_dir.join(OUTPUT_DIR, FILE_NAME + '.md')

class TestJekyllNB(Config):
    _app = JekyllNB
    _command = 'jekyllnb'

    @pytest.fixture(autouse=True,
                    params=[[], ['--to', 'jekyll'], ['--to', 'Jekyll']])
    def args(self, site_dir, request):
        return request.param + [
            '--site-dir', site_dir.strpath,
            '--output-dir', OUTPUT_DIR,
            '--image-dir', IMAGE_DIR,
            os.path.join(os.path.dirname(__file__), 'resources', FILE_NAME + '.ipynb')
        ]

# @pytest.mark.parametrize('argv', [
#     [],
#     ['--to', 'markdown'],
#     ['--to', 'jekyll']
# ])
# class TestException(JekyllConfig):
#     def test_jekyllnb_format_exception(self, jekyllnb_execute, argv):
#         raise_exception = 'jekyll' not in [arg.lower() for arg in argv] and len(argv) > 0
#         exceptions = (ValueError, CalledProcessError)
#         with conditional(raise_exception, pytest.raises(exceptions)) as e:
#             jekyllnb_execute(argv)

def test_jekyllpath():
    assert jekyllpath('assets\\images') == '{{ site.baseurl }}/assets/images'
