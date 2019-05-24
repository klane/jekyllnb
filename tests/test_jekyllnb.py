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
    PAGE_DIR,
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
    return site_dir.join(PAGE_DIR, FILE_NAME + '.md')


@pytest.fixture
def default_args(site_dir):
    return [
        '--site-dir', site_dir.strpath,
        '--page-dir', PAGE_DIR,
        os.path.join(os.path.dirname(__file__), 'resources', FILE_NAME + '.ipynb')
    ]


@pytest.fixture(params=[[IMAGE_DIR],
                        [os.path.join(IMAGE_DIR, FILE_NAME), '--no-auto-folder']])
def image_args(request):
    return ['--image-dir'] + request.param


class JekyllConfig(object):
    _app = JekyllNB
    _command = 'jekyllnb'


class TestJekyllNB(JekyllConfig, Config):
    @pytest.fixture(params=[[], ['--to', 'jekyll'], ['--to', 'Jekyll']])
    def args(self, default_args, image_args, request):
        return request.param + image_args + default_args


class TestException(JekyllConfig, AbstractConfig):
    @pytest.fixture(params=[[], ['--to', 'markdown'], ['--to', 'jekyll']])
    def args(self, default_args, image_args, request):
        return request.param + image_args + default_args

    @pytest.mark.parametrize('engine', [
        lambda self, args: self._app.launch_instance(args),
        lambda self, args: check_output(['jupyter', self._command] + args),
        pytest.param(
            lambda self, args: check_output(['python', '-m', self._command] + args),
            marks=pytest.mark.unix
        )
    ])
    def test_jekyllnb_format_exception(self, engine, args):
        args_lower = [arg.lower() for arg in args]
        raise_exception = '--to' in args_lower and 'jekyll' not in args_lower
        exceptions = (ValueError, CalledProcessError)

        with conditional(raise_exception, pytest.raises(exceptions)):
            engine(self, args)


def test_jekyllpath():
    assert jekyllpath('assets\\images') == '{{ site.baseurl }}/assets/images'
