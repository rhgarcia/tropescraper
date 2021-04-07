from lxml import html


class TVTropesParser(object):
    FILM_MAIN_SEARCH = 'https://tvtropes.org/pmwiki/pmwiki.php/Main/Film'
    TROPES_MAIN_SEARCH = 'https://tvtropes.org/pmwiki/pmwiki.php/Main/Tropes'

    BASE_FILM_URL = 'https://tvtropes.org/pmwiki/pmwiki.php/Film/'
    BASE_MAIN_URL = 'https://tvtropes.org/pmwiki/pmwiki.php/Main/'
    BASE_LINK_URL = 'https://tvtropes.org/'

    MAIN_RESOURCE = '/Main/'
    FILM_RESOURCE = '/Film/'
    LINK_SELECTOR = 'a'
    LINK_SELECTOR_INSIDE_ARTICLE = '#main-article ul li a'
    LINK_ADDRESS_SELECTOR = 'href'
    MEDIA_TYPES_NOT_TROPES = {'Advertising', 'AdvertisingCampaigns', 'Anime', 'AsianAnimation',
                              'EasternEuropeanAnimation', 'WesternAnimation', 'PhotographyAndIllustration',
                              'SequentialArt', 'MusicAndSoundEffects', 'AudioPlay', 'ConceptAlbum', 'AlbumsIndex',
                              'OralTradition', 'Podcast', 'Radio', 'RockOperas', 'AnimatedFilms', 'FilmSeries',
                              'Newsreel', 'ShortFilm', 'AlternateRealityGame', 'ARG', 'LARP', 'ParlorGames', 'Pinball',
                              'TabletopGames', 'BoardGames', 'CardGames', 'CollectibleCardGame', 'DeckbuildingGame',
                              'TabletopRPG', 'WarGaming', 'TabletopGames', 'VideoGames', 'Feelies', 'Machinima',
                              'Machinomics', 'VisualNovel', 'TheInternet', 'Fora', 'FriendingNetwork', 'LetsPlay',
                              'TheWikiRule', 'OnlineGames', 'VirtualWorlds', 'WebAnimation', 'WebComics', 'WebGames',
                              'Blog', 'WebOriginal', 'WebOriginalFiction', 'WebSerialNovel', 'WebVideo', 'OtherSites',
                              'PrintMedia', 'ComicBooks', 'Literature', 'LightNovels', 'Magazines', 'Manga', 'Manhua',
                              'Manhwa', 'Newspapers', 'NewspaperComics', 'PictureBooks', 'SchoolStudyMedia',
                              'SportingEvent', 'RecordedAndStandUpComedy', 'AnimatedShows', 'BroadcastLive',
                              'TelevisionMovieIndex', 'Series', 'Theatre', 'Ballet', 'Opera', 'Vaudeville',
                              'ThemeParks', 'Toys', 'FairyTale', 'FranchiseIndex', 'Legend', 'Mythology',
                              'Analysis', 'UsefulNotes', 'Recap', 'WMG', 'VideoExamples','FanficRecs',
                              'HoYay'}

    def get_films_starting_url(self):
        return self.FILM_MAIN_SEARCH

    def get_tropes_starting_url(self):
        return self.TROPES_MAIN_SEARCH

    def extract_categories(self, page):
        return self._get_links_from_page(page, self.MAIN_RESOURCE)

    def get_category_url(self, category_id):
        return self.BASE_MAIN_URL + category_id

    def extract_films(self, category_page):
        return self._get_links_from_page(category_page, self.FILM_RESOURCE)

    def get_film_url(self, film_id):
        return self.BASE_FILM_URL + film_id

    def get_link_url(self, link):
        if link.startswith("https://"):
            return link
        if link.startswith('/'):
            link = link[1:]
        return self.BASE_LINK_URL + link

    def extract_tropes_from_film_page(self, page):
        return self._get_links_from_page(page, self.MAIN_RESOURCE, only_article=True)

    def extract_films_from_trope_page(self, page):
        return self._get_links_from_page(page, self.FILM_RESOURCE, only_article=True)

    def get_all_trope_links_and_paginations(self, page, trope_name):
        if self.trope_name_is_media_type_to_ignore(trope_name):
            return [], []

        links = self._get_links_from_page(page, self.MAIN_RESOURCE, only_article=True, remove_link=False,
                                          sub_pages=False)
        links += self._get_links_from_page(page, '.php/{}/'.format(trope_name), only_article=True, remove_link=False,
                                           sub_pages=False)
        films = self.extract_films_from_trope_page(page)
        # TODO: retrieve paginations (see https://tvtropes.org/pmwiki/pmwiki.php/Main/BoxOfficeBomb)
        return links, films

    def _get_links_from_page(self, page, link_type, only_article=False, remove_link=True, sub_pages=False):
        tree = html.fromstring(page)
        selector = self.LINK_SELECTOR_INSIDE_ARTICLE if only_article else self.LINK_SELECTOR
        links = [element.get(self.LINK_ADDRESS_SELECTOR) for element in tree.cssselect(selector)
                 if element.get(self.LINK_ADDRESS_SELECTOR)]

        filtered_links = [link for link in links if link_type in link and 'action' not in link]
        if sub_pages:
            filtered_links += [link for link in links if 'NumbersThrough' in link and 'action' not in link]
        return list(map(lambda x: x.split('/')[-1] if remove_link else x, filtered_links))

    @classmethod
    def trope_name_is_media_type_to_ignore(cls, trope_name):
        return trope_name in cls.MEDIA_TYPES_NOT_TROPES
