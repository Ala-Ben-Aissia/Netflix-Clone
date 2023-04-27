from django.contrib import admin
from .models import Playlist, PlaylistItem, TvShowProxy, TvShowSeasonProxy, MovieProxy, PlaylistRelated
from tags.admin import TaggedItemInline
# Register your models here.

class PlaylistRelatedInline(admin.TabularInline):
    model = PlaylistRelated
    extra = 0
    fk_name = 'playlist'

class PlaylistItemInline(admin.TabularInline):
    
    model = PlaylistItem
    extra = 0

       
class PlaylistAdmin(admin.ModelAdmin):
    inlines = [PlaylistRelatedInline, PlaylistItemInline]
    fields = ['title', 'description', 'slug', 'active', 'state']
    list_filter = ['type']
    class Meta:
        model = Playlist
        
    def get_queryset(self, request):
        return Playlist.objects.filter(type=Playlist.PlaylistType.PLAYLIST)

        
class TvShowSeasonProxyInline(admin.TabularInline):
    
    model = TvShowSeasonProxy
    extra = 0
    fields = ['order', 'title', 'state']


class TvShowProxyAdmin(admin.ModelAdmin):
    
    inlines = [TaggedItemInline, TvShowSeasonProxyInline]
    fields = ['title', 'description', 'state', 'category', 'video', 'slug']
    class Meta:
        model = TvShowProxy
    
    def get_queryset(self, request):
        return TvShowProxy.objects.all()
    
class SeasonEpisodeInline(admin.TabularInline):
    
    model = PlaylistItem
    extra = 0
    fields = ['video','order', 'state'] 
    readonly_fields = ['state', ]
           
class TvShowSeasonProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent']
    inlines = [TaggedItemInline, SeasonEpisodeInline]
    class Meta:
        model = TvShowSeasonProxy
        
    def get_queryset(self, request):
        return TvShowSeasonProxy.objects.all()      


class MovieInline(admin.TabularInline):
    
    model = PlaylistItem
    extra = 0
    fields = ['video','order', 'state'] 
    readonly_fields = ['state', ]      
class MovieProxyAdmin(admin.ModelAdmin):
    list_display = ['title']
    fields = ['title', 'description', 'state', 'category', 'video', 'slug']
    inlines = [TaggedItemInline, MovieInline]
    class Meta:
        model = MovieProxy
        
    def get_queryset(self, request):
        return MovieProxy.objects.all()

admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(TvShowProxy, TvShowProxyAdmin)
admin.site.register(TvShowSeasonProxy, TvShowSeasonProxyAdmin)
admin.site.register(MovieProxy, MovieProxyAdmin)
