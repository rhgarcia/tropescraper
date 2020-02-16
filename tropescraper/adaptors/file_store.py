import logging
from tropescraper.interfaces.tropes_store_interface import TropesStoreInterface
import json


class FileStore(TropesStoreInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, filename, content):
        self.filename = filename
        self.content = content

    def store(self):
        self.logger.info(f'Saving dictionary <film_name> -> [<trope_list>] as JSON file {self.filename}')
        with open(self.filename, 'w') as file:
            json.dump(self.content, file)
