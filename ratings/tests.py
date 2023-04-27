from django.test import TestCase
from django.contrib.auth import get_user_model
from playlists.models import Playlist
from .models import Rating, RatingChoices
import random
from django.db.models import Avg
# Create your tests here.

User = get_user_model() # User.objects.all()

class RatingtestCase(TestCase):
    
    def create_users(self):
        self.users_count = random.randint(10, 700)
        items = []
        for i in range(self.users_count):
            items.append(User(username=f"user_{i}"))
        User.objects.bulk_create(items)
        self.users = User.objects.all()
        
    def create_playlists(self):
        self.playlists_count = random.randint(10, 100)
        items = []
        for i in range(self.playlists_count):
            items.append(Playlist(title=f"playlist_{i}"))
        Playlist.objects.bulk_create(items)
        self.playlists = Playlist.objects.all()
        
    def create_ratings(self):
        self.ratings_count = 300
        self.ratings_values = []
        items = []
        for i in range(self.ratings_count):
            user_obj = self.users.order_by('?').first()
            value_obj = random.choice(RatingChoices.choices)[0]
            content_obj = self.playlists.order_by('?').first() # random order by django
            if value_obj is not None:   
                self.ratings_values.append(value_obj)
            items.append(Rating(
                user = user_obj,
                value = value_obj,
                content_object = content_obj
                )
            )
        Rating.objects.bulk_create(items)
        self.ratings = Rating.objects.all()
        
    def setUp(self):
        self.create_users()
        self.create_playlists()
        self.create_ratings()
        
    def test_users_count(self):
        qs = User.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), self.users_count)
        self.assertEqual(self.users.count(), self.users_count)
        
    def test_playlists_count(self):
        qs = Playlist.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), self.playlists_count)
        self.assertEqual(self.playlists.count(), self.playlists_count)
        
    def test_ratings_count(self):
        qs = Rating.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), self.ratings_count)
        self.assertEqual(self.ratings.count(), self.ratings_count)
        
    def test_ratings_random_choices(self):
        value_set = set(Rating.objects.values_list('value', flat=True))
        self.assertTrue(len(value_set) in range(2, 7)) # More than one choice and less than 7
        
    def test_ratings_agg(self):
        avg1 = Rating.objects.aggregate(average_rating=Avg('value'))['average_rating']
        s = sum(Rating.objects.filter(value__isnull=False).values_list('value', flat=True))
        n = len(Rating.objects.filter(value__isnull=False)) * 1.0 # Make sure to get proper decima numbers
        avg2 = s/n
        total = sum(self.ratings_values)
        occ = len(self.ratings_values)
        avg3 = total/occ
        self.assertIsNotNone(avg1)
        self.assertTrue(avg1 > 1)
        self.assertEqual(avg1, avg2, avg3) 
        
    def test_playlist_ratings_agg(self):
        avg1  = Playlist.objects.aggregate(average_rating=Avg('ratings__value'))['average_rating']           
        avg2 = Rating.objects.aggregate(average_rating=Avg('value'))['average_rating']
        self.assertIsNotNone(avg1)
        self.assertTrue(avg1 > 1)
        self.assertEquals(avg1, avg2)
        