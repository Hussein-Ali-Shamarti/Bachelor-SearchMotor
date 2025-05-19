# Dette testskriptet validerer funksjonaliteten til spørringsparseren i `query_utils.py`, 
# inkludert korrekt identifisering av forfatter, emne, år og sted fra både naturlige og strukturerte forespørsler 
# på norsk og engelsk.


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
        self.assertIn("privacy research", normalize(topic))
        self.assertIn("berntzen", normalize(author))


    def test_compound_topic(self):
        author, topic, year, location = extract_filters_from_query("machine learning in healthcare")
        self.assertIn("machine learning", normalize(topic))
        self.assertIn("healthcare", normalize(topic))

    def test_topic_and_location_comma(self):
        author, topic, year, location = extract_filters_from_query("modeling, luxembourg")
        self.assertTrue("luxembourg" in normalize(location) or "luxembourg" in normalize(author))
        self.assertIn("modeling", normalize(topic))

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
        self.assertIn("modeling", normalize(topic))

    def test_norwegian_author_tech(self):
        author, topic, year, location = extract_filters_from_query("skrevet av l. berntzen om blockchain")
        self.assertIn("berntzen", normalize(author))
        self.assertIn("blockchain", normalize(topic))

if __name__ == '__main__':
    unittest.main()
