from conditional import conditional
from jekyllnb import JekyllNB
from jekyllnb.jekyllnb import jekyllpath
from subprocess import CalledProcessError, check_output
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

class JekyllConfig(object):
    _app = JekyllNB
    _command = 'jekyllnb'

class TestJekyllNB(JekyllConfig, Config):
    @pytest.fixture(autouse=True,
                    params=[[], ['--to', 'jekyll'], ['--to', 'Jekyll']])
    def args(self, site_dir, request):
        return request.param + [
            '--site-dir', site_dir.strpath,
            '--output-dir', OUTPUT_DIR,
            '--image-dir', IMAGE_DIR,
            os.path.join(os.path.dirname(__file__), 'resources', FILE_NAME + '.ipynb')
        ]

class TestException(JekyllConfig, AbstractConfig):
    @pytest.fixture(autouse=True,
                    params=[[], ['--to', 'markdown'], ['--to', 'jekyll']])
    def args(self, site_dir, request):
        return request.param + [
            '--site-dir', site_dir.strpath,
            '--output-dir', OUTPUT_DIR,
            '--image-dir', IMAGE_DIR,
            os.path.join(os.path.dirname(__file__), 'resources', FILE_NAME + '.ipynb')
        ]

    @pytest.mark.parametrize('engine', [
        lambda self, args: self._app.launch_instance(args),
        lambda self, args: check_output(['jupyter', self._command] + args)
    ])
    def test_jekyllnb_format_exception(self, engine, args):
        args_lower = [arg.lower() for arg in args]
        raise_exception = '--to' in args_lower and 'jekyll' not in args_lower
        exceptions = (ValueError, CalledProcessError)

        with conditional(raise_exception, pytest.raises(exceptions)) as e:
            engine(self, args)
            self._app.clear_instance()

def test_jekyllpath():
    assert jekyllpath('assets\\images') == '{{ site.baseurl }}/assets/images'
