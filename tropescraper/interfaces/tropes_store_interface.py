from abc import abstractmethod


class TropesStoreInterface(object):
    @abstractmethod
    def store(self):
        pass
