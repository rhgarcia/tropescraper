import datetime
import logging
import re
import sys
from collections import OrderedDict

from tropescraper.common.object_factory import ObjectFactory
from tropescraper.interfaces.cache_interface import CacheInterface
from tropescraper.interfaces.page_parser_interface import PageParserInterface
from tropescraper.interfaces.tropes_store_interface import TropesStoreInterface
from tropescraper.interfaces.web_page_retriever_interface import WebPageRetrieverInterface
from tropescraper.use_cases.parsers.tvtropes_parser import TVTropesParser


class ScrapeTropesUseCase(object):
    logger = logging.getLogger(__name__)

    def __init__(self, file_name, wait_time_between_calls_in_seconds=None, cache_path=None):
        self._file_name = file_name
        self.wait_time_between_calls_in_seconds = wait_time_between_calls_in_seconds
        self.cache_path = cache_path
        self._initial_recursivity = 1000000

        self.films = None
        self._all_trope_urls = set()
        self.tropes = None
        self.tropes_by_film = OrderedDict()
        self.latest_log_datetime = None

        self.cache_interface = CacheInterface
        self.page_parser_interface = PageParserInterface
        self.page_retriever_interface = WebPageRetrieverInterface
        self.tropes_store_interface = TropesStoreInterface
        self.object_factory = ObjectFactory

        self.parser = TVTropesParser()
        self._cache = None

    def run(self):
        self._log_instructions()
        self._extract_film_ids()
        self._extract_tropes()
        self._extract_trope_ids_and_link_films()
        self._export_to_json()
        self._log_summary()

        return self.tropes_by_film

    def _log_instructions(self):
        self.logger.info('Process started\n* Remember that you can stop and restart at any time.\n'
                         '** Please, remove manually the cache folder when you are done\n')

    def _extract_film_ids(self):
        self.logger.info('Scraping film ids...')

        self.films = set()
        starting_url = self.parser.get_films_starting_url()
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
            trope_ids = self.parser.extract_tropes_from_film_page(page)

            self.logger.debug(f'Film {film} ({len(trope_ids)} tropes): {trope_ids}')

            self.tropes.update(trope_ids)
            self.tropes_by_film[film] = sorted(trope_ids)

            if self._should_log_status():
                self._log_status(counter, sorted_films)

    def _extract_trope_ids_and_link_films(self):
        self.logger.info('Scraping trope ids...')

        starting_url = self.parser.get_tropes_starting_url()
        page = self._retrieve(starting_url)

        self._all_trope_urls = set()
        self._all_trope_urls.add(starting_url)

        sys.setrecursionlimit(10 ** 6)
        self.extract_all_tropes_in_page_recursively(page, 'tropes', recursivity_level=self._initial_recursivity)
        for film, tropes in self.tropes_by_film.items():
            self.tropes_by_film[film] = sorted(list(set(tropes)))

        self.logger.info(f'Found {len(self._all_trope_urls)} tropes')

    def _should_log_status(self):
        now = datetime.datetime.now()
        return self.latest_log_datetime is None or now - self.latest_log_datetime > datetime.timedelta(seconds=5)

    def _log_status(self, counter, total_elements_list=None, item_name_plural='films'):
        total = float('inf') if total_elements_list is None else len(total_elements_list)

        values = list(map(lambda x: len(x), self.tropes_by_film.values()))
        average = sum(values) / len(values)
        self.logger.info(f'Status: {counter + 1}/{total} {item_name_plural} scraped. '
                         f'Average tropes by film: {average}')
        self.latest_log_datetime = datetime.datetime.now()

    def _retrieve(self, url):
        if self._cache is None:
            if self.cache_path is None:
                self._cache = ObjectFactory().get_instance(CacheInterface)
            else:
                self._cache = ObjectFactory().get_instance(CacheInterface, self.cache_path)

        content = self._cache.get(url)
        if content is None:
            retriever = self._get_retriever()
            content = retriever.retrieve(url)
            self._cache.set(url, content)

        return content

    def _get_retriever(self):
        if self.wait_time_between_calls_in_seconds is None:
            return ObjectFactory().get_instance(WebPageRetrieverInterface)
        return ObjectFactory().get_instance(WebPageRetrieverInterface, self.wait_time_between_calls_in_seconds)

    def _export_to_json(self):
        store = ObjectFactory().get_instance(TropesStoreInterface, self._file_name, self.tropes_by_film)
        store.store()

    def _log_summary(self):
        films_count = len(self.tropes_by_film.keys())
        tropes_count = len(self.tropes)
        self.logger.info(f'Summary:\n- Films: {films_count}\n- Tropes: {tropes_count}\n- Cache: {self._get_info()}')

    @staticmethod
    def _get_info():
        file_cache = ObjectFactory().get_instance(CacheInterface)
        return file_cache.get_info()

    def extract_all_tropes_in_page_recursively(self, page, trope_name, recursivity_level):
        recursivity_level -= 1

        self.logger.info( f"Working with {trope_name}" )
        
        if page == '':
            self.logger.info( f"Page is empty for {trope_name}")
            return
        
        links, films = self.parser.get_all_trope_links_and_paginations(page, trope_name)
        for film in films:
            if film in self.tropes_by_film:
                self.tropes_by_film[film].append(trope_name)

        if self._should_log_status():
            self._log_status(len(self._all_trope_urls), item_name_plural='tropes')

        if recursivity_level <= 0:
            return

        filtered_links = []
        for link in links:
            full_link = self.parser.get_link_url(link)
            if full_link in self._all_trope_urls:
                # self.logger.warning(f'Link already visited: {full_link}')
                pass
            else:
                filtered_links.append(full_link)
                self._all_trope_urls.add(full_link)

        if self._should_log_status():
            self._log_status(len(self._all_trope_urls), item_name_plural='tropes')

        for full_link in filtered_links:
            if 'CircularRedirect' in full_link or 'ThisPageRedirectsToItself' in full_link:
                return []

            matches = re.match('^https://tvtropes.org/pmwiki/pmwiki.php/Main/([^/]+)(/.*)?$', full_link)
            if not matches:
                matches = re.match('^https://tvtropes.org/pmwiki/pmwiki.php/pmwiki.php/([^/]+)/.*$', full_link)
                if not matches:
                    self.logger.warning('Could not get the trope name in url {}'.format(full_link))
                    return

            subtrope = matches.group(1)
            category = full_link.split('/')[-1]
            if (not self.parser.trope_name_is_media_type_to_ignore(subtrope)
                    and not self.parser.trope_name_is_media_type_to_ignore(category)):

                if subtrope != category and category in self.tropes_by_film:
                    self.logger.info(f'URL encoded trope-film relation ({subtrope}=>{category}): {full_link}')
                    self.tropes_by_film[category].append(subtrope)
                else:
                    page = self._retrieve(full_link)
                    if page is not None:
                        self.extract_all_tropes_in_page_recursively(page, subtrope, recursivity_level)
