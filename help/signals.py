from django.db.models.signals import pre_save, post_save, post_delete
from django.utils.text import slugify
from django.dispatch import receiver
from help.models import Article
from help.helpers import SearchHelper


@receiver(pre_save, sender=Article)
def generate_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)[:49]


@receiver(post_save, sender=Article)
def add_to_index(sender, instance, **kwargs):
    search = SearchHelper("melia").get()
    if instance.published:
        search.add_article(instance)


@receiver(post_delete, sender=Article)
def remove_from_index(sender, instance, **kwargs):
    search = SearchHelper("melia").get()
    search.remove_document(instance.id)
