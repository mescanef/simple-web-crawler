# -*- coding: utf-8 -*-
"""Holds the logic of the crawler."""

import os
import re
import time
from urlparse import urlparse

import scrapy


class SimpleWebCrawler(scrapy.Spider):
    """A definition of a Scrapy spider. It holds the crawler's logic on how exactly parse the crawled web page."""

    name = 'generic'

    currentWorkingDir = os.getcwd()
    currentTime = time.mktime(time.gmtime())
    outFile = '{dir}/simple-web-crawler-{time}.log'.format(dir=currentWorkingDir, time=currentTime)
    commonGlobalUrlList = list()

    def __init__(self, *args, **kwargs):
        """The crawlers constructor method."""
        super(SimpleWebCrawler, self).__init__(*args, **kwargs)
        logFilePath = kwargs.get('log_file_path')
        if logFilePath is not None:
            self.outFile = logFilePath

    def normalizeUrl(self, inList, uri):
        """Helper method to perform a URL normalization."""
        scheme = '{uri.scheme}://'.format(uri=uri)
        netloc = '{uri.netloc}/'.format(uri=uri)
        rootUrl = '{scheme}{netloc}'.format(scheme=scheme, netloc=netloc)
        for position, _ in enumerate(inList):
            if inList[position].startswith('mailto'):
                inList.remove(position)
                continue
            if inList[position].startswith('//'):
                inList[position] = inList[position].replace('//', scheme)
                continue
            if re.search('^("|\\\| |/)', inList[position]):
                inList[position] = inList[position].strip(' /\\"')
                continue
            if not inList[position].startswith(('http://', 'https://')):
                inList[position] = rootUrl + inList[position]
        return inList

    def parse(self, response):
        """Scrapy's parse method parses the received response from the entity.

        Parse result - a list of found URLs on a web site - is stored in the file.
        """
        # declare local common list which holds temporary URLs
        localCommonUrlList = list()
        urlList = list()

        # get request's root URL
        uri = urlparse(response.url)

        print('Crawler in progress...\n')

        # find links within href=""
        try:
            # do not store links which starts with "#" or "mailto"
            urlList = response.xpath('/html//a[starts-with(@href, "") and not(starts-with(@href, "#")) and not(contains(@href, "mailto"))]/@href').extract()
            # normalize list
            urlList = self.normalizeUrl(urlList, uri)
            # merge list with local common
            localCommonUrlList = list(set(localCommonUrlList + urlList))
        except BaseException:
            pass

        # find css links
        try:
            urlList = response.xpath('/html/head/link[contains(@href, "")]/@href').extract()
            # normalize list
            urlList = self.normalizeUrl(urlList, uri)
            # merge with common list
            localCommonUrlList = list(set(localCommonUrlList + urlList))
        except BaseException:
            pass

        # find links within src=""
        try:
            urlList = response.xpath('//*[contains(@src, "")]/@src').extract()
            # normalize list
            urlList = self.normalizeUrl(urlList, uri)
            # merge with common list
            localCommonUrlList = list(set(localCommonUrlList + urlList))
        except BaseException:
            pass

        # parse inline css
        matchUrlPattern = 'url\((.*?)\)'
        extractUrlPattern = '([("\'])+(?P<url>[^)"\']+)'
        tmpInlineStyleUrls = list()
        try:
            urlList = response.xpath('//*[re:match(@style, matchUrlPattern)]/@style').extract()
            for link in urlList:
                item = re.search(extractUrlPattern, link)
                if item is not None:
                    item = item.group('url')
                    tmpInlineStyleUrls.append(item)
            # normalize list
            urlList = self.normalizeUrl(tmpInlineStyleUrls, uri)
            # merge with common list
            localCommonUrlList = list(set(localCommonUrlList + urlList))
        except BaseException:
            pass

        # TODO: parse external CSS

        if len(localCommonUrlList) > 0:
            # remove duplicates
            localCommonUrlList = list(set(localCommonUrlList))
            # merge with global list
            self.commonGlobalUrlList = list(
                set(self.commonGlobalUrlList + localCommonUrlList))
            # for evey found link perform url scraping
            for link in localCommonUrlList:
                yield scrapy.Request(link)

    def closed(self, reason):
        """When crawling is done write the list of links into the file."""
        # remove duplicates if any
        self.commonGlobalUrlList = list(set(self.commonGlobalUrlList))
        self.writeToDisk(self.commonGlobalUrlList)

    def writeToDisk(self, inList):
        """Writes the list of url content into the file."""
        with open(self.outFile, 'w') as f:
            for url in inList:
                f.write("%s\n" % url.encode("utf-8"))
