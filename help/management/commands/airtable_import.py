from unicodedata import category
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from help.models import Article, ArticleCategory
import requests
from pathlib import Path
import environ

env = environ.Env()
environ.Env.read_env()

airtable_key = env("AIRTABLE_KEY")

catmap = {
    "rec4rPCVqq1wZv7LX": 6, # Adding and managing clients
    "rec5cUsT4uTtXnmbh": 13, # Notifications
    "recLTPRCTQvI5Dd2A": 12, # Your account settings
    "recN4KlDnXpEghwOU": 11, # Teams
    "recOyEtZaWqbfMp23": 14, # Getting started
    "recPQYIbXKnWjTXuc": 9, # Your AppointmentGuru subscription
    "recTmoBkAmGSedRzY": 5, # Adding and managing appointments
    "recVm1QXZRXjgs4UA": 10, # Integrations
    "recWFc2tuZQq3u3u1": 8, #Calendar and schedule
    # "recpl1Ao3g6MriEoF": Let us do it for you
    "recrhVnOtv9tPk4tI": 7, # Your website
    "recrjB2ayw90T3KQn": 1, #Invoicing your clients
}

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
            "Tags": "tags",
            "Published": "published",
        }
        # Article.objects.filter(id__lt=171).delete()

        skipped = []
        for record in res.json().get("records"):
            verb = "Updated"
            try:
                slug = slugify(record.get("fields").get("Slug"))[:49]
                print(slug)
                try:
                    article = Article.objects.get(slug=slug)
                    print("Existing article")
                except Article.DoesNotExist:
                    print("new article")
                    article = Article()
                    article.slug = slug
                    verb = "Created"

                # set values:
                print("Set fields")
                for field, value in record.get("fields").items():
                    if field in field_map and value:
                        key = field_map.get(field)
                        setattr(article, key, value)

                # categorize:
                print("Set faq")
                cats = record.get("fields", {}).get("Category")
                if "rec5p1ZAC9xBnyCac" in cats:
                    article.faq = True

                article.save()
                print(f"{verb} {article.title}")

                print("Set cats")
                if cats:
                    for cat in cats:
                        if cat_id := catmap.get(cat):
                            print(cat_id)
                            ac, created = ArticleCategory.objects.get_or_create(article=article, category_id=cat_id)
                            print(f"{created}  - {ac.category}")

            except Exception as e:
                skipped.append(record)
                title = record.get("fields").get("Title")
                print(f"Skipping {title}")
                print(e)
                import ipdb

                ipdb.set_trace()

        print("-----------")
        print(skipped)

