import unittest

from tropescraper.adaptors.web_page_retriever import WebPageRetriever


class WebPageRetrieverTestCase(unittest.TestCase):
    def test_retrieve_when_called_then_returns_the_page(self):
        retriever = WebPageRetriever(wait_time_between_calls_in_seconds=0)
        content = retriever.retrieve('https://tvtropes.org/pmwiki/pmwiki.php/Main/Film')
        self.assertIn('Index of Films', content, 'Should\'ve downloaded the page')
