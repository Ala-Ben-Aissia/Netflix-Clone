from django.urls import path
from .views import *


urlpatterns = [
    path('', TaggedItemListView.as_view(), name='tags'),
    path('<slug:tag>/', TaggedItemDetailView.as_view(), name='tagged_items'),
]