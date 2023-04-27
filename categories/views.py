from django.shortcuts import render
from django.views.generic import ListView
from playlists.mixins import PlaylistMixin
from .models import Category
from django.http import Http404
from playlists.models import *
from django.db.models import Count
# Create your views here.

class CategoryListView(PlaylistMixin, ListView):
    queryset = Category.objects.all().filter(active=True).annotate(playlist_count=Count('category_playlists')).filter(
            playlist_count__gt=0
        ) # see related_name of category attribute in the Playlist model
    title = 'Categories'


class CategoryDetailView(PlaylistMixin, ListView):
    queryset = Category.objects.filter(active=True)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            obj = Category.objects.get(slug=self.kwargs.get('slug'))
        except Category.DoesNotExist:
            raise Http404
        except Category.MultipleObjectsReturned:
            raise Http404
        
        except:
            print('object is None')
            obj = None
        context['category'] = obj
        if obj is not None:
            context['title'] = obj.title
        return context
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Playlist.objects.filter(category__slug=slug).published()
        