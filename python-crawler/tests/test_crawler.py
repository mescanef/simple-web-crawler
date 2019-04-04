# -*- coding: utf-8 -*-
"""Holds the logic of the crawler unit tests."""

import os
import unittest
from urlparse import urlparse

from scrapy.http import TextResponse

from simple_web_crawler import crawler


class CrawlerTestCase(unittest.TestCase):
    """A definition of a CrawlerTestCase class.

    Has the unit test definitions for the most important crawler's method.

    """

    testUrlFile = os.path.join(os.path.dirname(__file__), 'testLogFile.log')
    kargs = {"log_file_path": testUrlFile}
    crawl = crawler.SimpleWebCrawler(**kargs)

    def test_normalizedUrl(self):
        """Tests the normalizedUrl method."""
        randomUrlLst = ["/test/object01",
                        "//external-site.com",
                        ' http://some-site.com'
                        ]
        normalizedLst = ['http://example.com/test/object01',
                         'http://external-site.com',
                         'http://some-site.com'
                         ]
        base_url = "http://example.com"
        uri = urlparse(base_url)

        assert self.crawl.normalizeUrl(randomUrlLst, uri) == normalizedLst, \
            "Wrongly normalized"

    def test_parse(self):
        """Tests the parse method."""
        crawl = crawler.SimpleWebCrawler()
        startUrl = "http://some-very-example.com"
        body = "<html><body>this is example for tests. more at " \
               "<a href=\"example\">example</a></body></html>"
        response = TextResponse(startUrl,
                                headers={'Content-Type': 'text/html'},
                                body=body)
        parsedResponse = crawl.parse(response)
        for genItem in parsedResponse:
            assert repr(genItem) == "<GET " \
                                    "http://some-very-example.com/example>"

    def test_wrieToDisk_and_closed(self):
        """Tests the writeToDisk and closed methods."""
        urlLst = ['http://site-1.com',
                  'http://example-site.com',
                  'http://example.com/about',
                  'http://example.com/about'
                  ]
        self.crawl.writeToDisk(urlLst, 'w')

        with open(self.testUrlFile, 'r') as f:
            fileRead = list(f.read().splitlines())

        assert fileRead == urlLst
        self.crawl.closed()
        # remove last item as its duplicate
        urlLst = urlLst[:-1]
        with open(self.testUrlFile, 'r') as f:
            fileRead = list(f.read().splitlines())
        assert fileRead == list(set(urlLst))
