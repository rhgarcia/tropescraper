import unittest
from tropescraper.web_page_retriever import WebPageRetriever

class TestWebPageRetriever(unittest.TestCase):

    def setUp(self):
        self.scraper = WebPageRetriever(0.5,"https://tvtropes.org/pmwiki/pmwiki.php/Film/FantasticBeastsAndWhereToFindThem","/tmp")

    def test_class(self):
        self.assertIsInstance( self.scraper, WebPageRetriever, "Correct class" )

    def test_retrieve(self):
        content = self.scraper.retrieve()
        self.assertIsNot( content, "",  "Retrieves something")
        content2 = self.scraper.retrieve()
        self.assertIs( content, conten2, "Retrieves from cache")
