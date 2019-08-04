from abc import abstractmethod


class WebPageRetrieverInterface(object):
    @abstractmethod
    def retrieve(self, url):
        pass
