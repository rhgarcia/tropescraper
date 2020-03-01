from typing import TypeVar, Type, List, Dict

from tropescraper.adaptors.file_cache import FileCache
from tropescraper.adaptors.file_store import FileStore
from tropescraper.adaptors.web_page_retriever import WebPageRetriever
from tropescraper.interfaces.cache_interface import CacheInterface
from tropescraper.interfaces.tropes_store_interface import TropesStoreInterface
from tropescraper.interfaces.web_page_retriever_interface import WebPageRetrieverInterface


class ObjectFactory(object):
    DEFAULT_IMPLEMENTATION_MAP = {
        WebPageRetrieverInterface: WebPageRetriever,
        CacheInterface: FileCache,
        TropesStoreInterface: FileStore,
    }
    MOCK_IMPLEMENTATION_MAP = {}

    def __init__(self):
        pass

    T = TypeVar('T')

    def get_instance(self, interface: Type[T], *args: List, **kwargs: Dict) -> T:
        if interface in self.MOCK_IMPLEMENTATION_MAP:
            return self.MOCK_IMPLEMENTATION_MAP[interface](*args, **kwargs)
        return self.DEFAULT_IMPLEMENTATION_MAP[interface](*args, **kwargs)

    def install_mock(self, interface, implementation):
        self.MOCK_IMPLEMENTATION_MAP[interface] = implementation

    def clean_mocks(self):
        self.MOCK_IMPLEMENTATION_MAP.clear()
