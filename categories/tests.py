from django.test import TestCase
from .models import Category
from playlists.models import Playlist
# Create your tests here.

class CategorytestCase(TestCase):
    
    def setUp(self):
        cat_a = Category.objects.create(title='Action')
        cat_b = Category.objects.create(title='Comedy', active=False)
        self.cat_a = cat_a
        self.cat_b = cat_b
        playlist_a = Playlist.objects.create(title='playlist_a', category=cat_a)
        self.playlist_a = playlist_a
    
    def test_is_active(self):
        self.assertTrue(self.cat_a.active)
        
    def test_is_not_active(self):
        self.assertFalse(self.cat_b.active)
        
    def test_related_playlist(self):
        qs = self.cat_a.category_playlists.all()
        self.assertEqual(qs.count(), 1)