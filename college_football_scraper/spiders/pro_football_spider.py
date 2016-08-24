from datetime import datetime

import scrapy
from scrapy.shell import inspect_response

from college_football_scraper.items import ProFootballScraperItem
from data_processor.match_schedules import get_team_name_for_schedule


class ProFootballSpider(scrapy.Spider):
    name = "pro_football"
    allowed_domains = ["espn.com"]
    start_urls = [
        "http://www.espn.com/nfl/teams"
    ]

    def parse(self, response):

        for sel in response.css(".span-2 > .mod-container  ul  li  span"):
            url = response.urljoin(sel.xpath('a/@href')[1].extract())
            yield scrapy.Request(url, callback=self.parse_schedule_content)

    crawled = []

    def parse_schedule_content(self, response):
        self.crawled.append(response.css('.sub-brand-title b::text').extract())

        item = ProFootballScraperItem()

        # item['date_create'] = datetime.now()
        item['team_name'] = response.css('.sub-brand-title b::text').extract()
        item['data'] = []

        owning_team = get_team_name_for_schedule(item['team_name'])

        item['team'] = owning_team

        for game in response.css('table tr[class*=row]'):

            if game.css('td::text').extract()[1] == 'BYE WEEK':

                x = 'BYE WEEK'
            else:
                x = {
                    'date': game.css('td::text').extract()[1],
                    'game_status': game.css('td ul .game-status::text ').extract()[0],
                    'opponent': {
                        'logo': game.css('td ul .team-logo-small img::attr(src)').extract()[0],
                        'name': game.css('td ul .team-name a::text').extract()[0]

                    },
                    'result_time': {
                        'time': self.get_time(game),
                        'score': self.get_score(game),
                        'status': self.get_status(game),
                        'network': self.get_network(game)

                    }
                }
            # inspect_response(response, self)

            item['data'].append(x)

        path = response.css('.mod-page-tabs.mod-pagenav-tabs ul.ui-tabs li').css('a::attr(href)')[0].extract()
        url = response.urljoin(path)

        yield scrapy.Request(url, callback=self.parse_logo, meta={'item': item})
        print(len(self.crawled))

    def get_time(self, game):
        if game.css('td')[3].xpath('text()') and len(game.css('td')[3].xpath('text()').extract()[0].split(' ')) > 1:
            return " ".join(game.css('td')[3].xpath('text()').extract()[0].split(' ')[:2])
        return False

    def get_status(self, game):
        if game.css('td')[3].css('.game-status'):
            return game.css('td')[3].css('.game-status span::text').extract()
        return False

    def get_network(self, game):

        if game.css('td')[3].xpath('text()').extract() and len(game.css('td')[3].xpath('text()').extract()[0].split(' ')) > 2:
            networks = game.css('td')[3].xpath('text()').extract()[0].split(' ')[2]

            if "WatchESPN" in networks:
                networks = "ESPN"
            return networks
        return False

    def get_score(self, game):

        if game.css('.score a::text').extract():
            return game.css('.score a::text').extract()[0]
        return False

    def parse_logo(self, response):
        item = response.meta['item']

        item['team_logo'] = response.css('nav#global-nav-secondary span.brand-logo img::attr(src)').extract()[0]

        yield item
