from setuptools import setup
from sys import argv


def is_register_command(a):
    for item in a:
        if item.startswith('-'):
            continue
        return item in ('register', 'bdist_wheel')
    return False

longdesc = None
if is_register_command(argv[1:]):
    # run before building a wheel:
    # pandoc -f markdown_github -t rst README.md > README.rst
    with open('README.rst') as f:
        longdesc = f.read()


setup(
    name='pybrood',
    version='0.9.0',
    description='Broodwar API binding',
    long_description=longdesc,
    url='https://github.com/neumond/pybrood',
    author='Vitalik Verhovodov',
    author_email='knifeslaughter@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Games/Entertainment',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 7',
    ],
    keywords='bwapi starcraft broodwar ai binding',
    packages=['pybrood'],
    package_data={'pybrood': ['inner.pyd']},
)
