import base64
import bz2
import logging
import os
from datetime import datetime
from time import ctime

from tropescraper.entities.cache_information_entity import CacheInformation
from tropescraper.interfaces.cache_interface import CacheInterface


class FileCache(CacheInterface):
    DEFAULT_ENCODING = 'utf-8'
    EXTENSION = '.html'
    COMPRESSED_EXTENSION = '.bz2'
    DEFAULT_CACHE_PATH = './scraper_cache'

    logger = logging.getLogger(__name__)

    def __init__(self, cache_path=DEFAULT_CACHE_PATH):
        self.cache_path = cache_path
        if not os.path.isdir(self.cache_path):
            self.logger.info(f'Building cache directory: {self.cache_path}')
            os.makedirs(self.cache_path)

    def get(self, url):
        encoded_url = self._build_encoded_url(url)
        file_path = os.path.join(self.cache_path, encoded_url)
        if not self._file_exists(file_path):
            self.logger.info(f'Cache miss for {url}')
            return None

        self.logger.info(f'Cache hit for {url}')
        content = self._read_file(file_path)
        return content.decode('utf-8')

    def _build_encoded_url(self, url):
        encoded_url = base64.b64encode(url.encode(self.DEFAULT_ENCODING)).decode(self.DEFAULT_ENCODING) + self.EXTENSION
        return encoded_url.replace('/', '_')

    @classmethod
    def _file_exists(cls, file_path):
        compressed_path = f'{file_path}{cls.COMPRESSED_EXTENSION}'
        return os.path.isfile(compressed_path)

    @classmethod
    def _read_file(cls, file_path):
        compressed_path = f'{file_path}{cls.COMPRESSED_EXTENSION}'
        with open(compressed_path, 'rb') as file:
            content = file.read()
        return bz2.decompress(content)

    def set(self, url, content):
        encoded_url = self._build_encoded_url(url)
        self.logger.info(f'Cache set for {url}')
        file_path = os.path.join(self.cache_path, encoded_url)
        encoded_content = content.encode('utf-8')
        self._write_file(file_path, encoded_content)

    @classmethod
    def _write_file(cls, file_path, content):
        compressed_path = f'{file_path}{cls.COMPRESSED_EXTENSION}'
        compressed_content = bz2.compress(content)
        with open(compressed_path, 'wb') as file:
            file.write(compressed_content)

    def get_info(self):
        try:
            files = [os.path.join(self.cache_path, file) for file in os.listdir(self.cache_path)]
            size = sum(os.path.getsize(file) for file in files if os.path.isfile(file))
            files_count = len(files)
            creation_date_as_text = ctime(os.path.getctime(self.cache_path))
            creation_date = datetime.strptime(creation_date_as_text, "%a %b %d %H:%M:%S %Y")
            return CacheInformation(size=size, files_count=files_count, creation_date=creation_date)
        except Exception as exception:
            self.logger.error(exception)
            return CacheInformation(size=0, files_count=0, creation_date=None)
