import bz2
import os
import shutil
import tempfile
import unittest

from tropescraper.adaptors.file_cache import FileCache


class FileCacheTestCase(unittest.TestCase):
    URL_KEY = 'https://tvtropes.org/pmwiki/pmwiki.php/Main/Film'
    EXPECTED_CONTENT = 'test'
    UNEXPECTED_CONTENT = 'another'

    def setUp(self):
        self.temporal_directory_name = tempfile.mkdtemp()
        self.cache = FileCache(cache_path=self.temporal_directory_name)

    def tearDown(self) -> None:
        shutil.rmtree(self.temporal_directory_name)

    def test_get_when_key_found_then_returns_file_content(self):
        file_name = 'aHR0cHM6Ly90dnRyb3Blcy5vcmcvcG13aWtpL3Btd2lraS5waHAvTWFpbi9GaWxt.html.bz2'
        compressed_content = bz2.compress(self.EXPECTED_CONTENT.encode('utf-8'))
        full_path = os.path.join(self.temporal_directory_name, file_name)
        with open(full_path, 'wb') as cached_file:
            cached_file.write(compressed_content)

        retrieved_content = self.cache.get(self.URL_KEY)
        self.assertEqual(retrieved_content, self.EXPECTED_CONTENT, 'Should\'ve get the content')

    def test_get_when_key_not_found_then_returns_None(self):
        retrieved_content = self.cache.get(self.URL_KEY)
        self.assertIsNone(retrieved_content, 'Should\'ve retrieved None when the key is not found')

    def test_set_when_key_does_not_exist_then_sets_content_in_new_file(self):
        self.cache.set(self.URL_KEY, self.EXPECTED_CONTENT)

        file_name = 'aHR0cHM6Ly90dnRyb3Blcy5vcmcvcG13aWtpL3Btd2lraS5waHAvTWFpbi9GaWxt.html.bz2'
        full_path = os.path.join(self.temporal_directory_name, file_name)
        with open(full_path, 'rb') as cached_file:
            compressed_content = cached_file.read()
        content = bz2.decompress(compressed_content).decode('utf-8')
        self.assertEqual(content, self.EXPECTED_CONTENT, 'Should\'ve stored the content in the cache')

    def test_set_when_key_exists_then_file_content_updated(self):
        file_name = 'aHR0cHM6Ly90dnRyb3Blcy5vcmcvcG13aWtpL3Btd2lraS5waHAvTWFpbi9GaWxt.html.bz2'

        compressed_content = bz2.compress(self.UNEXPECTED_CONTENT.encode('utf-8'))
        full_path = os.path.join(self.temporal_directory_name, file_name)
        with open(full_path, 'wb') as cached_file:
            cached_file.write(compressed_content)

        self.cache.set(self.URL_KEY, self.EXPECTED_CONTENT)

        with open(full_path, 'rb') as cached_file:
            compressed_content = cached_file.read()
        content = bz2.decompress(compressed_content).decode('utf-8')
        self.assertEqual(content, self.EXPECTED_CONTENT, 'Should\'ve stored the content in the cache')
