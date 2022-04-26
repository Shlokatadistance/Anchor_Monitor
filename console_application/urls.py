from django.urls import path

from . import views
from .views import *

#views file, index is a function in that file

urlpatterns = [ path('', anchor_view.as_view(template_name='viewer.html'), name='Anchor View'),
path('next_viewer',anchor_next_view.as_view(template_name='next_viewer.html'),name='next_viewer'),]

