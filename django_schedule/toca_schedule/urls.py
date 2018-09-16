from django.urls import path, include
from . import views

app_name = 'toca_schedule'
urlpatterns = [
    path('', views.schedule_list, name="list"),
    path('<job_id>', views.schedule_detail, name='detail'),
    path('create/', views.schedule_create, name="create"),
    path('<job_id>/delete/', views.schedule_delete, name="delete"),
]
