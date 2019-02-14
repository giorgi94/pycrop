import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='pycrop',
    version='1.0.1',
    packages=['pycrop'],
    description='Methods to manipulate images',
    include_package_data=True,
    long_description=README,
    author='Giorgi Kakulashvili',
    # author_email='yourname@example.com',
    url='https://github.com/giorgi94/pycrop',
    keywords=['pillow', 'contain', 'cover'],
    platforms=['OS Independent'],
    license='MIT',
    install_requires=[
        'Pillow>=5.3.0'
    ]
)
