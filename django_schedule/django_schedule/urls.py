from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('toca_schedule/', include('toca_schedule.urls')),
    path('accounts/', include('accounts.urls')),
    path('about/', views.about),
    path('', views.home),
]

urlpatterns += staticfiles_urlpatterns()

