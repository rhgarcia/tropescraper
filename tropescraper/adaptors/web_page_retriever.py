import logging
from time import sleep
import requests

from tropescraper.interfaces.web_page_retriever_interface import WebPageRetrieverInterface


class WebPageRetriever(WebPageRetrieverInterface):
    DEFAULT_WAIT_TIME = 0.5
    logger = logging.getLogger(__name__)

    def __init__(self, wait_time_between_calls_in_seconds=DEFAULT_WAIT_TIME):
        self.wait_time_between_calls_in_seconds = wait_time_between_calls_in_seconds

    def retrieve(self, url):
        self.logger.debug(f'Retrieve URL from TVTropes: {url}')
        self._wait_between_calls()
        page = requests.get(url)
        return page.content.decode('utf-8', 'ignore')

    def _wait_between_calls(self):
        sleep(self.wait_time_between_calls_in_seconds)
