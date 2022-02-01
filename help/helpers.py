from help.serializers import ArticleSearchSerializer
from help.models import Article
from rest_framework.renderers import JSONRenderer
import environ
import requests

env = environ.Env()
environ.Env.read_env()


class MeliaSearch:
    url = env("MELIA_URL")
    key = env("MELIA_API_KEY")
    headers = {
        "Content-Type": "application/json",
        "X-Meili-API-Key": key,
    }

    def u(self, path):
        return f"{self.url}{path}"

    def serialize_article(self, article):
        return JSONRenderer().render(ArticleSearchSerializer([article], many=True).data)

    def add_article(self, article):

        url = self.u("/indexes/articles/documents")
        data = self.serialize_article(article)
        return requests.post(url, data=data, headers=self.headers)

    def remove_document(self, id):
        url = self.u("/indexes/articles/documents/{id}")
        return requests.delete(url, headers=self.headers)


class SearchHelper:
    """py
search = SearchHelper("melia")
search.add_article
    """

    engine = None

    def __init__(self, search="melia"):
        if search == "melia":
            self.engine = MeliaSearch()
        else:
            raise Exception(f"{self.engine} is not supported. Use one of: 'melia'")

    def get(self):
        return self.engine
