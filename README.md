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

The script ~~can take some hours~~ can take a long time, from hours to days, 
to finish, but don't worry, 
it can be stopped at any moment because it relies in file cache, so
it will not try to re-download the same page twice even in 
different executions. You will notice because you will see 
thousands of "Cache hits" with the format:
```
INFO:tropescraper.adaptors.file_cache:Cache hit for https://tvtropes.org/pmwiki/pmwiki.php/Main/RulesOfTheRoad
```

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

### Dealing with unstructured data

The first version of the script considered that:
- all the film categories are listed in the ["Films"](https://tvtropes.org/pmwiki/pmwiki.php/Main/Film) section and
- every film page includes a list of the tropes that can be found inside, for example, 
["Raiders of the lost ark"](https://tvtropes.org/pmwiki/pmwiki.php/Film/RaidersOfTheLostArk)
includes a links to tropes such as ["Animal Espionage"](https://tvtropes.org/pmwiki/pmwiki.php/Main/AnimalEspionage).

It is "very" direct to build the films->tropes map and we got ~12567 films scraped with ~40 tropes on average.

However, we discovered that some of the most popular tropes in DBTropes were missing 
in tropescraper, and this is because of the unstructured nature of the wiki.

The next version of the script considers that: 
- all the trope-categories are hanging from the ["Tropes"](https://tvtropes.org/pmwiki/pmwiki.php/Main/Tropes) section or 
a sub-page, in a recursive way, and
- every trope page includes a list of the films that make use of it, for example,
["Animal Espionage"](https://tvtropes.org/pmwiki/pmwiki.php/Main/AnimalEspionage) 
includes a links to tropes such as ["Raiders of the lost ark"](https://tvtropes.org/pmwiki/pmwiki.php/Film/RaidersOfTheLostArk).
- some tropes do not include the films directly, but through category subpages
or paginated results hence the script needs to crawl pages that do not include "Main" 
or "Film".

The assumptions above imply that the crawl is more intense now.

Considering all the new relations discovered, the average number of tropes by film goes up to ~104.
Whilst the number of tropes and films do not grow much (on 2020/03, 12567 films and 26969 tropes)
the dataset doubles the dense¡ity in term of relations.


** Manual checks:

Due to the very nature of the wiki, it is hard to evaluate if we are missing films,
tropes or relations. The code includes some basic integration tests.

Also, some manual tests are covered:

- [x] a trope listed in a film page is linked to the film
- [x] a film listed in a trope page is linked to the trope:
For example, 'AHandfulForAnEye'->'RaidersOfTheLostArk' (but not the opposite)
- [x] a film listed in a category page inside a trope page is linked to the trope:
for example, 'BoxOfficeBomb'->'CThroughD'->'AChineseGhostStory'

### The log

The output should look like this:
```log
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

As result of improving the accuracy of the dataset by performing a hard-crawl of the
tropes and sub-pages, the process can take longer and it is
impossible to predict when the crawl will end. For this reason, a new log is included
periodically to let you know how things are going:

```
INFO:tropescraper.use_cases.scrape_tropes_use_case:Status: 94645/inf tropes scraped. Average tropes by film: 104.3337312007639
```

Apart from this, ths output is not really interesting unless
anything goes bad :-) and it can be ignored.
 

## Work with the original code

If you are a contributor and you want to work and improve the code
you only need clone the project and install all the dependencies with:

```bash
git clone https://github.com/raiben/tropescraper.git
cd tropescraper
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