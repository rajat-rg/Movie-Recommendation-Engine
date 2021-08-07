from django.core.management.base import BaseCommand
import pandas as pd
from recomm.models import movies_model
class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        data = pd.read_csv('movies_final.csv')
        for MID, TITLE, TAGS in zip(data.id, data.title, data.tags):
            model = movies_model(movie_id = MID, title = TITLE, tags = TAGS)
            model.save()