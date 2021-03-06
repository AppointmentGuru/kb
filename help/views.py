import re
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import UpdateView
from django.conf import settings
from help.models import Article, Category, Course
from django.urls import reverse

LETTERS = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "n",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]

class Page:
    slug=None

    def __init__(self, slug):
        self.slug = slug

def index(request):
    context = {
        "MELIA_API_URL": settings.MELIA_URL,
        "MELIA_API_KEY": settings.MELIA_API_KEY,
        "page_title": "AppointmentGuru Help Center",
    }
    return render(request, "index.html", context)


def articles(request, slug="a"):
    articles = Article.objects.filter(published=True)
    page_title = "Index of all help pages"
    group_by = None

    if slug == "recently-updated":
        page_title = "Recently updated articles"
        group_by = "date_modified"
        articles = articles.order_by("-modified_date")[:15]
    elif slug:
        articles = articles.filter(title__istartswith=slug).order_by("title")
        page_title = f"Articles starting with the letter {slug.upper()}"
    else:
        articles = Article.objects.none()

    sub_pages = [Page(letter) for letter in LETTERS]
    sub_pages.append(Page("recently-updated"))

    context = {
        "page_title": page_title,
        "articles": articles,
        "letters": LETTERS,
        "slug": slug,
        "group_by": group_by,
        "sub_pages": sub_pages,
        "empty_text": f"No articles found starting with the letter {slug.upper()}",
        "builder_config": {
            "item_context_key": "sub_pages",  # the key to use to find sub-pages from this pages context
            "item_key": "slug",  # for each item found in context[item_context_key], what attr do we pass to reverse()
            "page_name": "index",  # the reverse name.
        },
    }
    return render(request, "help/article_index.html", context)


def courses(request):
    courses = Course.objects.all().order_by("order")
    context = {
        "page_title": "Courses",
        "courses": courses,
        "builder_config": {  # contextual information to help the builder build these pages
            "item_context_key": "courses",  # the key to use to find sub-pages from this pages context
            "item_key": "slug",  # for each item found in context[item_context_key], what attr do we pass to reverse()
            "page_name": "courses",  # the reverse name.
        },
    }
    return render(request, "help/courses.html", context)


def course(request, slug=None):

    course = get_object_or_404(Course, slug=slug)
    first_lesson = course.chapters.first()
    if first_lesson:
        first_lesson = first_lesson.article
    context = {
        "page_title": course.title,
        "page_description": course.summary,
        "course": course,
        "first_lesson": first_lesson,
    }
    return render(request, "help/course.html", context)


def chapter(request, slug=None, chapter=None):

    course = get_object_or_404(Course, slug=slug)
    article = get_object_or_404(Article, slug=chapter)

    context = {
        "page_title": article.title,
        "page_description": article.summary,
        "course": course,
        "article": article,
    }
    return render(request, "help/chapter.html", context)


def topics(request, slug=None):
    topics = Category.objects.all().order_by("order")
    context = {
        "page_title": "Topics",
        "topics": topics,
        "builder_config": {  # contextual information to help the builder build these pages
            "item_context_key": "topics",  # the key to use to find sub-pages from this pages context
            "item_key": "slug",  # for each item found in context[item_context_key], what attr do we pass to reverse()
            "page_name": "topic",  # the reverse name.
        },
    }
    return render(request, "help/topics.html", context)


def videos(request, slug=None):
    videos = Article.objects.filter(video_embed_url__isnull=False).order_by(
        "articlecategory__category_id"
    )

    video = None
    page_title = "Videos"
    page_description = (
        "A selection of help articles with video for those who prefer to learn visually"
    )

    if slug:
        video = get_object_or_404(Article, slug=slug)
        page_title = video.title
        page_description = video.summary

    context = {
        "page_title": page_title,
        "page_description": page_description,
        "videos": videos,
        "video": video,
        "builder_config": {
            "item_context_key": "videos",
            "item_key": "slug",
            "page_name": "videos",
        },
    }

    return render(request, "help/videos.html", context)


def faqs(request, slug=None):
    articles = Article.objects.filter(faq=True)
    context = {
        "page_title": "Frequently Asked Questions",
        "articles": articles,
    }

    return render(request, "help/article_list.html", context)


def tags(request, slug=None):

    if not slug:
        tags = set()
        articles = Article.objects.filter(published=True, tags__isnull=False)
        for a in articles:
            tags = tags.union(set(a.tags))
        context = {
            "tags": tags,
            "articles": articles,
            "builder_config": {
                "item_context_key": "tags",
                "item_key": None,
                "page_name": "tags",
            },
        }
        return render(request, "help/tags.html", context)

    articles = Article.objects.filter(tags__contains=[slug], published=True)
    context = {"page_title": f"Articles tagged with {slug}", "articles": articles}

    return render(request, "help/article_list.html", context)


def topic(request, slug=None):
    topic = get_object_or_404(Category, slug=slug)
    context = {
        "topic": topic,
        "page_title": topic.title,
        "articles": topic.articlecategory_set.all().order_by("-featured", "order"),
    }

    return render(request, "help/topic.html", context)


def article(request, slug=None):
    article = get_object_or_404(Article, slug=slug)
    context = {"article": article, "page_title": article.title}

    return render(request, "article.html", context)


def sitemap(request):

    top_level_urls = {reverse(slug) for title, slug, desc in settings.START_PAGES}
    articles = Article.objects.filter(published=True).order_by('-modified_date')
    last_modified_date = articles.first().modified_date
    base = settings.BRAND.get("base_url")
    context = {
        "top_level_urls": top_level_urls,
        "last_modified_date": last_modified_date,
        "articles": articles,
        "base": base,
    }
    return render(request, "help/sitemap.xml", context, content_type='text/xml')
