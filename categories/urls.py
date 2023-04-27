from django.urls import path
from .views import *


urlpatterns = [
    path('', CategoryListView.as_view(), name='categories'),
    path('<slug:slug>/', CategoryDetailView.as_view(), name='category'),
]