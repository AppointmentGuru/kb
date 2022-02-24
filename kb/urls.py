"""kb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from help import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("topics/", views.topics, name="topics"),
    path("topics/<slug:slug>.html", views.topic, name="topic"),

    path("index/", views.articles, name="index"),
    path("index/<slug:slug>.html", views.articles, name="index"),

    # path("courses/<slug:slug>/<chapter:slug>.html", views.course, name="chapter"),
    path("courses/<slug:slug>/<slug:chapter>.html", views.chapter, name="chapter"),
    path("courses/<slug:slug>.html", views.course, name="courses"),
    path("courses/", views.courses, name="courses"),

    path("faqs/", views.faqs, name="faqs"),
    path("tags/", views.tags, name="tags"),
    path("tags/<slug:slug>.html", views.tags, name="tags"),

    path("videos/", views.videos, name="videos"),
    path("videos/<slug:slug>.html", views.videos, name="videos"),

    path("<slug:slug>.html", views.article, name="article"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("", views.index, name="home"),
]
