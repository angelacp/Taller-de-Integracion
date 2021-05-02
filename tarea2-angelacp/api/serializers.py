from rest_framework import serializers 
from api.models import Artist, Album, Track
 
from base64 import b64encode

class ArtistSerializer(serializers.ModelSerializer):
 	#albums = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
 	#tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
 	self = serializers.SerializerMethodField('get_self')
 	albums = serializers.SerializerMethodField('get_albums')
 	tracks = serializers.SerializerMethodField('get_tracks')

 	class Meta:
 		model = Artist
 		fields = ('id', 'name', 'age', 'self', 'albums', 'tracks')

 	def get_self(self, artist):
 		return('https://tarea2-angelacp.herokuapp.com/api/artists/' + artist.id)

 	def get_albums(self, artist):
 		return('https://tarea2-angelacp.herokuapp.com/api/artists/' + artist.id + '/albums')

 	def get_tracks(self, artist):
 		return('https://tarea2-angelacp.herokuapp.com/api/artists/' + artist.id + '/tracks')

class AlbumSerializer(serializers.ModelSerializer):
	artist_id = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all(), many=False)
	#tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	self = serializers.SerializerMethodField('get_self')
	artist = serializers.SerializerMethodField('get_artist')
	tracks = serializers.SerializerMethodField('get_tracks')

	class Meta:
		model = Album
		fields = ('id', 'name', 'genre', 'artist_id', 'self', 'artist', 'tracks')
	
	def get_self(self, album):
 		return('https://tarea2-angelacp.herokuapp.com/api/albums/' + album.id)

	def get_artist(self, album):
		return('https://tarea2-angelacp.herokuapp.com/api/artists/' + album.artist_id.id)

	def get_tracks(self, album):
		return('https://tarea2-angelacp.herokuapp.com/api/albums/' + album.id + '/tracks')

class TrackSerializer(serializers.ModelSerializer):
	album_id = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all(), many=False)
	artist_id = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all(), many=False)
 	#album = serializers.HyperlinkedRelatedField(queryset=Album.objects.all(), many=False, view_name='album-detail')
 	#artist = serializers.HyperlinkedRelatedField(queryset=Artist.objects.all(), many=False, view_name='artist-detail')
	self = serializers.SerializerMethodField('get_self')
	artist = serializers.SerializerMethodField('get_artist')
	album = serializers.SerializerMethodField('get_album')

	class Meta:
		model = Track
		fields = ('id', 'name', 'duration', 'times_played', 'album_id', 'artist_id', 'self', 'album', 'artist')

	def get_self(self, track):
 		return('https://tarea2-angelacp.herokuapp.com/api/tracks/' + track.id)

	def get_artist(self, track):
		return('https://tarea2-angelacp.herokuapp.com/api/artists/' + track.artist_id.id)

	def get_album(self, track):
		return('https://tarea2-angelacp.herokuapp.com/api/albums/' + track.album_id.id)