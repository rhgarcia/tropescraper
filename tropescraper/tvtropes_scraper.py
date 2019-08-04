import datetime
import logging
from collections import OrderedDict
from tropescraper.common.object_factory import ObjectFactory
from tropescraper.interfaces.cache_interface import CacheInterface
from tropescraper.interfaces.page_parser_interface import PageParserInterface
from tropescraper.interfaces.web_page_retriever_interface import WebPageRetrieverInterface


class TVTropesScraper(object):
    logger = logging.getLogger(__name__)

    def __init__(self, wait_time_between_calls_in_seconds=None, cache_path=None):
        self.wait_time_between_calls_in_seconds = wait_time_between_calls_in_seconds
        self.cache_path = cache_path

        self.films = None
        self.tropes = None
        self.tropes_by_film = OrderedDict()
        self.latest_log_datetime = None
        self.parser = ObjectFactory().get_instance(PageParserInterface)

    def get_tropes(self):
        self.logger.info('Process started\n* Remember that you can stop and restart at any time.\n'
                         '** Please, remove manually the cache folder when you are done\n')

        self._extract_film_ids()
        self._extract_tropes()

        return self.tropes_by_film

    def _extract_film_ids(self):
        self.logger.info('Scraping film ids...')

        self.films = set()
        starting_url = self.parser.get_starting_url()
        page = self._retrieve(starting_url)
        category_ids = self.parser.extract_categories(page)

        for category_id in category_ids:
            category_url = self.parser.get_category_url(category_id)
            page = self._retrieve(category_url)
            film_ids = self.parser.extract_films(page)
            self.films.update(film_ids)

        self.logger.info(f'Found {len(self.films)} films')

    def _extract_tropes(self):
        self.logger.info('Scraping tropes (this might take a while...)')

        self.tropes = set()
        self.tropes_by_film = OrderedDict()
        sorted_films = sorted(list(self.films))

        self.logger.debug(f'Found {len(sorted_films)} films')

        for counter, film in enumerate(sorted_films):
            url = self.parser.get_film_url(film)
            page = self._retrieve(url)
            trope_ids = self.parser.extract_tropes(page)

            self.logger.debug(f'Film {film} ({len(trope_ids)} tropes): {trope_ids}')

            self.tropes.update(trope_ids)
            self.tropes_by_film[film] = sorted(trope_ids)

            if self._should_log_status():
                self._log_status(counter, sorted_films)

    def _should_log_status(self):
        now = datetime.datetime.now()
        return self.latest_log_datetime is None or now - self.latest_log_datetime > datetime.timedelta(seconds=5)

    def _log_status(self, counter, sorted_films):
        self.logger.info(f'Status: {counter + 1}/{len(sorted_films)} films scraped')
        self.latest_log_datetime = datetime.datetime.now()

    def _retrieve(self, url):
        cache = self._get_cache()
        content = cache.get(url)
        if content is None:
            retriever = self._get_retriever()
            content = retriever.retrieve(url)
            cache.set(url, content)

        return content

    def _get_cache(self):
        if self.cache_path is None:
            return ObjectFactory().get_instance(CacheInterface)
        return ObjectFactory().get_instance(CacheInterface, self.cache_path)

    def _get_retriever(self):
        if self.wait_time_between_calls_in_seconds is None:
            return ObjectFactory().get_instance(WebPageRetrieverInterface)
        return ObjectFactory().get_instance(WebPageRetrieverInterface, self.wait_time_between_calls_in_seconds)

    @staticmethod
    def get_info():
        file_cache = ObjectFactory().get_instance(CacheInterface)
        return file_cache.get_info()

    def export_to_json(self, filename):
        import json
        with open(filename, 'w') as file:
            json.dump(self.tropes_by_film, file)
        self.logger.info(f'Saved dictionary <film_name> -> [<trope_list>] as JSON file {filename}')

    def log_summary(self):
        films_count = len(self.tropes_by_film.keys())
        tropes_count = len(self.tropes)
        self.logger.info(f'Summary:\n- Films: {films_count}\n- Tropes: {tropes_count}\n- Cache: {self.get_info()}')
