from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(name='tropescraper',
      version='1.1.0',
      description='A TvTropes scrapper',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/rhgarcia/tropescraper',
      author='Rubén H. García',
      author_email='4012515+rhgarcia@users.noreply.github.com',
      license='LGPL',
      packages=['tropescraper', 'tropescraper.adaptors', 'tropescraper.common', 'tropescraper.entities',
                'tropescraper.interfaces', 'tropescraper.use_cases', 'tropescraper.use_cases.parsers'],
      install_requires=['requests', 'lxml', 'cssselect'],
      scripts=['bin/scrape-tvtropes'],
      zip_safe=False)
