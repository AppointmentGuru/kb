from django.contrib import admin
from help.models import Article, Category, ArticleCategory, Course, CourseArticle

@admin.action(description='Make featured')
def make_featured(modeladmin, request, queryset):
    queryset.update(featured=True)

@admin.action(description='Make faq')
def make_faq(modeladmin, request, queryset):
    queryset.update(faq=True)

@admin.action(description='Needs an update')
def mark_for_update(modeladmin, request, queryset):
    queryset.update(update_required=True)

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


class ArticleCourseInline(admin.TabularInline):
    model = CourseArticle
    extra = 0
    order = ('order',)


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
        "categories",
    )
    search_fields = ("title", "summary",)
    ordering = ("order",)

    actions = [make_faq, publish, unpublish, mark_for_update]

    inlines = [ArticleCategoryInline, ArticleCourseInline]

    def categories_list(self, obj):
        return ", ".join([c.title for c in obj.categories.all()])


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_filter = ("featured",)
    actions = [make_featured]
    # list_display = (
    #     "id",
    #     "order",
    #     "featured"
    #     "category",
    #     "article",
    # )

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )
    search_fields = ("title", "summary",)
    inlines = [ArticleCategoryInline]


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "order",
        "published",
    )
    search_fields = ("title", "summary",)
    list_filter = ("published",)
    inlines = [ArticleCourseInline]


# Register your models here.
admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
