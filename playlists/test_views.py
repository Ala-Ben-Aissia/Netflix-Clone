from django.test import TestCase
from .models import Video, Playlist, TvShowProxy, MovieProxy, TvShowSeasonProxy, StateOptions, PlaylistItem
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings

class PlaylistViewTestCase(TestCase):
    fixtures = ['data']
    
    def test_movies_count(self):
        qs = MovieProxy.objects.all()
        self.assertEqual(qs.count(), 6)
        
    def test_shows_count(self):
        qs = TvShowProxy.objects.all()
        self.assertEqual(qs.count(), 2)
    
    def test_movie_list_view(self):
        movies = MovieProxy.objects.all().published()
        url = f'/movies/'    # if url = f"/movies" then :
        response = self.client.get(url)   # response = self.client.get(url, follow=True)
        context = response.context
        obj = context['object_list']
        self.assertIsNotNone(url) 
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(movies.order_by('-timestamp'), obj.order_by('-timestamp'))
        
    def test_show_list_view(self):
        shows = TvShowProxy.objects.all().published()
        url = f'/tvshows/'
        response = self.client.get(url)
        context = response.context
        obj = context['object_list']
        self.assertIsNotNone(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(shows.order_by('-timestamp'), obj.order_by('-timestamp'))
        
    def test_movie_detail_view(self):
        movie = MovieProxy.objects.all().published().first()
        url = f'/movies/{movie.slug}/'    # if url = f"/movies/{movie.slug}" then :
        response = self.client.get(url)   # response = self.client.get(url, follow=True)
        context = response.context
        obj = context['object']
        self.assertIsNotNone(url) 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"{movie.title}")
        self.assertEqual(movie.id, obj.id)
        
    def test_show_detail_view(self):
        show = TvShowProxy.objects.all().published().first()
        url = show.get_absolute_url()
        response = self.client.get(url)
        context = response.context
        obj = context['object']
        self.assertIsNotNone(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"{show.title}")
        self.assertEqual(show.id, obj.id)
        
    def test_search_none_view(self):
        query = None
        url = '/search/'
        response = self.client.get(url)
        context = response.context
        qs1 = Playlist.objects.none()
        qs2 = context['object_list']
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(qs1, qs2)
        self.assertContains(response, 'Perform your search')
        
    def test_search_view(self):
        query = 'action'
        url = f'/search/?q={query}'
        response = self.client.get(url)
        context = response.context
        qs1 = Playlist.objects.all().movie_or_show().search(query=query) # The Searched Playlists QuerySet
        qs2 = context['object_list'] # The Response QuerySet
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(qs1.order_by('-timestamp'), qs2.order_by('-timestamp'))
        self.assertContains(response, f'Searched for {query}')