from django.shortcuts import render
from .models import *
from playlists.models import *
from django.views.generic import ListView, View, DetailView
from playlists.mixins import PlaylistMixin
# Create your views here.

# class TaggedItemListView(ListView):
#     template_name = 'tags/tag_list.html'
#     queryset = TaggedItem.objects.unique_tags()
#     context_object_name = 'tags'

class TaggedItemListView(View):
    def get(self, request, *args, **kwargs):
        tags = TaggedItem.objects.unique_tags()
        context = {'tags': tags}
        return render(request, 'tags/tag_list.html', context)
    
class TaggedItemDetailView(PlaylistMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"{self.kwargs.get('tag')}".title()
        return context
    def get_queryset(self):
        tag = self.kwargs.get('tag')
        return set(Playlist.objects.filter(tags__tag=tag).movie_or_show()) 
