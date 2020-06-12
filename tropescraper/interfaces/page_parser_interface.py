from abc import abstractmethod


class PageParserInterface(object):
    @abstractmethod
    def get_films_starting_url(self):
        pass

    @abstractmethod
    def get_tropes_starting_url(self):
        pass

    @abstractmethod
    def extract_categories(self, page):
        pass

    @abstractmethod
    def get_category_url(self, category_id):
        pass

    @abstractmethod
    def extract_films(self, category_page):
        pass

    @abstractmethod
    def get_film_url(self, film_id):
        pass

    @abstractmethod
    def extract_tropes_from_film_page(self, page):
        pass

    @abstractmethod
    def get_all_trope_links_and_paginations(self, page):
        pass

    @abstractmethod
    def _get_links_from_page(self, page, link_type, only_article=False):
        pass
