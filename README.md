# simple-web-crawler

[![CircleCI](https://circleci.com/gh/mescanef/simple-web-crawler/tree/master.svg?style=svg)](https://circleci.com/gh/mescanef/simple-web-crawler/tree/master)

Goal of this project is to have implemented a Simple Web Crawler as a PoC by using few 
different technologies (Python+Scrapy, Java+htmlUnit, ...). 
For now only python-based implementation is available, which uses Scrapy and Splash 
components.

## python-crawler

Python based (2.7.x) script that underneath uses Scrapy for the scraping activities, and 
Splash, the lightweight web browser, for rendering web pages in order to act as a 
'real-user'. Since today many of web pages are JS/Ajax based, it is worth to have such 
implementation, in order to not miss some of "hidden" content like links, just because of 
missing JavaScript support.

### Setup&Run

Install Python 2.7, virtualenv and perform the following steps:

```
$ virtualenv venv
$ . venv/bin/activate
$ python setup.py install
```

Make Splash running. Recommended way is to run it as a Docker container:

```
$ docker run -p 8050:8050 scrapinghub/splash --disable-browser-caches
```

Now with all that dependencies, run the crawler:

```
$ venv/bin/simple-web-crawler -d example.com
```

Output with all crawled links will be present in the `log` file, which by default is
written into the current working directory. Example:

```
$ cat simple-web-crawler-1553059123.0.log
http://www.iana.org/domains/example
```

### Tests

In order to run tests, the most efficient way is to use `tox` as it will execute:
- `flake8`,
- `pycodestyle`,
- `bandit`
against the package sources and, in the end, will execute the `py.test` to run the
unit tests.
Running tests via `tox` is straightforward:

```
$ cd python-crawler && tox
```

### TODOs

- Implement parsing of the external CSS, in order to extract links from *background-image*
  property or similar, by taking content of *url('static/example.png')*,
- Better exception handling,
- Improved final list of URls - links should be normalized against more complex situations,
- Integration test cases.
