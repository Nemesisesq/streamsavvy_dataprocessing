import string
from functools import partial

import pandas as pd
import time
import redis
from celery.schedules import crontab
from celery.task import periodic_task
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import logging

from data_processor.shortcuts import print_progress
from streamsavvy_dataprocessing.settings import get_env_variable

logger = logging.getLogger('cutthecord')
class StringTemplate(object):
    orig = ''
    def __init__(self, template):
        self.template = string.Template(template)
        self.partial_substituted_str = None

    def __repr__(self):
        return self.orig.safe_substitute()

    def format(self, *args, **kws):
        self.partial_substituted_str = self.template.safe_substitute(*args, **kws)
        self.orig = string.Template(self.partial_substituted_str)
        return self.__repr__()


class ContentEngine:
    class __ContentEngine(object):
        SIMKEY = StringTemplate('ss_reco:${cat}:${id}')

        def __init__(self):

            self._r = redis.StrictRedis.from_url(get_env_variable('REDISCLOUD_URL'))
            self.r = self._r

        training = False


        def train(self):

            if not self.training:
                start = time.time()
                from data_processor.models import Content
                v = [x["guidebox_data"] for x in Content.objects.all().values() if x]
                v = [x for x in v if x]
                v = [x for x in v if 'detail' in x]


                ds = pd.DataFrame(v)
                # print(ds)
                logger.info("Training data injested in %s seconds" % (time.time() - start))

                self._r.flushdb()

                start = time.time()
                self._train(ds)
                logger.info("Engine trained in %s seconds" % (time.time() - start))

        def _train(self, ds):
            self.training = True

            """
            Train the engine.

            Create a TF-IDF matrix of unigrams, bigrams, and trigrams
            for each product. The 'stop_words' param tells the TF-IDF
            module to ignore common english words like 'the', etc.

            Then we compute similarity between all products using
            SciKit Leanr's linear_kernel (which in this case is
            equivalent to cosine similarity).

            Iterate through each item's similar items and store the
            100 most-similar. Stops at 100 because well...  how many
            similar products do you really need to show?

            Similarities and their scores are stored in redis as a
            Sorted Set, with one set for each item.

            :param ds: A pandas dataset containing two fields: description & id
            :return: Nothin!
            """

            tf = TfidfVectorizer(analyzer='word',
                                 ngram_range=(1,3),
                                 min_df=0,
                                 stop_words='english')

            """
            The dataset for the content needs to be split up in to
            """




            collection = [self.category_dicts_to_string(x) for x in ds.detail]

            """
            Unwind the collection object in to attributes on the ds object
            """

            collection_data_frame  = pd.DataFrame(collection)
            # ds.genres = pd.Series(attr_list)


            for i in ['genres', 'tags', 'cast']:
                series = collection_data_frame[i]
                self.find_and_save_recomendations(series, ds, tf, i)
                self.training = False

        def find_and_save_recomendations(self, series, ds, tf, category):
            tfid_matrix = tf.fit_transform(series)
            cosine_similarities = linear_kernel(tfid_matrix, tfid_matrix)
            for idx, row in ds.iterrows():
                print_progress(idx+1, len(ds), prefix=category)
                # print(idx, row['title'], row['id'])
                self.process_dataset_row(cosine_similarities, ds, idx, row, category)



        def process_dataset_row(self, cosine_similarities, ds, idx, row, category):
            similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
            smilar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]
            flattened = sum(smilar_items[1:], ())
            self._r.zadd(self.SIMKEY.format(cat=category,id=row['id']), *flattened)

        def category_dicts_to_string(self, x):
            y = {'genres': '', 'tags': '', 'cast': ''}
            if 'genres' in x:
                z = [c['title'] for c in x['genres']]
                y['genres'] = " ".join(z)


            if 'tags' in x:
                z = [c['tag'] for c in x['tags']]
                y['tags'] = " ".join(z)

            if 'cast' in x:
                z = [c['name'] for c in x['cast']]
                y['cast'] = " ".join(z)


            return y

        def predict(self, category, item_id, num):
            """
            Couldn't be simpler! Just retrieves the similar items and
            their 'score' from redis.

            :param item_id: string
            :param num: number of similar items to return
            :return: A list of lists like: [["19", 0.2203],
            ["494", 0.1693], ...]. The first item in each sub-list is
            the item ID and the second is the similarity score. Sorted
            by similarity score, descending.
            """

            return self._r.zrange(self.SIMKEY.format(cat=category, id=item_id),
                                  0,
                                  num - 1,
                                  withscores=True,
                                  desc=True)
    instance = None
    def __init__(self):
        if not ContentEngine.instance:
            ContentEngine.instance = ContentEngine.__ContentEngine()

    def __getattr__(self, item):
        return getattr(self.instance, item)

    # def __setattr__(self, key, value):



# content_engine = ContentEngine()

