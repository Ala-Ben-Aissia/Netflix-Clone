from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from djangoflix.db.receivers import publish_state_pre_save, slugify_post_save
from djangoflix.db.models import StateOptions
# Create your models here.


class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=StateOptions.PUBLISH,
            publish_timestamp__lte=now
        )


class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()


class Video(models.Model):
     
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    video_id = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    state = models.CharField(max_length=2, choices=StateOptions.choices, default=StateOptions.DRAFT)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    
    objects = VideoManager()
    
    def __str__(self):
        return self.title
    
    @property
    def is_published(self):
        return self.active and self.state == StateOptions.PUBLISH

    def playlists_ids(self):
        return list(self.video_playlists .all().values_list('id', flat=True)) 
        # related_name in the Playlist has replaced playlist_set
        
    def get_video_id(self):
        if self.is_published:
            return self.video_id

class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
      
class VideoPublishedProxyManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().filter(state=StateOptions.PUBLISH)
        
class VideoPublishedProxy(Video):
    
    objects = VideoPublishedProxyManager()
    
    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'
            

pre_save.connect(publish_state_pre_save, sender=Video)    
post_save.connect(slugify_post_save, sender=Video)

 
pre_save.connect(publish_state_pre_save, sender=VideoAllProxy)    
post_save.connect(slugify_post_save, sender=VideoAllProxy)


pre_save.connect(publish_state_pre_save, sender=VideoPublishedProxy)    
post_save.connect(slugify_post_save, sender=VideoPublishedProxy)



