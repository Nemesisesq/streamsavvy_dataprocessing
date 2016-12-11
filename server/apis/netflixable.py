import logging
import time
import urllib.error
import urllib.request

from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz, process

from server.apis.guidebox import GuideBox
from server.models import Content, Channel


class Netflixable():
    logger = logging.getLogger('cutthecord')

    g = GuideBox()

    def __init__(self, url):
        self.url = url

    def get_netflix_list(self):
        try:
            with urllib.request.urlopen(self.url) as response:
                t1 = time.time()
                soup = BeautifulSoup(response, 'lxml')
                print(time.time() - t1)

                self.logger.debug('successfully got soup')
            return soup
        except urllib.error.URLError as e:
            print(e)

    def get_netflixable_show_detail(self, url):
        try:
            with urllib.request.urlopen(url) as response:
                t1 = time.time()
                soup = BeautifulSoup(response, 'lxml')
                print(time.time() - t1)

                self.logger.debug('successfully got soup')
            return soup
        except urllib.error.URLError as e:
            print(e)

    def get_shows_from_soup(self):
        soup = self.get_netflix_list()

        listings = soup.find_all(class_='listings')

        anchor_tags = []
        for listing in listings:
            for tag in listing('a'):
                anchor_tags.append(tag)

        def f(tag):
            return tag.string != 'imdb'

        # shows = filter(f, anchor_tags)
        shows = [t for t in anchor_tags if t.string !='imdb']

        # result = map(lambda x: str(x.string), shows)
        result = [{'show': elem.string, 'link': elem.get('href')} for elem in list(shows)]

        return list(result)

    def get_show_match(self, show, show_detail):

        found_show = None

        matching_shows = [s for s in show_detail['results'] if fuzz.token_sort_ratio(show, s['title']) > 80]

        found_show = process.extractOne(show, matching_shows)

        return found_show

    def save_found_show(self, title):

        c = Content.objects.get(title=title)
        c.on_netflix = True
        c.save()

    def process_shows(self, shows):

        # shows = self.get_shows_from_soup()
        p = Channel.objects.get_or_create(name='Netflix')[0]

        for show in shows:
            print("{} is the current show".format(show))

            res = self.get_netflixable_show_detail(show['link'])

            # soup = BeautifulSoup(res, 'lxml')

            title = res.find('h3', class_='post-title').string

            try:

                try:
                    self.save_found_show(title)
                except:
                    show_detail = self.g.get_show_by_title(title)

                    print(show_detail)

                    if show_detail['total_results'] != 0:

                        try:

                             # TODO add more checks around matching the show to the title of the guide box result and find the best result

                            found_show = show_detail['results'][0]

                            # c_tuple = Content.objects.get_or_create(guidebox_data__id=found_show['id'])
                            #
                            # server = c_tuple[0]

                            content = self.g.save_content(found_show)

                            content.on_netflix = True

                            if not content.title:
                                self.logger.debug('blank show?')

                            content.save()
                            # self.logger()

                        except ValueError as e:
                            self.logger.debug(e)

            except Exception as e:
                print(e)
