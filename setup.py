from setuptools import setup, find_packages


setup(
    name="twit",
    version="0.0.1",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=["tweepy", "pyelasticsearch", "PyZMQ"],
    package_data={
        '': ['*.txt'],
    },
    # metadata for upload to PyPI
    author="Radu Ciorba",
    description="Twit",
    url="https://github.com/rciorba/twit/",
)
