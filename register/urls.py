from django.urls import path

from . import views

urlpatterns = [
    path('', views.indexview, name='Avaleht'),
    path('details', views.detailsview, name='Osaühingu andmete vaade'),
    path('add', views.addview, name='Osaühingu asutamise vorm'),
    path('edit', views.editview, name='Osaühingu osakapitali suurendamise vorm')
]
