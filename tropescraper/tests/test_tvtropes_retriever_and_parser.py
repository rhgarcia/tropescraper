import unittest

from tropescraper.use_cases.parsers.tvtropes_parser import TVTropesParser
from tropescraper.adaptors.web_page_retriever import WebPageRetriever


class TVTropesParserTestCase(unittest.TestCase):
    SAMPLE_CATEGORY = 'FilmsOfThe1980s'
    SAMPLE_FILM = 'BackToTheFuture'
    SAMPLE_TROPE = 'BigHeroicRun'

    def setUp(self) -> None:
        self.parser = TVTropesParser()
        self.retriever = WebPageRetriever(wait_time_between_calls_in_seconds=0)

    def test_extract_categories_when_starting_page_retrieved_then_returns_categories(self):
        url = self.parser.get_films_starting_url()
        content = self.retriever.retrieve(url)
        categories = self.parser.extract_categories(content)
        self.assertIn(self.SAMPLE_CATEGORY, categories, f'Should\'ve found the category {self.SAMPLE_CATEGORY}')

    def test_extract_films_when_category_page_retrieved_then_returns_films(self):
        url = self.parser.get_category_url(self.SAMPLE_CATEGORY)
        content = self.retriever.retrieve(url)
        films = self.parser.extract_films(content)
        self.assertIn(self.SAMPLE_FILM, films, f'Should\'ve found the film {self.SAMPLE_FILM}')

    def test_extract_categories_when_categories_page_retrieved_then_returns_the_tropes(self):
        url = self.parser.get_film_url(self.SAMPLE_FILM)
        content = self.retriever.retrieve(url)
        tropes = self.parser.extract_tropes_from_film_page(content)
        self.assertIn(self.SAMPLE_TROPE, tropes, f'Should\'ve found the trope {self.SAMPLE_TROPE}')