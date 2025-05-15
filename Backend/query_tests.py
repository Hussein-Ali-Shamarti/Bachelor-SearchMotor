import unittest
from utils.query_utils import extract_filters_from_query, normalize

class TestQueryParsing(unittest.TestCase):
    def test_author_and_topic(self):
        author, topic, year, location = extract_filters_from_query("papers by berntzen on e-health")
        self.assertIn("berntzen", normalize(author))
        self.assertIn("ehealth", normalize(topic))

    def test_location_and_year(self):
        author, topic, year, location = extract_filters_from_query("studies from barcelona 2020")
        self.assertEqual(location.lower(), "barcelona")
        self.assertEqual(year, "2020")

    def test_initials_and_topic(self):
        author, topic, year, location = extract_filters_from_query("privacy research by L. Berntzen")
        self.assertIn("privacy", normalize(topic))
        self.assertIn("berntzen", normalize(topic))


    def test_compound_topic(self):
        author, topic, year, location = extract_filters_from_query("machine learning in healthcare")
        self.assertIn("machine learning", normalize(topic))
        self.assertIn("healthcare", normalize(topic))

    def test_topic_and_location_comma(self):
        author, topic, year, location = extract_filters_from_query("modeling, luxembourg")
        self.assertTrue("oslo" in normalize(location) or "oslo" in normalize(author))
        self.assertIn("big data", normalize(topic))

    def test_natural_question(self):
        author, topic, year, location = extract_filters_from_query("Can I see some articles about digital twins?")
        self.assertIn("digital twins", normalize(topic))

    def test_smart_city_topic(self):
        author, topic, year, location = extract_filters_from_query("Do you have anything on smart cities?")
        self.assertIn("smart cities", normalize(topic))

    def test_year_only(self):
        author, topic, year, location = extract_filters_from_query("I’m looking for studies written in 2018")
        self.assertEqual(year, "2018")

    def test_full_filter(self):
        author, topic, year, location = extract_filters_from_query("Find all papers from 2021 by Berntzen")
        self.assertEqual(year, "2021")
        self.assertIn("berntzen", normalize(author))

    def test_norwegian_author_topic(self):
        author, topic, year, location = extract_filters_from_query("finn artikler om personvern skrevet av berntzen")
        self.assertIn("berntzen", normalize(author))
        self.assertIn("personvern", normalize(topic))

    def test_norwegian_location_topic(self):
        author, topic, year, location = extract_filters_from_query("fra luxembourg om modeling")
        self.assertEqual(location.lower(), "luxembourg")
        self.assertIn("tingenes internett", normalize(topic))

    def test_norwegian_author_tech(self):
        author, topic, year, location = extract_filters_from_query("skrevet av l. berntzen om helseteknologi")
        self.assertIn("berntzen", normalize(author))
        self.assertIn("helseteknologi", normalize(topic))

if __name__ == '__main__':
    unittest.main()
