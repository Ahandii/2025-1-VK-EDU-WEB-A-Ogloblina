import requests
from django.conf import settings
from django.core.cache import cache
from django.core.management import BaseCommand
from django.core.cache import cache
from questions.models import Tag

class Command(BaseCommand):
    def handle(self, *args, **options):
        tags = Tag.objects.popular_tags()
        cache.set("TAGS", tags, timeout = 30 * 60)
        