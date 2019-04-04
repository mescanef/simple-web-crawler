# -*- coding: utf-8 -*-
"""Holds the logic of the crawler."""

import os
import re
import time
from urlparse import urlparse

import scrapy

from scrapy_splash import SplashRequest


class SimpleWebCrawler(scrapy.Spider):
    """A definition of a Scrapy spider.

    It holds the crawler's logic on how exactly parse the crawled web page.

    """

    name = 'generic'

    currentWorkingDir = os.getcwd()
    currentTime = time.mktime(time.gmtime())
    outFile = '{dir}/simple-web-crawler-{time}.log'.format(
        dir=currentWorkingDir, time=currentTime)

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
        for position, url in enumerate(inList):
            # remove all strings starting with 'mailto'
            if url.startswith('mailto'):
                inList.remove(position)
                continue

            fixedUrl = url
            if fixedUrl.startswith('//'):
                fixedUrl = fixedUrl.replace('//', scheme)
            if re.search('^("|\\\| |/)', fixedUrl):
                fixedUrl = fixedUrl.strip(' /\\"')
            if not fixedUrl.startswith(('http://', 'https://')):
                fixedUrl = rootUrl + fixedUrl
            # check if the string in fixedUrl is different than in url
            # variable. if different, then assign it to the list's element.
            if fixedUrl != url:
                inList[position] = fixedUrl
        return inList

    def start_requests(self):
        """From here the scraping of URLs begins."""
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 10})

    def parse(self, response):
        """This method parses the received response from an entity.

        Parse result - a list of found URLs on a web site - is stored
        in the file.
        """
        # declare local common list which holds temporary URLs
        localCommonUrlList = list()
        urlList = list()

        # get request's root URL
        uri = urlparse(response.url)

        # find links within href=""
        try:
            # do not store links which starts with "#" or "mailto"
            urlList = response.xpath('/html//a[starts-with(@href, "") \
                                     and not(starts-with(@href, "#")) \
                                     and not(contains(@href, "mailto"))]/@href'
                                     ).extract()
            # normalize list
            urlList = self.normalizeUrl(urlList, uri)
            # merge list with local common
            localCommonUrlList = list(set(localCommonUrlList + urlList))
        except BaseException:
            pass

        # find css links
        try:
            urlList = response.xpath('/html/head/link[contains(@href, "")]\
                                     /@href').extract()
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

        # parse inline css for URLs
        extractUrlPattern = '([("\'])+(?P<url>[^)"\']+)'
        tmpInlineStyleUrls = list()
        try:
            urlList = response.xpath('//*[re:match(@style, "url\((.*?)\)")]\
                                     /@style').extract()
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
            # write local list of URLs into a file (in append mode)
            self.writeToDisk(localCommonUrlList, 'a+')
            # for evey found link perform url scraping
            for link in localCommonUrlList:
                yield SplashRequest(link, args={'wait': 10})

    def closed(self):
        """When crawling is done write the list of links into the file."""
        # read outFile's content and find possible duplicates.
        fileExists = os.path.isfile(self.outFile)
        if fileExists:
            fileContent = list()
            with open(self.outFile, 'r') as f:
                fileContent = list(set(f.read().splitlines()))
            if len(fileContent) > 0:
                self.writeToDisk(fileContent, 'w')

    def writeToDisk(self, inList, writeMode):
        """Writes the list of url content into the file."""
        with open(self.outFile, writeMode) as f:
            for url in inList:
                f.write("%s\n" % url.encode("utf-8"))
