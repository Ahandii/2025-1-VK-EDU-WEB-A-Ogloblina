from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("--ratio", dest="ratio", type=str, required=True)

    def handle(self, *args, **options):
        users_to_create = []
        print(options["ratio"])
        for i in range(5):
            username = f"z_{i}@m.ru"
            user = User(email = username, username = username)
            users_to_create.append(user)
        
        created_users = User.objects.bulk_create(users_to_create, batch_size=5)
        print(f"Было создано {len(created_users)} пользователей")