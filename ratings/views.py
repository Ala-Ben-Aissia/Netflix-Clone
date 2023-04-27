from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RatingForm
from .models import Rating
from django.contrib.contenttypes.models import ContentType
# Create your views here.

def rate_view(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data.get('rating')
            content_type_id = form.cleaned_data.get('content_type_id')
            c_type = ContentType.objects.get_for_id(content_type_id)
            object_id = form.cleaned_data.get('object_id')
            next_path = form.cleaned_data.get('next')
            obj = Rating.objects.create(
                user = request.user,
                value = rating,
                content_type = c_type,
                object_id = object_id,
            )
            return HttpResponseRedirect(next_path)
    return HttpResponseRedirect('/')
