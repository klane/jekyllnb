import os
from subprocess import CalledProcessError, check_output

import pytest
from conditional import conditional

from jekyllnb import JekyllNB
from jekyllnb.jekyllnb import jekyllpath
from tests import (
    AbstractConfig,
    Config,
    FILE_NAME,
    IMAGE_DIR,
    OUTPUT_DIR,
    SITE_DIR
)


@pytest.fixture
def site_dir(tmpdir):
    return tmpdir.join(SITE_DIR)


@pytest.fixture
def image_dir(site_dir):
    return site_dir.join(IMAGE_DIR, FILE_NAME)


@pytest.fixture
def test_file(site_dir):
    return site_dir.join(OUTPUT_DIR, FILE_NAME + '.md')


@pytest.fixture
def args(site_dir):
    return [
        '--site-dir', site_dir.strpath,
        '--output-dir', OUTPUT_DIR,
        '--image-dir', IMAGE_DIR,
        os.path.join(os.path.dirname(__file__), 'resources', FILE_NAME + '.ipynb')
    ]


class JekyllConfig(object):
    _app = JekyllNB
    _command = 'jekyllnb'


class TestJekyllNB(JekyllConfig, Config):
    @pytest.fixture(autouse=True,
                    params=[[], ['--to', 'jekyll'], ['--to', 'Jekyll']])
    def args(self, args, request):
        return request.param + args


class TestException(JekyllConfig, AbstractConfig):
    @pytest.fixture(autouse=True,
                    params=[[], ['--to', 'markdown'], ['--to', 'jekyll']])
    def args(self, args, request):
        return request.param + args

    @pytest.mark.parametrize('engine', [
        lambda self, args: self._app.launch_instance(args),
        lambda self, args: check_output(['jupyter', self._command] + args),
        lambda self, args: check_output(['python', '-m', self._command] + args)
    ])
    def test_jekyllnb_format_exception(self, engine, args):
        args_lower = [arg.lower() for arg in args]
        raise_exception = '--to' in args_lower and 'jekyll' not in args_lower
        exceptions = (ValueError, CalledProcessError)

        with conditional(raise_exception, pytest.raises(exceptions)):
            engine(self, args)
            self._app.clear_instance()


def test_jekyllpath():
    assert jekyllpath('assets\\images') == '{{ site.baseurl }}/assets/images'
