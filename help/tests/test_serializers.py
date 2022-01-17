from django.test import TestCase
from help.serializers import ArticleSearchSerializer
from help.models import Article


class ArticleSearchSerializerTestCase(TestCase):
    def setUp(self):
        article = Article()
        article.title = "hello"
        article.text = "lorum ipsum etc"
        article.save()

        self.article = article

    def test_serialize(self):
        data = ArticleSearchSerializer(self.article).data

