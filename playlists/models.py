from django.db import models
from django.utils import timezone
from djangoflix.db.models import StateOptions
from django.db.models.signals import pre_save, post_save
from djangoflix.db.receivers import publish_state_pre_save, slugify_post_save
from videos.models import Video
from categories.models import Category
from tags.models import TaggedItem
from ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Avg, Max, Min, Q
# Create your models here.

        
class PlaylistQuerySet(models.QuerySet):
    
    def published(self):
        now = timezone.now()
        return self.filter(
            state=StateOptions.PUBLISH,
            publish_timestamp__lte=now
        )
    
    def movie_or_show(self):
        return self.filter(
            Q(type=Playlist.PlaylistType.MOVIE) |
            Q(type=Playlist.PlaylistType.SHOW)
        )
    
    def search(self, query=None):
        if query is None:
            return self.none()
        return self.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__title__icontains=query) |
            Q(tags__tag__icontains=query) 
        ).distinct() # Remove duplicates


class PlaylistManager(models.Manager):
    
    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()
    
    def featured_playlists(self):
        return self.get_queryset().filter(type=Playlist.PlaylistType.PLAYLIST)


class Playlist(models.Model):
    
    class PlaylistType(models.TextChoices):
        
        MOVIE = 'MV', 'Movie'       
        SHOW = 'SW', 'Show'
        SEASON = 'SE', 'Season'
        PLAYLIST = 'PLY', 'Playlist'
    
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True) 
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    related = models.ManyToManyField("self", blank=True, through="PlaylistRelated")
    type = models.CharField(max_length=3, choices=PlaylistType.choices, default=PlaylistType.PLAYLIST)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='category_playlists')
    tags = GenericRelation(TaggedItem, related_query_name='playlist')
    ratings = GenericRelation(Rating, related_query_name='playlist')
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, blank=True, related_name='video_playlist')
    videos = models.ManyToManyField(Video, blank=True, related_name='video_playlists', through='PlaylistItem')
    active = models.BooleanField(default=True)
    state = models.CharField(max_length=2, choices=StateOptions.choices, default=StateOptions.DRAFT)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    
    objects = PlaylistManager()
    
    @property
    def is_published(self):
        return self.active and self.state == StateOptions.PUBLISH
    
    def get_ratings_avg(self):
        return Playlist.objects.filter(id=self.id).aggregate(Avg("ratings__value"))
    
    def get_ratings_spread(self):
        return Playlist.objects.filter(id=self.id).aggregate(Max("ratings__value"), Min("ratings__value"))
    
    def get_related_items(self):
        return self.playlistrelated_set.all()
    
    def get_absolute_url(self):
        if self.is_show:
            return f"/tvshows/{self.slug}/"
        if self.is_season and self.parent is not None:
            return f"/tvshows/{self.parent.slug}/seasons/{self.slug}/"
        if self.is_movie:
            return f"/movies/{self.slug}/"
    
    @property
    def is_show(self):
        return self.type == Playlist.PlaylistType.SHOW
    
    @property
    def is_season(self):
        return self.type == Playlist.PlaylistType.SEASON
    
    @property
    def is_movie(self):
        return self.type == Playlist.PlaylistType.MOVIE
        
    def __str__(self):
        return self.title        
    
pre_save.connect(publish_state_pre_save, sender=Playlist)    
post_save.connect(slugify_post_save, sender=Playlist)

class TvShowProxyManager(PlaylistManager):
    
    def all(self):
        return self.get_queryset().filter(parent__isnull=True, type = Playlist.PlaylistType.SHOW)

class TvShowProxy(Playlist):
    
    objects = TvShowProxyManager()
    class Meta:
        proxy = True
        verbose_name = "TvShow"
        verbose_name_plural = "TvShows" 
        
    def save(self, *args, **kwargs):
            self.type = Playlist.PlaylistType.SHOW   
            super().save(*args, **kwargs)    
    
    @property
    def seasons(self):
        return self.playlist_set.published()
            
    def get_short_display(self):
        return f"{self.seasons.count()} Seasons"

pre_save.connect(publish_state_pre_save, sender=TvShowProxy)    
post_save.connect(slugify_post_save, sender=TvShowProxy)    
    
class TvShowSeasonProxyManager(PlaylistManager):
    
    def all(self):
        return self.get_queryset().filter(parent__isnull=False, type=Playlist.PlaylistType.SEASON)
    
    
class TvShowSeasonProxy(Playlist):

    objects = TvShowSeasonProxyManager()
    class Meta:
        proxy = True
        verbose_name = "Season"
        verbose_name_plural = "Seasons"
    
    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistType.SEASON   
        super().save(*args, **kwargs) 
    
    def get_short_display(self):
        if self.is_published:
            qs = self.videos.filter(state=StateOptions.PUBLISH, active=True)
            return f"{qs.count()} Episodes"
    
    def get_season_trailer(self):
        try:
            if self.video.is_published:
                return self.video
        except:
            return None
    
    def get_season_episodes(self):
        return self.playlistitem_set.published()
    
pre_save.connect(publish_state_pre_save, sender=TvShowSeasonProxy)    
post_save.connect(slugify_post_save, sender=TvShowSeasonProxy)   
    
class MovieProxyManager(PlaylistManager):
    
    def all(self):
        return self.get_queryset().filter(type = Playlist.PlaylistType.MOVIE)

class MovieProxy(Playlist):
    
    objects = MovieProxyManager()
    class Meta:
        proxy = True
        verbose_name = "Movie"
        verbose_name_plural = "Movies" 
        
    def save(self, *args, **kwargs):
            self.type = Playlist.PlaylistType.MOVIE   
            super().save(*args, **kwargs)
    
    @property
    def movies(self):
        return self.videos.published()
    
    def get_trailer_id(self):
        try:
            return self.video.get_video_id()
        except:
            return None
    
    def get_short_display(self):
        return f"{self.movies.count()} Movies"
    

pre_save.connect(publish_state_pre_save, sender=MovieProxy)    
post_save.connect(slugify_post_save, sender=MovieProxy)   

class PlaylistItemQuerySet(models.QuerySet):
    
    def published(self):
        now = timezone.now()
        return self.filter(
            playlist__state=StateOptions.PUBLISH,
            playlist__publish_timestamp__lte=now,
            video__state=StateOptions.PUBLISH,
            video__publish_timestamp__lte=now
        )


class PlaylistItemManager(models.Manager): 
    
    def get_queryset(self):
        return PlaylistItemQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()
    

class PlaylistItem(models.Model):
    
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = PlaylistItemManager()
     
    class Meta:
        ordering = ['order', '-timestamp']
        
    @property    
    def state(self):
        return self.video.state
    
def pr_limit_choices_to():
    return Q(type=Playlist.PlaylistType.SHOW) | Q(type=Playlist.PlaylistType.MOVIE)

class PlaylistRelated(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    related = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="related_item", limit_choices_to=pr_limit_choices_to)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    

        