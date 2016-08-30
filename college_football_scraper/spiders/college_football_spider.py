from datetime import datetime

import scrapy
from scrapy.shell import inspect_response
import re

from college_football_scraper.helpers import isTimeString
from college_football_scraper.items import CollegeFootballScraperItem as CFItem
from data_processor.match_schedules import get_team_name_for_schedule




class CollegeFootballSpider(scrapy.Spider):
    name = "ncaaf"
    allowed_domains = ["espn.com"]
    start_urls = [
        "http://www.espn.com/college-football/teams"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + ".html"
        with open(filename, 'wb') as f:
            f.write(response.body)

        for sel in response.css('.span-2 > .mod-container  ul > li > span'):
            url = response.urljoin(sel.xpath('a/@href')[1].extract())
            yield scrapy.Request(url, callback=self.parse_schedule_content)

    def parse_schedule_content(self, response):

        item = CFItem()

        # item['date_create'] = datetime.now()

        item['team_name'] = response.css('.sub-brand-title b::text').extract()

        item['data'] = []


        owning_team = get_team_name_for_schedule(item['team_name'], 'ncaaf')

        item['team'] = owning_team

        for game in response.css('table tr[class*=row]'):
            x = {
                'date': game.css('td::text').extract()[0],
                'game_status':  game.css('td ul .game-status::text ').extract()[0],
                'opponent': {
                    'logo': game.css('td ul .team-logo-small img::attr(src)').extract()[0],
                    'name': game.css('td ul .team-name a::text').extract()[0]

                },
                'result_time': {
                    'time': self.get_time(game),
                    'network': self.get_network(game)

                }
            }

            item['data'].append(x)

        # inspect_response(response, self)

        path = response.css('.mod-page-tabs.mod-pagenav-tabs ul.ui-tabs li').css('a::attr(href)')[0].extract()
        url = response.urljoin(path)
        yield scrapy.Request(url, callback=self.parse_logo, meta={'item': item})

    def parse_logo(self, response):
        item = response.meta['item']

        item['team_logo'] = response.css('nav#global-nav-secondary span.brand-logo img::attr(src)').extract()[0]

        yield item

    def get_time(self, game):

        if game.css('td')[2].xpath('text()').extract()[0] == 'TBD':
            return 'TBD'

        d = game.css('td')[2].xpath('text()').extract()[0].split()[:3]

        d = [i for i in d if isTimeString(i)]

        return " ".join(d)

    def get_network(self, game):

        network = []

        # if game.css('td')[2].xpath('a').css('img::attr(alt)').extract():
        #     return game.css('td')[2].xpath('a').css('img::attr(alt)').extract()[0]

        if game.css('td')[2].css('img::attr(alt)').extract():
            logos = game.css('td')[2].css('img::attr(alt)').extract()
            if len(logos) > 0: network += logos

        network_name = game.css('td')[2].xpath('text()').extract()[0].split()[3:]


        network += network_name

        return network
