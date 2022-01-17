from django.core.management.base import BaseCommand
from help.models import Article
import requests

airtable_key = env("AIRTABLE_KEY")


class Command(BaseCommand):

    help = "Import from Airtable"

    def handle(self, *args, **options):
        url = "https://api.airtable.com/v0/appB8tJlSNDM6eeWt/HelpPage?maxRecords=150&view=Grid%20view%20en"
        headers = {"Authorization": f"Bearer {airtable_key}"}
        res = requests.get(url, headers=headers)

        field_map = {
            "Title": "title",
            "Slug": "slug",
            "Description": "content",
            "Tagline": "summary",
            "Video": "video_embed_url",
            "Tags": "tags,",
        }
        Article.objects.all().delete()

        skipped = []
        for record in res.json().get("records"):
            try:
                article = Article()
                for field, value in record.get("fields").items():
                    if field in field_map and value:
                        key = field_map.get(field)
                        setattr(article, key, value)
                article.save()
                print(f"Created {article.title}")
            except Exception as e:
                skipped.append(record)
                title = record.get("fields").get("Title")
                print(f"Skipping {title}")
                print(e)

        print("-----------")
        print(skipped)

