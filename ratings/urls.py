from django.urls import path
from .views import *


urlpatterns = [
    path('', rate_view, name='rate' ),
    
]