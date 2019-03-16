# -*- coding: utf-8 -*-

import scrapy


class SimpleWebCrawler(scrapy.Spider):
    """ A definition of a Scrapy spider. It holds the crawler's logic on how exactly parse the crawled web page

    """
    name = 'generic'

    def parse(self, response):
        """ Scrapy's parse method parses the received response from the entity.
        Parse result - a list of found URLs on a web site - is stored in the file.

        """
        urls = response.xpath('//a[starts-with(@href, "") and not(contains(@href,"#"))]/@href').extract()
        with open('/tmp/simple-web-crawler.log', "w") as file:
            for url in urls:
                file.write("%s" %url)
