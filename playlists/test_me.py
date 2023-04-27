from django.test import TestCase
from .models import MovieProxy, StateOptions
from django.utils import timezone

# Create your tests here.

class PlaylistModelTestCase(TestCase):
    
    def create_movie_with_videos(self):
        
        movie = MovieProxy.objects.create(title='movie', state=StateOptions.PUBLISH)
        self.movie = movie
        trailer = MovieProxy.objects.create(title='trailer', parent=movie, state=StateOptions.PUBLISH) # Only Trailer is realeased
        movie1 = MovieProxy.objects.create(title='movie 1', parent=movie)
        movie2 = MovieProxy.objects.create(title='movie 2', parent=movie)
        movie3 = MovieProxy.objects.create(title='movie 3', parent=movie)
        self.trailer = trailer
        self.movie1 = movie1
        self.movie2 = movie2
        self.movie3 = movie3
        movie_qs = MovieProxy.objects.all().exclude(parent__isnull=True)
        self.movie_qs = movie_qs
      
    def setUp(self):
        self.create_movie_with_videos()
        
    def test_movie_parts(self):
        qs = self.movie.playlist_set.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), self.movie_qs.count())

    
    def test_part_s_movie(self):
        qs = self.trailer.parent
        qs1 = self.movie1.parent
        qs2 = self.movie2.parent
        qs3 = self.movie3.parent
        self.assertEqual(qs1, qs2, qs3)
        self.assertEqual(self.movie_qs.count(), 4)

      
    def test_valid_title(self):
        title = 'movie'
        qs = MovieProxy.objects.filter(title=title)
        self.assertTrue(qs.exists())
        
        
    def test_draft_case(self):
        qs = MovieProxy.objects.filter(state=StateOptions.DRAFT)
        self.assertTrue(qs.exists())
        
        
    def test_publish_case(self):
        now = timezone.now()
        published_qs = MovieProxy.objects.filter(state=StateOptions.PUBLISH, publish_timestamp__lte=now)
        self.assertTrue(published_qs.exists())
        
    def test_MovieProxy_manager(self):
        published_qs1 = MovieProxy.objects.all().published() # PlaylistQuerySet
        published_qs2 = MovieProxy.objects.published() # PlaylistManager
        self.assertEqual(list(published_qs1), list(published_qs2))
        self.assertEqual(published_qs1.count(), published_qs2.count())