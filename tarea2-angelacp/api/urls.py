#from django.conf.urls import url 
from django.urls import path
from api import views 
 
urlpatterns = [ 
   path('api/artists', views.artist_list, name='artist-list'),
   path('api/artists/<str:artist_id>', views.artist_detail, name='artist-detail'),
   path('api/artists/<str:artist_id>/albums/play', views.artist_play, name='artist-play'),

   path('api/albums', views.album_menu, name='album-menu'),
   path('api/artists/<str:artist_id>/albums', views.album_list, name='album-list'),
   path('api/albums/<str:album_id>', views.album_detail, name='album-detail'),
   path('api/albums/<str:album_id>/tracks/play', views.album_play, name='album-play'),

   path('api/tracks', views.track_menu, name='track-menu'),
   path('api/albums/<str:album_id>/tracks', views.track_list, name='track-list'),
   path('api/tracks/<str:track_id>', views.track_detail, name='track-detail'),
   path('api/artists/<str:artist_id>/tracks', views.track_list_artist, name='track-list-artist'),
   path('api/tracks/<str:track_id>/play', views.track_play, name='track-play')
]