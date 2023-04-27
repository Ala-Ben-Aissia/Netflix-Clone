from django.contrib import admin
from .models import VideoAllProxy, VideoPublishedProxy
# Register your models here.


class VideoAllProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'state', 'video_id', 'is_published', 'playlists_ids']
    search_fields = ['title',]
    list_filter = ['state', 'active',]
    readonly_fields = ['id', 'is_published', 'publish_timestamp', 'playlists_ids']
    class Meta:
        model = VideoAllProxy

admin.site.register(VideoAllProxy, VideoAllProxyAdmin)        

class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'state', 'video_id']
    search_fields = ['title']
    readonly_fields = ['id', 'is_published', 'publish_timestamp']
    
    class Meta:
        model = VideoPublishedProxy
          
    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(active=True)

admin.site.register(VideoPublishedProxy, VideoPublishedProxyAdmin)


