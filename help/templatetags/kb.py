import datetime
from django import template

register = template.Library()

@register.simple_tag
def header_items():
    return [
        ("Courses", "courses", "Courses to help you get up to speed with AppointmentGuru"),
        ("Topics", "topics", "Courses to help you get up to speed with AppointmentGuru"),
        ("FAQ", "faqs", "Courses to help you get up to speed with AppointmentGuru"),
        ("Videos", "videos", "Courses to help you get up to speed with AppointmentGuru"),
    ]
