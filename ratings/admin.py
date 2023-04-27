from django.contrib import admin
from .models import Rating
# Register your models here.

class RatingAdmin(admin.ModelAdmin):
    fields = ['user', 'content_type', 'object_id', 'content_object', 'value']
    readonly_fields = ['content_object']

admin.site.register(Rating, RatingAdmin)