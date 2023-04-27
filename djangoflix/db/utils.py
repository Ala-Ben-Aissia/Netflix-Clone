import string, random
from django.utils.text import slugify

def get_random_string(size=4, chars=string.ascii_lowercase + string.digits):
    return "-" + "".join([random.choice(chars) for _ in range(size)])

def get_unique_slug(instance, new_slug=None):
    title = instance.title
    rand_str = get_random_string()
    if new_slug is None:
        slug = slugify(title) # Default Iteration
    else:
        slug = new_slug # Recursive Iteration
    klass = instance.__class__
    parent = None
    try:
        parent = instance.parent
    except:
        pass
    if parent is not None:
        qs = klass.objects.filter(parent=parent, slug=slug) # Smaller Lookup during a long run
    else:
        qs = klass.objects.filter(slug=slug)
    if qs.exists():
        new_slug = slugify(title) + rand_str
        return get_unique_slug(instance, new_slug=new_slug)
    return slug