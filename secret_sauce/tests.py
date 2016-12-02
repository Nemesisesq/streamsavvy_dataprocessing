from django.test import TestCase
from secret_sauce.tf_idf import ContentEngine

# Create your tests here.

class TDIDF(TestCase):

    def setUp(self):
        self.c = ContentEngine()

    def content_engine_train_test(self):
        self.c.train()
