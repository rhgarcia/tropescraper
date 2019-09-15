[![Project status](https://travis-ci.com/raiben/tropescraper.svg?branch=master)](https://travis-ci.com/raiben/tropescraper)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/raiben/tropescraper.svg)](https://github.com/raiben/tropescraper/blob/master/LICENSE)
[![Github all releases](https://img.shields.io/github/downloads/raiben/tropescraper/total.svg)](https://GitHub.com/raiben/tropescraper/releases/)
[![GitHub issues](https://img.shields.io/github/issues/raiben/tropescraper.svg)](https://GitHub.com/Naereen/raiben/tropescraper/)
[![PyPI version](https://badge.fury.io/py/tropescraper.svg)](https://badge.fury.io/py/tropescraper)

# tropescraper

A tool to scrape all the films and their tropes 
from the website TV Tropes.

## Requirements

This tool uses python >= 3.6 

## Install as library

If you want to use this tool, you don't need to download the sources
or clone the repository. Just install the latest version through PyPi:
```
pip install tropescraper
```
This will create an executable called `scrape-tvtropes`

## Running the executable

Try to execute
```
scrape-tvtropes
```

The script can take some hours to finish, but don't worry, 
it can be stopped at any moment because it relies in file cache, so
it will not try to re-download the same page twice even in 
different executions.

The script will create a folder in the same directory called `scraper_cache`
with thousand of small compressed files. 

When the script finishes, you will also see a file called `tvtropes.json`
with a JSON content in the following format:

```json
{
  "film_identifier":[
    "trope_identifier", 
    "trope_identifier"
  ],
  ...
}, 
```

### The log


The output should look something close to:
```bash
INFO:tropescraper.tvtropes_scraper:Process started
* Remember that you can stop and restart at any time.
** Please, remove manually the cache folder when you are done

INFO:tropescraper.tvtropes_scraper:Scraping film ids...
INFO:tropescraper.adaptors.file_cache:Building cache directory: ./scraper_cache
INFO:tropescraper.adaptors.file_cache:Cache miss for https://tvtropes.org/pmwiki/pmwiki.php/Main/Film
INFO:tropescraper.adaptors.file_cache:Cache set for https://tvtropes.org/pmwiki/pmwiki.php/Main/Film
INFO:tropescraper.adaptors.file_cache:Cache miss for https://tvtropes.org/pmwiki/pmwiki.php/Main/Tropes
INFO:tropescraper.adaptors.file_cache:Cache set for https://tvtropes.org/pmwiki/pmwiki.php/Main/Tropes
...
...
INFO:tropescraper.adaptors.file_cache:Cache set for https://tvtropes.org/pmwiki/pmwiki.php/Film/ZyzzyxRoad
INFO:tropescraper.tvtropes_scraper:Saved dictionary <film_name> -> [<trope_list>] as JSON file tvtropes.json
INFO:tropescraper.tvtropes_scraper:Summary:
- Films: 12147
- Tropes: 26479
- Cache: CacheInformation(size=179513467, files_count=12290, 
  creation_date=datetime.datetime(2019, 9, 15, 14, 59, 2))
```

The tool is verbose so you can know the progress and estimate the
duration of the process. You will be able to see a message
in the form `Status: {film_index}/{total} films scraped`.

Apart from this, ths output is not really interesting unless
anything goes bad :-) and it can be ignored.


## Work with the original code

If you are a contributor and you want to work and improve the code
you only need clone the project and install all the dependencies with:

```
pip install -r requirements.txt
```

To build the module, 

1. Don't forget to modify the version in setup.py
according to the standard [Semantic Versioning](https://semver.org/).

2. Then, just run in the project folder:
```bash
python3 setup.py sdist bdist_wheel
pip install dist/tropescraper-<version>.tar.gz
```