import requests
from django.conf import settings
from django.core.cache import cache
from django.core.management import BaseCommand
from django.db.models import Count
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models

def get_best_members(limit=5):
    return User.objects.annotate(
        answers_count=Count('answer',
            filter=models.Q(answer__is_active=True, answer__is_correct=True)))\
            .filter(answers_count__gt=0)\
            .order_by('-answers_count')[:limit]

class Command(BaseCommand):
    def handle(self, *args, **options):
        members = get_best_members()
        cache.set("MEMBERS", members, timeout = 30 * 60)