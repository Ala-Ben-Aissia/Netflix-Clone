from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from django.db.models import Avg
from django.db.models.signals import post_save
# Create your models here.

User = settings.AUTH_USER_MODEL # auth.User

class RatingQuerySet(models.QuerySet):
    def rating(self):
        return self.aggregate(average=Avg('value'))['average']
    
class RatingManager(models.Manager):
    def get_queryset(self):
        return RatingQuerySet(self.model, using=self._db)

class RatingChoices(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    __empty__ = 'Rate Me'


class Rating(models.Model):
     
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    value = models.PositiveIntegerField(choices=RatingChoices.choices, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    
    objects = RatingManager()
    
def rating_post_save(sender, instance, created, *args, **kwargs):
    if created:
        user = instance.user
        content_type = instance.content_type
        object_id = instance.object_id
        qs = Rating.objects.filter(user=user, content_type=content_type, object_id=object_id).exclude(pk=instance.pk)
        # exclude(pk=instance.pk) => exclude the current rating wich should be the user rating
        if qs.exists():
            qs.delete()
            
post_save.connect(receiver=rating_post_save, sender=Rating)