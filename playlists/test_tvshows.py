from django.test import TestCase
from .models import Video, TvShowProxy, TvShowSeasonProxy, StateOptions
from django.utils import timezone
from django.utils.text import slugify
# Create your tests here.

class Tv_ShowModelTestCase(TestCase):
    
    def create_show_with_seasons(self):
        
        show = TvShowProxy.objects.create(title='Show', state=StateOptions.PUBLISH)
        self.show = show
        season1 = TvShowSeasonProxy.objects.create(title='Season 1', parent=show, order=1, state=StateOptions.PUBLISH)
        season2 = TvShowSeasonProxy.objects.create(title='Season 2', parent=show, order=2, state=StateOptions.PUBLISH)
        season3 = TvShowSeasonProxy.objects.create(title='Season 1', parent=show, order=3)
        self.season1 = season1
        self.season2 = season2
        self.season3 = season3
    
    def create_videos_and_tv_shows(self):
        video_a = Video.objects.create(title='video titleA', video_id='abc123a')
        video_b = Video.objects.create(title='video titleB', video_id='abc123b')
        video_c = Video.objects.create(title='video titleC', video_id='abc123c')  
        video_qs = Video.objects.all()
        self.video_qs = video_qs 
        self.video_a = video_a
        self.video_b = video_b
        self.video_c = video_c
        tv_show_a = TvShowProxy.objects.create(title='tv_show titleA', video=video_a)
        tv_show_b = TvShowProxy.objects.create(title='tv_show titleB', state=StateOptions.PUBLISH, video=video_a)
        self.tv_show_a = tv_show_a
        self.tv_show_b = tv_show_b
        
    def setUp(self):
        self.create_show_with_seasons()
        self.create_videos_and_tv_shows()
        self.tv_show_a.videos.set(self.video_qs)
        # tv_show_a.save()
        self.tv_show_b.videos.set(self.video_qs)
        # tv_show_b.save()

    def tvshow_unique_slug(self):
        return self.assertNotEqual(self.season1.slug, self.season3.slug)
    
    def test_show_has_seasons(self):
        qs = self.show.playlist_set.all()
        self.assertTrue(qs.exists())
        
    def test_tv_show_video(self):
        self.assertEqual(self.tv_show_a.video, self.video_a) # comparing (the tv_show's video instance, the created video)
    
    def test_tv_show_videos(self):
        videos_count = self.tv_show_a.videos.all().count()
        self.assertEqual(videos_count, 3)
    
    def test_tv_show_videos_through_model(self):
        v_qs = sorted(list(self.video_qs.values_list('id')))
        video_qs = sorted(list(self.tv_show_a.videos.all().values_list('id')))
        tv_show_item_qs = sorted(list(self.tv_show_a.playlistitem_set.all().values_list('video')))
        self.assertEqual(v_qs, video_qs)
        self.assertEqual(v_qs, tv_show_item_qs)
        
    def test_video_tv_shows_ids(self):
        ids = self.tv_show_a.video.playlists_ids()
        actual_ids = list(self.video_a.video_playlists.all().values_list('id', flat=True))
        idss = list(TvShowProxy.objects.filter(video=self.video_a).values_list('id', flat=True))
        self.assertEqual(ids, actual_ids, idss)
    
    def test_video_tv_show(self):
        qs = self.video_a.video_playlist.all()
        self.assertEqual(qs.count(), 2)
    
    def test_videos_tv_show(self):
        qs = self.video_a.video_playlist.all() # queryset of the tv_shows of the video
        self.assertEqual(qs.count(), 2) # comparing (the tv_shows of the video, tv_shows created)
    
    def test_slug_field(self):
        title = self.tv_show_a.title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.tv_show_a.slug)
      
    def test_valid_title(self):
        title = 'tv_show titleA'
        qs = TvShowProxy.objects.filter(title=title)
        self.assertTrue(qs.exists())
        
    def test_tv_show_count(self):
        qs = TvShowProxy.objects.all()
        self.assertEqual(qs.count(), 3)
    
    def test_tv_show_count(self):
        qs = TvShowProxy.objects.all()
        self.assertEqual(qs.count(), 3)
        
    def test_tv_show_draft_case(self):
        qs = TvShowProxy.objects.all().filter(state=StateOptions.DRAFT)
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), 1)
    
    def test_season_draft_case(self):
        qs = TvShowSeasonProxy.objects.all().filter(state=StateOptions.DRAFT)
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), 1)
        
    def test_tv_show_publish_case(self):
        now = timezone.now()
        published_qs = TvShowProxy.objects.all().filter(state=StateOptions.PUBLISH, publish_timestamp__lte=now)
        self.assertTrue(published_qs.exists())
        self.assertEqual(published_qs.count(), 2)
        
    def test_season_publish_case(self):
        now = timezone.now()
        published_qs = TvShowSeasonProxy.objects.all().filter(state=StateOptions.PUBLISH, publish_timestamp__lte=now)
        self.assertTrue(published_qs.exists())
        self.assertEqual(published_qs.count(), 2)
        
    def test_tv_show_manager(self):
        qs1 = TvShowProxy.objects.all().published()
        qs2 = TvShowSeasonProxy.objects.all().published()
        qs3 = TvShowProxy.objects.published()
        qs4 = TvShowSeasonProxy.objects.published()
        self.assertEqual(qs3.count(), qs1.count() + qs2.count())
        self.assertEqual(qs4.count(), qs1.count() + qs2.count())
        