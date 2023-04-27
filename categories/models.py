from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from tags.models import TaggedItem
from playlists.models import *
from django.db.models.signals import post_save
from djangoflix.db.receivers import slugify_post_save
from django.http import Http404
# Create your models here.

class Category(models.Model):
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)
    tags = GenericRelation(TaggedItem, related_query_name='category')
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    def get_absolute_url(self):
        return f"/categories/{self.slug}/"

def category_pre_save(sender, instance, *args, **kwargs):
    instance.title = f"{instance.title}".title()
    
        
    

pre_save.connect(category_pre_save, sender=Category)    
post_save.connect(slugify_post_save, sender=Category)        

    