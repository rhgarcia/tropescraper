from lxml import html

from tropescraper.interfaces.page_parser_interface import PageParserInterface


class TVTropesParser(PageParserInterface):
    MAIN_SEARCH = 'https://tvtropes.org/pmwiki/pmwiki.php/Main/Film'
    BASE_FILM_URL = 'https://tvtropes.org/pmwiki/pmwiki.php/Film/'
    BASE_MAIN_URL = 'https://tvtropes.org/pmwiki/pmwiki.php/Main/'

    MAIN_RESOURCE = '/Main/'
    FILM_RESOURCE = '/Film/'
    LINK_SELECTOR = 'a'
    LINK_SELECTOR_INSIDE_ARTICLE = '#main-article ul li a'
    LINK_ADDRESS_SELECTOR = 'href'

    def get_starting_url(self):
        return self.MAIN_SEARCH

    def extract_categories(self, page):
        return self._get_links_from_url(page, self.MAIN_RESOURCE)

    def get_category_url(self, category_id):
        return self.BASE_MAIN_URL + category_id

    def extract_films(self, category_page):
        return self._get_links_from_url(category_page, self.FILM_RESOURCE)

    def get_film_url(self, film_id):
        return self.BASE_FILM_URL + film_id

    def extract_tropes(self, page):
        return self._get_links_from_url(page, self.MAIN_RESOURCE, only_article=True)

    def _get_links_from_url(self, page, link_type, only_article=False):
        tree = html.fromstring(page)
        selector = self.LINK_SELECTOR_INSIDE_ARTICLE if only_article else self.LINK_SELECTOR
        links = [element.get(self.LINK_ADDRESS_SELECTOR) for element in tree.cssselect(selector)
                 if element.get(self.LINK_ADDRESS_SELECTOR)]
        return [link.split('/')[-1] for link in links if link_type in link and 'action' not in link]
