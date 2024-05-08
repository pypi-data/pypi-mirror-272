import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

os.environ['BURLAP_NO_LOAD'] = '1'

import burlap # pylint: disable=wrong-import-position


def read_md(f):
    with open(f, encoding='utf8') as fin:
        return fin.read()


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


def get_reqs(fn):
    return [_.strip() for _ in open(os.path.join(CURRENT_DIR, fn), encoding='utf8').readlines() if _.strip() and not _.strip().startswith('#')]


class Tox(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox # pylint: disable=import-outside-toplevel
        tox.cmdline(self.test_args)
        sys.exit(0)


setup(
    name="burlap",
    version=burlap.__version__,
    packages=find_packages(exclude=['ez_setup', 'tests']),
    scripts=['bin/burlap-admin.py'],
    package_data={
        'burlap': [
            'templates/*.*',
            'fixtures/*.*',
        ],
    },
    author="Chris Spencer",
    author_email="chrisspen@gmail.com",
    description="Fabric commands for simplifying server deployments",
    long_description=read_md('README.md'),
    long_description_content_type='text/markdown',
    license="MIT",
    url="https://gitlab.com/chrisspen/burlap",
    #https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration',
    ],
    zip_safe=False,
    include_package_data=True,
    install_requires=get_reqs('burlap/fixtures/requirements.txt'),
    tests_require=get_reqs('requirements-test.txt'),
    extras_require={'aws': ['boto>=2.49.0']},
    cmdclass={'test': Tox},
)
