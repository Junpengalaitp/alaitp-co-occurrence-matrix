import pprint
from unittest import TestCase

from constant.category import fw, lb, pl, ol
from service.matrix_service import get_most_related_words

pp = pprint.PrettyPrinter()


class Test(TestCase):

    def test_get_most_related_words_1(self):
        test_word = "Python"
        test_categories = [lb, fw]
        expected_words = ["Flask", "Django", "Pandas"]
        most_correlated_words = get_most_related_words(test_word, 30, test_categories)
        pp.pprint(most_correlated_words)
        self.assertTrue(all([word in most_correlated_words.keys() for word in expected_words]))

    def test_get_most_related_words_2(self):
        test_word = "Java"
        test_categories = [pl, ol, lb, fw]
        expected_words = ["Spring", "Spring Boot", "JUnit", "Apache Hadoop", "Apache Spark", "Hibernate"]
        most_correlated_words = get_most_related_words(test_word, 30, test_categories)
        pp.pprint(most_correlated_words)
        self.assertTrue(all([word in most_correlated_words.keys() for word in expected_words]))

    def test_get_most_related_words_3(self):
        test_word = "JavaScript"
        test_categories = [pl, ol, lb, fw]
        expected_words = ["TypeScript", "ECMAScript", "HTML", "CSS", "React", "Redux"]
        most_correlated_words = get_most_related_words(test_word, 30, test_categories)
        pp.pprint(most_correlated_words)
        self.assertTrue(all([word in most_correlated_words.keys() for word in expected_words]))


