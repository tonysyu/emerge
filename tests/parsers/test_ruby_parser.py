"""
All unit tests that are related to RubyParser.
"""

# Authors: Grzegorz Lato <grzegorz.lato@gmail.com>
# License: MIT

import unittest
from emerge.languages.rubyparser import RubyParser
from emerge.results import FileResult
from emerge.languages.abstractparser import LanguageType
from emerge.analysis import Analysis
from tests.testdata.ruby import RUBY_TEST_FILES
from typing import Dict
import coloredlogs
import logging

LOGGER = logging.getLogger('TESTS')
coloredlogs.install(level='INFO', logger=LOGGER, fmt='\n%(asctime)s %(name)s %(levelname)s %(message)s')


class RubyParserTestCase(unittest.TestCase):

    def setUp(self):
        self.example_data = RUBY_TEST_FILES
        self.parser = RubyParser()
        self.analysis = Analysis()
        self.analysis.analysis_name = "test"

    def tearDown(self):
        pass

    def test_generate_file_results(self):
        """Generate file results and check basic attributes."""
        self.assertFalse(self.parser.results)

        for file_name, file_content in self.example_data.items():
            self.parser.generate_file_result_from_analysis(self.analysis, file_name=file_name, file_content=file_content)

        results: Dict[str, FileResult] = self.parser.results
        self.assertTrue(results)
        self.assertTrue(len(results) == 2)

        result: FileResult
        for _, result in results.items():
            self.assertTrue(len(result.scanned_tokens) > 0)
            self.assertTrue(len(result.scanned_import_dependencies) > 0)

            self.assertTrue(result.analysis.analysis_name.strip())
            self.assertTrue(result.scanned_file_name.strip())
            self.assertTrue(result.scanned_by.strip())
            self.assertTrue(result.scanned_language == LanguageType.RUBY)
        LOGGER.info(f'test successful')
