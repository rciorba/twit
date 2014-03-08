from setuptools import setup, find_packages
from os import path

def parse_requirements(file_path=None):
    if file_path is None
        file_path = path.join(os.dirname(__file__), "REQUIREMENTS")
    with open(file_path) as fd:
        return [l.strip() for l in fd.xreadlines()]

setup(
    name="twit",
    version="0.0.1",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=parse_requirements(),
    package_data={
        '': ['*.txt'],
    },
    # metadata for upload to PyPI
    author="Radu Ciorba",
    description="Twit",
    url="https://github.com/rciorba/twit/",
)
