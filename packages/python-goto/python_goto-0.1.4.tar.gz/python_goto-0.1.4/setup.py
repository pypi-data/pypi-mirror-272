from setuptools import setup

VERSION = '0.1.4'
DESCRIPTION = 'Add goto to Python'
LONG_DESCRIPTION = open('C:\\Users\\NewUser\\Desktop\\github\\pygoto\\README.md', 'r').read()

setup(
    name='python-goto',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='The Lumberjack',
    author_email='just4now@example.com',
    packages=['python_goto'],
    keywords=['goto']
)