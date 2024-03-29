"Trigram based algorithm for Addok."

from codecs import open  # To use a consistent encoding
from os import path

from setuptools import find_packages, setup


VERSION = (1, 1, 1)

here = path.abspath(path.dirname(__file__))

# Get the long description trigramsom the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def is_pkg(line):
    return line and not line.startswith(('--', 'git', '#'))


setup(
    name='addok-trigrams',
    version='.'.join(map(str, VERSION)),
    description=__doc__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/addok/addok-trigrams',
    author='Yohan Boniface',
    author_email='yohan.boniface@data.gouv.fr',
    license='WTFPL',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: GIS',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='addok geocoding',
    packages=find_packages(exclude=['tests']),
    extras_require={'test': ['pytest']},
    include_package_data=True,
    entry_points={'addok.ext': ['trigrams=addok_trigrams']},
)
