from django.urls import path
from . import views

urlpatterns = [
    path('', views.subject_list, name='subject_list'),
    path('get_total_sem/', views.get_total_sem, name='get_total_sem'),
    path('add/', views.add_subject, name='add_subject'),
    path('edit/<int:id>/', views.edit_subject, name='edit_subject'),
    path('delete/<int:id>/', views.delete_subject, name='delete_subject'),

]
