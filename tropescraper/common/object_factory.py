from tropescraper.adaptors.file_cache import FileCache
from tropescraper.adaptors.tvtropes_parser import TVTropesParser
from tropescraper.adaptors.web_page_retriever import WebPageRetriever
from tropescraper.interfaces.cache_interface import CacheInterface
from tropescraper.interfaces.page_parser_interface import PageParserInterface
from tropescraper.interfaces.web_page_retriever_interface import WebPageRetrieverInterface


class ObjectFactory(object):
    DEFAULT_IMPLEMENTATION_MAP = {
        WebPageRetrieverInterface: WebPageRetriever,
        CacheInterface: FileCache,
        PageParserInterface: TVTropesParser
    }
    MOCK_IMPLEMENTATION_MAP = {}

    def __init__(self):
        pass

    def get_instance(self, interface, *args, **kwargs):
        if interface in self.MOCK_IMPLEMENTATION_MAP:
            return self.MOCK_IMPLEMENTATION_MAP[interface](*args, **kwargs)
        return self.DEFAULT_IMPLEMENTATION_MAP[interface](*args, **kwargs)

    def install_mock(self, interface, implementation):
        self.MOCK_IMPLEMENTATION_MAP[interface] = implementation

    def clean_mocks(self):
        self.MOCK_IMPLEMENTATION_MAP.clear()
