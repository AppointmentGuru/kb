from django.core.management.base import BaseCommand
from help.serializers import ArticleSearchSerializer
from help.models import Article
from rest_framework.renderers import JSONRenderer
import requests
import environ

env = environ.Env()
environ.Env.read_env()

url = env("MELIA_URL")
key = env("MELIA_API_KEY")


def u(path):
    return f"{url}{path}"


headers = {
    "Content-Type": "application/json",
    "X-Meili-API-Key": key,
}


class Command(BaseCommand):

    help = "Build Meliasearch index"

    def handle(self, *args, **options):
        requests.delete(u("/indexes/articles"), headers=headers)

        articles = Article.objects.all()
        data = JSONRenderer().render(ArticleSearchSerializer(articles, many=True).data)
        res = requests.post(
            u("/indexes/articles/documents"), data=data, headers=headers
        )
        print(res.status_code)
