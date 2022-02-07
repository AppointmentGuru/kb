from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from help.mixins.modelmixins import CategoryModelProperties

class Category(CategoryModelProperties, models.Model):
    def __str__(self):
        return self.title

    title = models.CharField(max_length=144, null=True, blank=False)
    slug = models.SlugField(null=True, blank=False, unique=True)
    cover_image = models.URLField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    order = models.PositiveIntegerField(default=1000)


class ArticleCategory(models.Model):
    def __str__(self):
        str = f"{self.category.title}: {self.article.title}"
        if self.featured:
            str = "✓ " + str
        return str

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['category', 'article'], name='unique_category_article')
        ]

    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    article = models.ForeignKey("Article", on_delete=models.CASCADE)

    order = models.PositiveIntegerField(default=1000)
    featured = models.BooleanField(default=False)


class Article(models.Model):
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article", args=(self.slug,))

    categories = models.ManyToManyField(Category, blank=True, through=ArticleCategory)  # through=ArticleCategory

    title = models.CharField(max_length=144, null=True, blank=False)
    slug = models.SlugField(null=True, blank=False, max_length=144, unique=True)
    cover_image = models.URLField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True, help_text="Meta Keywords for SEO")
    summary = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    discussion = models.TextField(null=True, blank=True, help_text="Admin only field for discussion on the article")

    video_thumbnail = models.URLField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    video_embed_url = models.URLField(null=True, blank=True)

    mobile_video_thumbnail = models.URLField(null=True, blank=True)
    mobile_video_url = models.URLField(null=True, blank=True)
    mobile_video_embed_url = models.URLField(null=True, blank=True)

    tags = ArrayField(
        models.CharField(max_length=100, blank=True), null=True, blank=True
    )
    search_phrases = ArrayField(
        models.CharField(max_length=250, blank=True), null=True, blank=True, help_text="Specific phrases someone might type to find this article"
    )

    order = models.PositiveIntegerField(default=1000, db_index=True)
    faq = models.BooleanField(default=False, db_index=True)
    published = models.BooleanField(default=False, db_index=True)
    update_required = models.BooleanField(default=False, db_index=True)

    upvotes = models.PositiveBigIntegerField(default=0, db_index=True)
    downvotes = models.PositiveBigIntegerField(default=0, db_index=True)

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)


class CourseArticle(models.Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'article'], name='unique_course_article')
        ]
        ordering = ['order',]

    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    article = models.ForeignKey("Article", on_delete=models.CASCADE)

    order = models.PositiveIntegerField(default=1000)
    published = models.BooleanField(default=True)


class Course(models.Model):

    def __str__(self):
        return self.title

    title = models.CharField(max_length=144, null=True, blank=False)
    slug = models.SlugField(null=True, blank=False, max_length=144, unique=True)
    icon = models.URLField(null=True, blank=True)
    cover_image = models.URLField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True, help_text="Meta Keywords for SEO")
    content = models.TextField(null=True, blank=True)

    # chapters
    articles = models.ManyToManyField(Article, blank=True, through=CourseArticle)

    published = models.BooleanField(default=False, db_index=True)
    order = models.PositiveIntegerField(default=1000, db_index=True)
    upvotes = models.PositiveBigIntegerField(default=0, db_index=True)
    downvotes = models.PositiveBigIntegerField(default=0, db_index=True)

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)

    @property
    def chapters(self):
        return self.coursearticle_set.filter(published=True).order_by('order')
