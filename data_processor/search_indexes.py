import datetime
from haystack import indexes
from data_processor.models import Content


# class ContentIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     content_auto = indexes.EdgeNgramField(model_attr='title')
#
#     def get_model(self):
#         return Content
#
#     def index_queryset(self, using=None):
#         return self.get_model().objects.all()

class ContentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Content

    def index_queryset(self, using=None):
        return self.get_model().objects.all().exclude(title=None)
