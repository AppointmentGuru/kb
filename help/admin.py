from django.contrib import admin
from help.models import Article, Category, ArticleCategory

@admin.action(description='Make featured')
def make_featured(modeladmin, request, queryset):
    queryset.update(featured=True)

@admin.action(description='Make faq')
def make_faq(modeladmin, request, queryset):
    queryset.update(faq=True)

@admin.action(description='Publish')
def publish(modeladmin, request, queryset):
    queryset.update(published=True)

@admin.action(description='Unpublish')
def unpublish(modeladmin, request, queryset):
    queryset.update(published=False)


class ArticleInline(admin.TabularInline):
    model = Article
    extra = 0

class ArticleCategoryInline(admin.TabularInline):
    model = ArticleCategory
    extra = 0
    order = ('featured', 'order',)


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "summary",
        "published",
        "faq",
        "update_required",
        "upvotes",
        "downvotes",
        "categories_list",
        "tags",
    )
    list_filter = (
        "published",
        "faq",
        "update_required",
    )
    search_fields = ("title", "summary",)
    ordering = ("order",)

    actions = [make_faq, publish, unpublish]

    inlines = [ArticleCategoryInline]

    def categories_list(self, obj):
        return ", ".join([c.title for c in obj.categories.all()])


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_filter = ("featured",)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )
    search_fields = ("title", "summary",)
    inlines = [ArticleCategoryInline]

# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
