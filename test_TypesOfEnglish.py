# Author: Luis Briones

import TypesOfEnglish
import unittest


class TestFunction(unittest.TestCase):
    def test_lowercase(self):
        self.assertEqual(TypesOfEnglish.check_type_of_english('color', {'color': 'american',
                                                                        'colour': 'british'}), 'American English')

    def test_uppercase(self):
        self.assertEqual(TypesOfEnglish.check_type_of_english('COLOUR', {'color': 'american',
                                                                        'colour': 'british'}), 'British English')

    def test_plural(self):
        self.assertEqual(TypesOfEnglish.check_type_of_english('humors and colours', {'color': 'american',
                                                                                    'colour': 'british',
                                                                                    'humor': 'american',
                                                                                    'humour': 'british'}), 'Mixed British and American English')

    def test_integer(self):
        self.assertEqual(TypesOfEnglish.check_type_of_english(9, {'color': 'american',
                                                                        'colour': 'british'}), 'Unknown')

    def test_within_word(self):
        self.assertEqual(TypesOfEnglish.check_type_of_english('literature', {'liter': 'american',
                                                                            'litre': 'british'}), 'Unknown')

    def test_within_characters(self):
        self.assertEqual(TypesOfEnglish.check_type_of_english('//liter</td>', {'liter': 'american',
                                                                            'litre': 'british'}), 'American English')


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestFunction))
    return test_suite


englishtestsuite = suite()
runner = unittest.TextTestRunner()
runner.run(englishtestsuite)
