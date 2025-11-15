from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from djongo import models as djongo_models

from django.apps import apps

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Delete all data
        User.objects.all().delete()
        Team = self.get_or_create_model('Team', ['name'])
        Activity = self.get_or_create_model('Activity', ['user', 'type', 'duration', 'date'])
        Leaderboard = self.get_or_create_model('Leaderboard', ['user', 'score'])
        Workout = self.get_or_create_model('Workout', ['name', 'description', 'difficulty'])
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Users
        ironman = User.objects.create_user(username='ironman', email='ironman@marvel.com', password='password', first_name='Tony', last_name='Stark')
        batman = User.objects.create_user(username='batman', email='batman@dc.com', password='password', first_name='Bruce', last_name='Wayne')
        superman = User.objects.create_user(username='superman', email='superman@dc.com', password='password', first_name='Clark', last_name='Kent')
        captain = User.objects.create_user(username='captain', email='captain@marvel.com', password='password', first_name='Steve', last_name='Rogers')

        # Activities
        Activity.objects.create(user=ironman, type='Run', duration=30, date='2025-11-01')
        Activity.objects.create(user=batman, type='Swim', duration=45, date='2025-11-02')
        Activity.objects.create(user=superman, type='Fly', duration=60, date='2025-11-03')
        Activity.objects.create(user=captain, type='Bike', duration=50, date='2025-11-04')

        # Leaderboard
        Leaderboard.objects.create(user=ironman, score=100)
        Leaderboard.objects.create(user=batman, score=90)
        Leaderboard.objects.create(user=superman, score=110)
        Leaderboard.objects.create(user=captain, score=95)

        # Workouts
        Workout.objects.create(name='Hero HIIT', description='High intensity for heroes', difficulty='Hard')
        Workout.objects.create(name='Sidekick Cardio', description='Cardio for sidekicks', difficulty='Medium')
        Workout.objects.create(name='Villain Yoga', description='Stretch like a villain', difficulty='Easy')

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))

    def get_or_create_model(self, name, fields):
        # Dynamically create a model if not already present
        try:
            return apps.get_model('octofit_tracker', name)
        except LookupError:
            attrs = {'__module__': 'octofit_tracker.models'}
            for field in fields:
                if field == 'user':
                    attrs[field] = djongo_models.ForeignKey(get_user_model(), on_delete=djongo_models.CASCADE)
                elif field == 'score' or field == 'duration':
                    attrs[field] = djongo_models.IntegerField()
                elif field == 'date':
                    attrs[field] = djongo_models.DateField()
                else:
                    attrs[field] = djongo_models.CharField(max_length=255)
            model = type(name, (djongo_models.Model,), attrs)
            return model
