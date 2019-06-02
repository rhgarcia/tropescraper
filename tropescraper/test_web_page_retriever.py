import unittest
from tropescraper.web_page_retriever import WebPageRetriever

class TestWebPageRetriever(unittest.TestCase):

    def setUp(self):
        self.scraper = WebPageRetriever(0.5,"https://tvtropes.org/pmwiki/pmwiki.php/Film/FantasticBeastsAndWhereToFindThem","/tmp")

    def test_class(self):
        self.assertIsInstance( self.scraper, WebPageRetriever, "Correct class" )
