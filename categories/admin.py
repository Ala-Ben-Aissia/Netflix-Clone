from django.contrib import admin
from .models import Category
from tags.admin import TaggedItemInline
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    class Meta:
        model = Category

admin.site.register(Category, CategoryAdmin)