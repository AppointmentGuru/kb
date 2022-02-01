from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import UpdateView
from django.conf import settings
from help.models import Article, Category

def index(request):
    context = {
        "MELIA_API_URL": settings.MELIA_URL,
        "MELIA_API_KEY": settings.MELIA_API_KEY,
        "page_title": "AppointmentGuru Help Center",
    }
    return render(request, "index.html", context)

def courses(request, slug=None):
    context = {}
    return render(request, "help/courses.html", context)

def topics(request, slug=None):
    topics = Category.objects.all().order_by('order')
    context = {
        "page_title": "Topics",
        "item_key": "topics", # <- tell the builder where to find sub-pages
        "topics": topics,
        "builder_config": {
            "item_context_key": "topics",
            "item_key": "slug",
            "page_name": "topic",
        }
    }
    return render(request, "help/topics.html", context)

def videos(request, slug=None):
    videos = Article.objects.filter(video_embed_url__isnull=False).order_by("articlecategory__category_id")

    video = get_object_or_404(Article, slug=slug) if slug else None
    context = {
        "page_title": "Videos",
        "videos": videos,
        "video": video,
        "builder_config": {
            "item_context_key": "videos",
            "item_key": "slug",
            "page_name": "videos",
        }
    }

    return render(request, "help/videos.html", context)


def faqs(request, slug=None):
    articles = Article.objects.filter(faq=True)
    context = {
        "page_title": "Frequently Asked Questions",
        "articles": articles,
    }

    return render(request, "help/article_list.html", context)

def topic(request, slug=None):
    topic = get_object_or_404(Category, slug=slug)
    context = {
        "topic": topic,
        "page_title": topic.title,
        "articles": topic.articlecategory_set.all(),
    }

    return render(request, "help/topic.html", context)


def article(request, slug=None):
    article = get_object_or_404(Article, slug=slug)
    context = {"article": article, "page_title": article.title}

    return render(request, "article.html", context)


class AuthorUpdateView(UpdateView):
    model = Article
    fields = ["title", "summary", "content"]
