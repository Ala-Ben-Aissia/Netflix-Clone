from django.test import TestCase
from .models import Video, Playlist, StateOptions
from django.utils import timezone
from django.utils.text import slugify
# Create your tests here.

class PlaylistModelTestCase(TestCase):
    
    def create_show_with_seasons(self):
        
        show = Playlist.objects.create(title='Show')
        self.show = show
        season1 = Playlist.objects.create(title='Season 1', parent=show, order=1)
        season2 = Playlist.objects.create(title='Season 2', parent=show, order=2)
        season3 = Playlist.objects.create(title='Season 3', parent=show, order=3)
        self.season1 = season1
        self.season2 = season2
        self.season3 = season3
    
    def create_videos_and_playlists(self):
        video_a = Video.objects.create(title='video titleA', video_id='abc123a')
        video_b = Video.objects.create(title='video titleB', video_id='abc123b')
        video_c = Video.objects.create(title='video titleC', video_id='abc123c')  
        video_qs = Video.objects.all()
        self.video_qs = video_qs 
        self.video_a = video_a
        self.video_b = video_b
        self.video_c = video_c
        playlist_a = Playlist.objects.create(title='playlist titleA', video=video_a)
        playlist_b = Playlist.objects.create(title='playlist titleB', state=StateOptions.PUBLISH, video=video_a)
        self.playlist_a = playlist_a
        self.playlist_b = playlist_b
        
    def setUp(self):
        self.create_show_with_seasons()
        self.create_videos_and_playlists()
        self.playlist_a.videos.set(self.video_qs)
        # playlist_a.save()
        self.playlist_b.videos.set(self.video_qs)
        # playlist_b.save()

    def test_show_has_seasons(self):
        qs = self.show.playlist_set.all()
        self.assertTrue(qs.exists())
        
    def test_playlist_video(self):
        self.assertEqual(self.playlist_a.video, self.video_a) # comparing (the playlist's video instance, the created video)
    
    def test_playlist_videos(self):
        videos_count = self.playlist_a.videos.all().count()
        self.assertEqual(videos_count, 3)
    
    def test_playlist_videos_through_model(self):
        v_qs = sorted(list(self.video_qs.values_list('id')))
        video_qs = sorted(list(self.playlist_a.videos.all().values_list('id')))
        playlist_item_qs = sorted(list(self.playlist_a.playlistitem_set.all().values_list('video')))
        self.assertEqual(v_qs, video_qs)
        self.assertEqual(v_qs, playlist_item_qs)
        
    def test_video_playlists_ids(self):
        ids = self.playlist_a.video.playlists_ids()
        actual_ids = list(self.video_a.video_playlists.all().values_list('id', flat=True))
        idss = list(Playlist.objects.filter(video=self.video_a).values_list('id', flat=True))
        self.assertEqual(ids, actual_ids, idss)
    
    def test_video_playlist(self):
        qs = self.video_a.video_playlist.all()
        self.assertEqual(qs.count(), 2)
    
    def test_videos_playlist(self):
        qs = self.video_a.video_playlists.all() # queryset of the playlists of the video
        self.assertEqual(qs.count(), 2) # comparing (the playlists of the video, playlists created)
    
    def test_slug_field(self):
        title = self.playlist_a.title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.playlist_a.slug)
      
    def test_valid_title(self):
        title = 'playlist titleA'
        qs = Playlist.objects.filter(title=title)
        self.assertTrue(qs.exists())
        
    def test_created_count(self):
        qs = Playlist.objects.all()
        self.assertEqual(qs.count(), 6)
        
    def test_draft_case(self):
        qs = Playlist.objects.filter(state=StateOptions.DRAFT)
        self.assertTrue(qs.exists())
        
    def test_publish_case(self):
        now = timezone.now()
        published_qs = Playlist.objects.filter(state=StateOptions.PUBLISH, publish_timestamp__lte=now)
        self.assertTrue(published_qs.exists())
        
    def test_Playlist_manager(self):
        published_qs1 = Playlist.objects.all().published() # PlaylistQuerySet
        published_qs2 = Playlist.objects.published() # PlaylistManager
        self.assertQuerysetEqual(published_qs1, published_qs2)
        self.assertEqual(published_qs1.count(), published_qs2.count())