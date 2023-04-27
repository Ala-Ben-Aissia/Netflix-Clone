from django.test import TestCase
from .models import Video, StateOptions
from django.utils import timezone
from django.utils.text import slugify
# Create your tests here.

class VideoModelTestCase(TestCase):
    def setUp(self):
        self.obj_a = Video.objects.create(title='some title', video_id='abc')
        self.obj_b = Video.objects.create(title='some title', state=StateOptions.PUBLISH, video_id='def')
        self.obj_c = Video.objects.create(title='some title', video_id='ghi')

    
    def test_slug_field(self):
        title = self.obj_a.title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.obj_a.slug)
     
    def test_unique_slug(slef):
        slef.assertNotEqual(slef.obj_a.slug, slef.obj_b.slug, slef.obj_c.slug)
      
    def test_valid_title(self):
        title = self.obj_a.title
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())
        
    def test_created_count(self):
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 3)
        
    def test_draft_case(self):
        qs = Video.objects.filter(state=StateOptions.DRAFT)
        self.assertTrue(qs.exists())
        self.assertFalse(self.obj_a.is_published, self.obj_c.is_published)
        
    def test_publish_case(self):
        now = timezone.now()
        published_qs = Video.objects.filter(state=StateOptions.PUBLISH, publish_timestamp__lte=now)
        self.assertTrue(published_qs.exists())
        self.assertTrue(self.obj_b.is_published)

        
    def test_video_manager(self):
        published_qs1 = Video.objects.all().published() # VideoQuerySet
        published_qs2 = Video.objects.published() # VideoManager
        self.assertQuerysetEqual(published_qs1, published_qs2)
        self.assertEqual(published_qs1.count(), published_qs2.count())