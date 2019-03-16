# -*- coding: utf-8 -*-

import os

from crawler import SimpleWebCrawler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    """ An entry point function from where the CrawlerProcess is started.

    """
    # Set the proper path to settings.py
    settings_file_path = 'simple_web_crawler.settings'
    # Set the SCRAPY_SETTINGS_MODULE variable
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(SimpleWebCrawler(), allowed_domains=['example.com'], start_urls=['http://example.com'])
    process.start()
