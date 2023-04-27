from django.test import TestCase
from .models import Video, MovieProxy, StateOptions
from django.utils.text import slugify
# Create your tests here.

class MovieProxyTestCase(TestCase):
    
    def create_movie_with_videos(self):
        
        video1 = Video.objects.create(title='video 1', video_id="zrv")
        video2 = Video.objects.create(title='video 2', video_id="zefz")
        video3 = Video.objects.create(title='video 3', video_id="zrgz")
        video_qs = Video.objects.all()
        self.video1 = video1
        self.video2 = video2
        self.video3 = video3
        self.video_qs = video_qs
         
        
    def setUp(self):
        self.create_movie_with_videos()
        movie_a = MovieProxy.objects.create(title='movie a', video=self.video1, state=StateOptions.PUBLISH)
        movie_b = MovieProxy.objects.create(title='movie b', video=self.video1)
        self.movie_a = movie_a
        self.movie_b = movie_b
        movie_a.videos.set(self.video_qs)
        # playlist_a.save()

 
        
    def test_movie_video(self):
        self.assertEqual(self.movie_a.video, self.video1) # comparing (the playlist's video instance, the created video)
    
    def test_movie_clips(self):
        clips_count = self.movie_a.videos.all().count()
        self.assertEqual(clips_count, 3)
   
    
    def test_slug_field(self):
        title = self.movie_a.title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.movie_a.slug)
      
    def test_valid_title(self):
        title = self.movie_a.title
        qs = MovieProxy.objects.filter(title=title)
        self.assertTrue(qs.exists())
        
    def test_draft_case(self):
        qs = MovieProxy.objects.filter(state=StateOptions.DRAFT)
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), 1)
        
    # def test_publish_case(self):
    #     now = timezone.now()
    #     published_qs = Playlist.objects.filter(state=StateOptions.PUBLISH, publish_timestamp__lte=now)
    #     self.assertTrue(published_qs.exists())
        
    def test_Playlist_manager(self):
        published_qs1 = MovieProxy.objects.all().published() # PlaylistQuerySet
        published_qs2 = MovieProxy.objects.published() # PlaylistManager
        self.assertQuerysetEqual(published_qs1, published_qs2)
        self.assertEqual(published_qs1.count(), published_qs2.count())