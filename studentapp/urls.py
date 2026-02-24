from django.urls import path
from . import views

urlpatterns = [
    path('', views.stream_list, name='stream_list'),
    path('add/',views.add_stream, name='stream_add'),
    path('edit/<int:id>/',views.edit_stream, name='stream_edit'),
    path('delete/<int:stream_id>', views.delete_stream, name='delete_stream')
]


# localhost:8000/stream/


# Function based view (HttpRequest & HttpResponse)
# Class based View