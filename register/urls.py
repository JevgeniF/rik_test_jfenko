from django.urls import path

from . import views

# Array of url patterns used for navigation between screens of register app
urlpatterns = [
    path('', views.indexview, name='Avaleht'),
    path('details/<int:oy_id>', views.detailsview, name='Osaühingu andmete vaade'),
    path('add', views.addview, name='Osaühingu asutamise vorm'),
    path('edit/<int:oy_id>', views.editview, name='Osaühingu osakapitali suurendamise vorm')
]
