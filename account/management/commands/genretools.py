from account.models import Genre, Instrument
from account_api.constants import TRANSLATIONS

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        for key in TRANSLATIONS:
            if key.endswith("tool"):
                if not Instrument.objects.filter(name=key).exists():
                    tool = Instrument(name=key)
                    tool.save()
                    print(key, "added")
            else:
                if not Genre.objects.filter(name=key).exists():
                    genre = Genre(name=key)
                    genre.save()
                    print(key, "added")
