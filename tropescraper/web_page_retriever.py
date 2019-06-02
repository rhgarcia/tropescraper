import base64
import bz2
import logging
import os
from datetime import datetime
from time import sleep, ctime
from collections import namedtuple

import requests

CacheInformation = namedtuple('CacheInformation', ['size', 'files_count', 'creation_date'])


class WebPageRetriever(object):
    DEFAULT_ENCODING = 'utf-8'
    EXTENSION = '.html'
    COMPRESSED_EXTENSION = '.bz2'

    logger = logging.getLogger(__name__)

    def __init__(self, wait_time_between_calls_in_seconds, url, cache_path):
        self.wait_time_between_calls_in_seconds = wait_time_between_calls_in_seconds
        self.url = url
        self.cache_path = cache_path

    def retrieve(self):
        encoded_url = self._build_encoded_url(self.url)
        file_path = os.path.join(self.cache_path, encoded_url)

        if self._file_exists(file_path):
            self.logger.debug(f'Retrieving URL from cache: {self.url}')
            content = self._read_file(file_path)
            return self._read_content_safely(content)

        self.logger.debug(f'Retrieving URL from TVTropes and storing in cache: {self.url}')
        self._wait_between_calls()
        page = requests.get(self.url)
        content = page.content
        self._write_file(content, file_path)
        return self._read_content_safely(content)

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

    def _write_file(self, content, file_path):
        compressed_path = f'{file_path}{self.COMPRESSED_EXTENSION}'
        self.compressed_content = bz2.compress(content)
        with open(compressed_path, 'wb') as file:
            file.write(self.compressed_content)

    def _read_content_safely(self, content):
        return content.decode(self.DEFAULT_ENCODING, errors='ignore')

    def _build_encoded_url(self, url):
        encoded_url = base64.b64encode(url.encode(self.DEFAULT_ENCODING)).decode(self.DEFAULT_ENCODING) + self.EXTENSION
        return encoded_url.replace('/', '_')

    def _wait_between_calls(self):
        sleep(self.wait_time_between_calls_in_seconds)

    def get_info(self):
        files = [os.path.join(self.cache_path, file) for file in os.listdir(self.cache_path)]
        size = sum(os.path.getsize(file) for file in files if os.path.isfile(file))
        files_count = len(files)
        creation_date_as_text = ctime(os.path.getctime(self.cache_path))
        creation_date = datetime.strptime(creation_date_as_text, "%a %b %d %H:%M:%S %Y")
        return CacheInformation(size=size, files_count=files_count, creation_date=creation_date)
