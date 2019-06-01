from setuptools import setup

setup(name='tropescraper',
      version='0.1',
      description='A TvTropes scrapper',
      url='https://github.com/raiben/tropescraper',
      author='Rubén H. García',
      author_email='raiben@gmail.com',
      license='LGPL',
      packages=['tropescraper'],
      install_requires=['requests', 'lxml', 'cssselect'],
      scripts=['bin/scrape-tvtropes'],
      zip_safe=False)
