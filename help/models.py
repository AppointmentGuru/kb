from django.db import models
from django.contrib.postgres.fields import ArrayField


class Category(models.Model):

    title = models.CharField(max_length=144, null=True, blank=False)
    slug = models.SlugField(null=True, blank=False)
    cover_image = models.URLField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)


class Article(models.Model):
    def __str__(self):
        return self.title

    categories = models.ManyToManyField(Category, blank=True)

    title = models.CharField(max_length=144, null=True, blank=False)
    slug = models.SlugField(null=True, blank=False)
    cover_image = models.URLField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    video_url = models.URLField(null=True, blank=True)
    video_embed_url = models.URLField(null=True, blank=True)

    tags = ArrayField(
        models.CharField(max_length=100, blank=True), null=True, blank=True
    )

    published = models.BooleanField(default=False, db_index=True)
    update_required = models.BooleanField(default=False, db_index=True)

    upvotes = models.PositiveBigIntegerField(default=0, db_index=True)
    downvotes = models.PositiveBigIntegerField(default=0, db_index=True)

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)
