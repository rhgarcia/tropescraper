import datetime
import logging
import os
from collections import OrderedDict

from lxml import html

from tropescraper.web_page_retriever import WebPageRetriever


class TVTropesScraper(object):
    MAIN_SEARCH = 'https://tvtropes.org/pmwiki/pmwiki.php/Main/Film'
    BASE_FILM_URL = 'https://tvtropes.org/pmwiki/pmwiki.php/Film/'
    BASE_MAIN_URL = 'https://tvtropes.org/pmwiki/pmwiki.php/Main/'

    MAIN_RESOURCE = '/Main/'
    FILM_RESOURCE = '/Film/'
    LINK_SELECTOR = 'a'
    LINK_SELECTOR_INSIDE_ARTICLE = '#main-article ul li a'
    LINK_ADDRESS_SELECTOR = 'href'

    DEFAULT_CACHE_PATH = './scraper_cache'
    DEFAULT_WAIT_TIME = 0.5

    logger = logging.getLogger(__name__)

    def __init__(self, wait_time_between_calls_in_seconds=DEFAULT_WAIT_TIME, cache_path=DEFAULT_CACHE_PATH):
        self.wait_time_between_calls_in_seconds = wait_time_between_calls_in_seconds
        self.cache_path = cache_path
        self.films = None
        self.tropes = None
        self.urls = None
        self.tropes_by_film = OrderedDict()
        self.latest_log_datetime = None

    def get_tropes(self):
        self.logger.info('Process started\n* Remember that you can stop and restart at any time.\n'
                         '** Please, remove manually the cache folder when you are done\n')

        self._build_cache_directory()
        self._extract_film_ids()
        self._extract_tropes()

        return self.tropes_by_film

    def _build_cache_directory(self):
        if not os.path.isdir(self.cache_path):
            self.logger.info(f'Building cache directory: {self.cache_path}')
            os.makedirs(self.cache_path)
        else:
            self.logger.info(f'Cache directory found: {self.cache_path}')

    def _extract_film_ids(self):
        self.logger.info('Scraping film ids...')

        self.films = set()
        self.urls = set()

        category_ids = self._get_links_from_url(self.MAIN_SEARCH, self.MAIN_RESOURCE)

        for category_id in category_ids:
            url = self.BASE_MAIN_URL + category_id
            film_ids = self._get_links_from_url(url, self.FILM_RESOURCE)
            self.films.update(film_ids)

        self.logger.info(f'Found {len(self.films)} films')

    def _extract_tropes(self):
        self.logger.info('Scraping tropes (this might take a while...)')

        self.tropes = set()
        self.tropes_by_film = OrderedDict()
        sorted_films = sorted(list(self.films))

        self.logger.debug(f'Found {len(sorted_films)} films')

        for counter, film in enumerate(sorted_films):
            self._get_tropes_by_film(film)

            if self._should_log_status():
                self.logger.info(f'Status: {counter + 1}/{len(sorted_films)} films scraped')
                self.latest_log_datetime = datetime.datetime.now()

    def _get_tropes_by_film(self, film):
        url = self.BASE_FILM_URL + film
        trope_ids = self._get_links_from_url(url, self.MAIN_RESOURCE, only_article=True)

        self.logger.debug(f'Film {film} ({len(trope_ids)} tropes): {trope_ids}')

        self.tropes.update(trope_ids)
        self.tropes_by_film[film] = sorted(trope_ids)

    def _get_links_from_url(self, url, link_type, only_article=False):
        retriever = WebPageRetriever(self.wait_time_between_calls_in_seconds, url, self.cache_path)
        page = retriever.retrieve()
        tree = html.fromstring(page)
        selector = self.LINK_SELECTOR_INSIDE_ARTICLE if only_article else self.LINK_SELECTOR
        links = [element.get(self.LINK_ADDRESS_SELECTOR) for element in tree.cssselect(selector)
                 if element.get(self.LINK_ADDRESS_SELECTOR)]
        return [link.split('/')[-1] for link in links if link_type in link and 'action' not in link]

    def get_info(self):
        retriever = WebPageRetriever(self.wait_time_between_calls_in_seconds, None, self.cache_path)
        return retriever.get_info()

    def export_to_json(self, filename):
        import json
        with open(filename, 'w') as file:
            json.dump(self.tropes_by_film, file)
        self.logger.info(f'Saved dictionary <film_name> -> [<trope_list>] as JSON file {filename}')

    def log_summary(self):
        films_count = len(self.tropes_by_film.keys())
        tropes_count = len(self.tropes)
        self.logger.info(f'Summary:\n- Films: {films_count}\n- Tropes: {tropes_count}\n- Cache: {self.get_info()}')

    def _should_log_status(self):
        now = datetime.datetime.now()
        return self.latest_log_datetime is None or now - self.latest_log_datetime > datetime.timedelta(seconds=5)
