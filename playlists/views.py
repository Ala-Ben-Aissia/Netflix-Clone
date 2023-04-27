from django.shortcuts import render
from django.views import generic
from .models import *
from django.http import Http404
# Create your views here.

from .mixins import PlaylistMixin


class SearchView(PlaylistMixin, generic.ListView):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query is not None:
            context['title'] = f'Searched for {query}'
        else:
            context['title'] = 'Perform your search'
        return context
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Playlist.objects.all().movie_or_show().search(query=query)
   

    
class MovieListView(PlaylistMixin, generic.ListView):
    queryset = MovieProxy.objects.all()
    title = 'Movies'

class MovieDetailView(PlaylistMixin, generic.DetailView):
    template_name = 'playlists/movie_detail.html'
    queryset = MovieProxy.objects.all()
    title = 'Movie'
    
class ShowListView(PlaylistMixin, generic.ListView):
    queryset = TvShowProxy.objects.all()
    title = 'Tv Shows'

class ShowDetailView(PlaylistMixin, generic.DetailView):
    template_name = 'playlists/tvshow_detail.html'
    queryset = TvShowProxy.objects.all()
    title = 'Tv Show'    
    
    # def get_object(self):
    #     request = self.request
    #     kwargs = self.kwargs
    #     print("request: ", request)
    #     print("kwargs: ", kwargs)
    #     return self.get_queryset().filter(**kwargs).first()

class PlaylistListView(PlaylistMixin, generic.ListView):
    queryset = Playlist.objects.all()
    title = 'Playlists'
    
    
class PlaylistDetailView(PlaylistMixin, generic.DetailView):
    template_name = 'playlists/playlist_detail.html'
    queryset = Playlist.objects.all()
    title = 'Playlist'

    
class FeaturedPlaylistListView(PlaylistMixin, generic.ListView):
    template_name = 'playlists/featured_list.html'
    queryset = Playlist.objects.featured_playlists()
    title = 'Featured Playlists'

class ShowSeasonListView(PlaylistMixin, generic.ListView):
    queryset =  TvShowSeasonProxy.objects.all()
    title = 'Seasons'
    
    def get_queryset(self):
        kwargs = self.kwargs
        show_slug = kwargs.get('tvshowSlug')
        print("kwargs:    ", kwargs)
        return TvShowSeasonProxy.objects.filter(parent__slug__iexact=show_slug)
    
class ShowSeasonDetailView(PlaylistMixin, generic.DetailView):
    queryset = TvShowSeasonProxy.objects.all()
    template_name = 'playlists/season_detail.html'
    title = 'Season'
    
    def get_object(self):
        tvshow_slug = self.kwargs.get('tvshowSlug')
        season_slug = self.kwargs.get('seasonSlug')
        try:
            obj = self.get_queryset().get(parent__slug__iexact=tvshow_slug, slug__iexact=season_slug)
        except:
            obj = None
        return obj
        