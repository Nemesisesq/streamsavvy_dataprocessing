import datetime
from haystack import indexes
from data_processor.models import Content, Sport


# class ContentIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     content_auto = indexes.EdgeNgramField(model_attr='title')
#
#     def get_model(self):
#         return Content
#
#     def index_queryset(self, using=None):
#         return self.get_model().objects.all()

class ContentIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(use_template=True)
    cur_pop_score = indexes.CharField(model_attr='curr_pop_score')

    def get_model(self):
        return Content

    def index_queryset(self, using=None):
        return self.get_model().objects.all().exclude(title=None)

    # def prepare_genre(self, obj):
    #     if 'detail' in obj.guidebox_data:
    #         return [i['title'] for i in obj.guidebox_data['detail']['genres']]
    #     return []
    #
    # def prepare_cast(self, obj):
    #     if 'detail' in obj.guidebox_data:
    #         return [i['name'] for i in obj.guidebox_data['detail']['cast']]
    #     return []
    #
    # def prepare_tags(self, obj):
    #     if 'detail' in obj.guidebox_data:
    #         return [i['tag'] for i in obj.guidebox_data['detail']['tags']]
    #     return []

class SportIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    team_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Sport

    def index_queryset(self, using=None):
        return self.get_model().objects.all().exclude(title=None)
