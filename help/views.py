from django.shortcuts import render
from django.conf import settings


def index(request):
    context = {
        "MELIA_API_URL": settings.MELIA_URL,
        "MELIA_API_KEY": settings.MELIA_API_KEY,
    }
    return render(request, "index.html", context)
