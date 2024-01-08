from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.home, name='home'),
    path('process_song_selection/', views.process_song_selection, name='process_song_selection'),
    path('playlists/create/', views.PlaylistCreate.as_view(), name='playlists_create'),
]

