from django.test import TestCase
from help.helpers import SearchHelper
from help.models import Article


class MeliaSearchHelperTestCase(TestCase):
    def setUp(self):
        self.search = SearchHelper("melia")

    def create_article(self):
        Article.objects.create(title="test", slug="test")
