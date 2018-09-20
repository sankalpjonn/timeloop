# please install python if it is not present in the system
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
 name='timeloop',
 version='1.0.1',
 packages=['timeloop'],
 license = 'MIT',
 description = 'An elegant way to run period tasks.',
 author = 'Sankalp Jonna',
 author_email = 'sankalpjonna@gmail.com',
 keywords = ['tasks','jobs','periodic task','interval','periodic job', 'flask style', 'decorator'],
 long_description=long_description,
 long_description_content_type="text/markdown",
 url="https://github.com/sankalpjonn/timeloop",
 include_package_data=True,
)
