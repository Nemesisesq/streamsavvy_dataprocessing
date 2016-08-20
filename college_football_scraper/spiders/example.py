# -*- coding: utf-8 -*-
import requests
import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["streamsavvvy.tv"]
    start_urls = (
        'http://www.streamsavvy.tv/',
    )

    def parse(self, response):
        # r = requests.get('http://localhost:8081')

        requests.get('http://localhost:8080')
        yield {'hello':'world'}
