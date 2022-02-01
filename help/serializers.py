from help.models import Article
from rest_framework import serializers


class ArticleSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "title", "slug", "summary", "content", "tags"]
