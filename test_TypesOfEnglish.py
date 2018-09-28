# Author: Luis Briones
import TypesOfEnglish
import unittest


class TestFunction(unittest.TestCase):
    def test_lowercase(self):
        self.assertEqual(TypesOfEnglish.check_type_of_english('color', {'americanwords': ['color'],
                                                                        'britishwords': ['colour']}), 'American English')

    def test_uppercase(self):
        self.assertEqual(TypesOfEnglish.check_type_of_english('COLOUR', {'americanwords': ['color'],
                                                                         'britishwords': ['colour']}), 'British English')

    def test_plural(self):
        self.assertEqual(TypesOfEnglish.check_type_of_english('humors and colours', {'americanwords': ['color', 'humor'],
                                                                                     'britishwords': ['colour', 'humour']}), 'Mixed British and American English')

    def test_integer(self):
        self.assertEqual(TypesOfEnglish.check_type_of_english(9, {'americanwords': ['color'],
                                                                  'britishwords': ['colour']}), 'Unknown')

    def test_within_word(self):
        self.assertEqual(TypesOfEnglish.check_type_of_english('literature', {'americanwords': ['liter'],
                                                                             'britishwords': ['litre']}), 'Unknown')

    def test_within_characters(self):
        self.assertEqual(TypesOfEnglish.check_type_of_english('//liter</td>', {'americanwords': ['liter'],
                                                                               'britishwords': ['litre']}), 'American English')


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestFunction))
    return test_suite


englishtestsuite = suite()
runner = unittest.TextTestRunner()
runner.run(englishtestsuite)
