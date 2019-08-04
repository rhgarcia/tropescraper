from abc import abstractmethod


class CacheInterface(object):

    @abstractmethod
    def get(self, url):
        pass

    @abstractmethod
    def set(self, url, content):
        pass

    @abstractmethod
    def get_info(self):
        pass
