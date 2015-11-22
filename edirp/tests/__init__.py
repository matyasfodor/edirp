import fnmatch
from unittest import TestCase
import pep8
import os

from edirp.defaults import DEFAULT_PROJECT_DIR


def list_python_files_recursively(directory):
    python_files = []

    for root, _, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.py'):
            python_files.append(os.path.join(root, filename))

    return python_files


class TestCodeFormat(TestCase):

    def test_pep8_conformance(self):
        """Test that we conform to PEP8."""
        pep8style = pep8.StyleGuide(ignore=['E501'])
        python_files = list_python_files_recursively(DEFAULT_PROJECT_DIR)
        result = pep8style.check_files(python_files)
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")


class TestTest(TestCase):

    def test_fail(self):
        assert True
