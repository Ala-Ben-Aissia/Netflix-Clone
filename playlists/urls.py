from django.urls import path
from .views import *


urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movies'),
    path('movies/<slug:slug>/', MovieDetailView.as_view(), name='movie'),
    path('tvshows/', ShowListView.as_view(), name='tvshows'),  
    path('tvshows/<slug:slug>/', ShowDetailView.as_view(), name='tvshow'),  
    path('tvshows/<slug:tvshowSlug>/seasons/', ShowSeasonListView.as_view(), name='seasons'),
    path('tvshows/<slug:tvshowSlug>/seasons/<slug:seasonSlug>/', ShowSeasonDetailView.as_view(), name='season'),    
    path('playlists/', PlaylistListView.as_view(), name='playlists'),  
    path('playlists/<int:pk>/', PlaylistDetailView.as_view(), name='playlist'),
    path('', FeaturedPlaylistListView.as_view(), name='featured_playlists'), 
    path('search/', SearchView.as_view(), name='search'), 
]