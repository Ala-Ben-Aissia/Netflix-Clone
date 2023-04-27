from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import pre_save
# Create your models here.

class TaggedItemManager(models.Manager):
    def unique_tags(self):
        unique_tags = set(self.get_queryset().values_list('tag', flat=True))
        return sorted(unique_tags)

class TaggedItem(models.Model):
    
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    
    objects = TaggedItemManager()
    
      
def lowercase_tag_pre_save(sender, instance, *args, **kwargs):
    instance.tag = f"{instance.tag}".lower()
    
pre_save.connect(lowercase_tag_pre_save, sender=TaggedItem)