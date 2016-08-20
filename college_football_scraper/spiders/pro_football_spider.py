from datetime import datetime

import scrapy
from scrapy.shell import inspect_response

from college_football_scraper.items import ProFootballScraperItem


class ProFootballSpider(scrapy.Spider):
    name = "pro_football"
    allowed_domains = ["espn.com"]
    start_urls = [
        "http://www.espn.com/nfl/teams"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + ".html"
        with open(filename, 'wb') as f:
            f.write(response.body)


        for sel in response.css(".span-2 > .mod-container  ul  li  span"):
            url = response.urljoin(sel.xpath('a/@href')[1].extract())
            yield scrapy.Request(url, callback=self.parse_schedule_content)



    crawled = []

    def parse_schedule_content(self, response):
        self.crawled.append(response.css('.sub-brand-title b::text').extract())

        item = ProFootballScraperItem()

        # item['date_create'] = datetime.now()
        item['name'] = response.css('.sub-brand-title b::text').extract()
        item['games'] = []

        for game in response.css('table tr[class*=row]'):



            if game.css('td::text').extract()[1] == 'BYE WEEK':

                x = 'BYE WEEK'
            else:
                x = {
                    'date': game.css('td::text').extract()[1],
                    'opponent': {
                        'logo': game.css('td ul .team-logo-small a::attr(href)').extract()[0],
                        'name': game.css('td ul .team-name a::text').extract()[0]

                    },
                    'result_time': {
                        'time': self.get_result(game),
                        'network': self.get_network(game)

                    }
                }
            inspect_response(response, self)

            item['games'].append(x)

        yield item
        print(len(self.crawled))



    def get_network(self, game):

        if game.css('td')[3].xpath('text()'):
            return game.css('td')[3].xpath('text()').extract()[0].split(' ')[2]
        return 'played'

    def get_result(self, game):
        if game.css('td')[3].css('.game-status'):
            return game.css('td')[3].css('.game-status span::text').extract()

        if game.css('td')[3].xpath('text()'):
            return game.css('td')[3].xpath('text()').extract()[0]
