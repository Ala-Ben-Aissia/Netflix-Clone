from .models import StateOptions
from django.utils import timezone
from .utils import get_unique_slug

def publish_state_pre_save(sender, instance, *args, **kwargs):
    is_publish = instance.state == StateOptions.PUBLISH
    is_draft = instance.state == StateOptions.DRAFT
    if is_publish:
        instance.publish_timestamp = timezone.now()
    elif is_draft:
        instance.publish_timestamp = None
        
def slugify_post_save(sender, instance, *args, **kwargs): 
        if instance.slug is None:
            instance.slug = get_unique_slug(instance)
            instance.save()