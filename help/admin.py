from django.contrib import admin
from help.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "published",
        "summary",
        "tags",
    )
    list_filter = (
        "published",
        "update_required",
    )
    search_fields = ("title", "summary")


# Register your models here.
admin.site.register(Article, ArticleAdmin)
