# -*- coding: utf-8 -*-

import argparse, os

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

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', help='Specify the domain name to crawle.', required=True)
    parser.add_argument('-l', '--log', help='Specify the log file for crawled data.', required=False)
    args = parser.parse_args()

    logFilePath = args.log
    allowedDomain = args.domain
    startUrl = 'http://{domain}'.format(domain=allowedDomain)

    # run the crawler process
    process = CrawlerProcess(settings)
    process.crawl(SimpleWebCrawler(), allowed_domains=[allowedDomain], start_urls=[startUrl], log_file_path=logFilePath)
    process.start()
