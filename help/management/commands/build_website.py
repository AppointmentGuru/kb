from django.core.management.base import BaseCommand
from django.urls.exceptions import NoReverseMatch
from django.test import Client
from help.models import Article, CourseArticle
from django.urls import reverse
from help.templatetags.kb import header_items
import os
from django.test.utils import setup_test_environment
from django.conf import settings

# needed so we can read template context
setup_test_environment()


def start_pages():
    return settings.START_PAGES


def create_directory(dir):
    try:
        os.mkdir(dir)
    except FileExistsError:
        pass
    return dir


def write_file(filename, content):
    if not filename.startswith("/"):
        filename = f"/{filename}"

    with open(f"dist{filename}", 'wb') as f:
        f.write(content)

    indent = "\t" * (len(str.split("/")) -1)
    print(f"{indent}{filename}")


def build_section(slug, with_index=True):
    path = reverse(slug)
    create_directory(f"./dist/{path}")

    index = Client().get(path)
    write_file(f"/{slug}/index.html", index.content)

    if builder_context := index.context.get("builder_config"):
        context_key = builder_context.get("item_context_key", "items")
        page_name = builder_context.get("page_name", slug)
        item_key =  builder_context.get("item_key", "slug")
        items = index.context.get(context_key)

        for item in items:
            item_slug = getattr(item, item_key) if item_key is not None else item
            path = reverse(page_name, args=(item_slug,))
            page = Client().get(path)
            write_file(path, page.content)

def course_chapters():
    chapters = CourseArticle.objects.filter(published=True)
    for chapter in chapters:
        create_directory(f"./dist/courses/{chapter.course.slug}/")
        path = reverse("chapter", args=(chapter.course.slug, chapter.article.slug,))
        page = Client().get(path)
        write_file(path, page.content)

def generate_sitemap():
    path = reverse("sitemap")
    page = Client().get(path)
    write_file("sitemap.xml", page.content)


class Command(BaseCommand):

    help = "Build a static version of the website"

    def add_arguments(self, parser):
        parser.add_argument(
            '--since',
            help='Skip top level pages. Only update articles modified after the provided date',
        )

    def handle(self, *args, **options):

        generate_sitemap()

        articles = Article.objects.all()
        if since := options.get("since"):
            articles = articles.filter(modified_date__date__gte=since)
        else:
            p = Client().get('/')
            write_file("/index.html", p.content)

            print("============")
            print("Tags")
            print("============")
            build_section("tags")

            # sections:
            for title, slug, summary in start_pages():
                print("============")
                print(title)
                print("============")
                build_section(slug)

            course_chapters()

        print("============")
        print("Articles")
        print("============")

        for article in articles:
            try:
                url = reverse("article", args=(article.slug,))
                p = Client().get(url)
                write_file(url, p.content)
            except NoReverseMatch:
                print(f"Invalid slug: {article.slug}")
