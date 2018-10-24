from setuptools import setup

setup(
    name='jekyllnb',
    version='0.1',
    py_modules=['jekyllnb'],
    install_requires=[
        'Click',
        'PyYAML',
    ],
    entry_points='''
        [console_scripts]
        jekyllnb=jekyllnb:cli
    ''',
)
