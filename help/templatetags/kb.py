import datetime
from django import template
from django.conf import settings
from help.models import Article

register = template.Library()

@register.simple_tag
def header_items():
    return [
        ("Courses", "courses", "Courses to help you get up to speed with AppointmentGuru"),
        ("Topics", "topics", "Courses to help you get up to speed with AppointmentGuru"),
        ("FAQ", "faqs", "Courses to help you get up to speed with AppointmentGuru"),
        ("Videos", "videos", "Courses to help you get up to speed with AppointmentGuru"),
    ]


@register.simple_tag
def header_items_dict():
    return [
        {
            "title": "Courses",
            "slug": "courses",
            "description": "Courses to help you get up to speed with AppointmentGuru",
            "icon": "https://tuk-cdn.s3.amazonaws.com/can-uploader/light-with-button-svg4.svg",
            "icon_dark": "https://tuk-cdn.s3.amazonaws.com/can-uploader/black-left-aligned-with-icons-svg2.svg",
            "cover_image": "https://images.unsplash.com/photo-1472289065668-ce650ac443d2?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1469&q=80",
        },
        {
            "title": "Topics",
            "slug": "topics",
            "description": "Find articles related to important topics like scheduling, invoicing, notifications, automation etc.",
            "icon": "https://tuk-cdn.s3.amazonaws.com/can-uploader/light-with-button-svg5.svg",
            "icon_dark": "https://tuk-cdn.s3.amazonaws.com/can-uploader/black-left-aligned-with-icons-svg3.svg",
            "cover_image": "https://images.unsplash.com/photo-1587654780291-39c9404d746b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80",
        },
        {
            "title": "FAQ",
            "slug": "faqs",
            "description": "Frequently asked questions",
            "icon_dark": "https://tuk-cdn.s3.amazonaws.com/can-uploader/black-left-aligned-with-icons-svg5.svg",
            "icon": "https://tuk-cdn.s3.amazonaws.com/can-uploader/light-with-button-svg6.svg",
            "cover_image": "https://images.unsplash.com/photo-1553342047-1a988767f0de?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80",
        },
        {
            "title": "Videos",
            "slug": "videos",
            "description": "Watch video tutorials",
            "icon_dark": "https://tuk-cdn.s3.amazonaws.com/can-uploader/black-left-aligned-with-icons-svg5.svg",
            "icon": "https://tuk-cdn.s3.amazonaws.com/can-uploader/light-with-button-svg7.svg",
            "cover_image": "https://images.unsplash.com/photo-1551817958-c5b51e7b4a33?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80",
        }
    ]


@register.simple_tag
def articles_by_tag(tag):
    return Article.objects.filter(tags__contains=[tag])


@register.simple_tag
def get_brand():
    return settings.BRAND
