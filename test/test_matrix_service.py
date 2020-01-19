from unittest import TestCase
import pprint

from service.matrix_service import get_most_related_words

pp = pprint.PrettyPrinter()


class Test(TestCase):
    def test_get_most_related_words(self):
        word = "Python"
        most_correlated_words = get_most_related_words(word, 10)
        pp.pprint(most_correlated_words)
