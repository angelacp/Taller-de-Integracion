from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.renderers import JSONRenderer
 
from api.models import Artist, Album, Track
from api.serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
from rest_framework.decorators import api_view

import io

from base64 import b64encode

""" ARTISTS """

# POST /artists, 
# GET /artists
@api_view(['GET', 'POST'])
def artist_list(request):
	if request.method == 'GET':
		results = Artist.objects.all()
		name = request.GET.get('name', None)
		if name is not None:
			results = results.filter(name__icontains=name)
		serializer = ArtistSerializer(results, many=True)
		return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		try:
			string = data['name']
		except KeyError: # Falta el atributo name
			return JsonResponse(data=data, status=status.HTTP_400_BAD_REQUEST)
		data['id'] = b64encode(string.encode()).decode('utf-8')[0:22]
		artist = Artist.objects.filter(id=data['id'])
		if artist: # Ya existe un artista con este id, asi que lo retorno con error
			serializer = ArtistSerializer(artist[0])
			content = JSONRenderer().render(serializer.data)
			stream = io.BytesIO(content)
			data = JSONParser().parse(stream)
			return JsonResponse(data=data, status=status.HTTP_409_CONFLICT)
		# Si no, lo creo y lo retorno
		serializer = ArtistSerializer(data=data)
		if serializer.is_valid():
		    serializer.save()
		    return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
		# Otros errores de formato
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET /artists/<artist_id>
# DELETE /artists/<artist_id>
@api_view(['GET', 'DELETE'])
def artist_detail(request, artist_id):
	try: 
		artist = Artist.objects.get(pk=artist_id) 
	except Artist.DoesNotExist: # El artista no existe
		return JsonResponse({'message': 'The artist does not exist'}, status=status.HTTP_404_NOT_FOUND) 
	if request.method == 'GET': 
		serializer = ArtistSerializer(artist) 
		return JsonResponse(serializer.data, status=status.HTTP_200_OK) 
	elif request.method == 'DELETE': 
		artist.delete() 
	return JsonResponse({'message': 'Artist was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)    

# PUT /artists/<artist_id>/albums/play
@api_view(['PUT'])
def artist_play(request, artist_id):
	try: 
		artist = Artist.objects.get(pk=artist_id) 
	except Artist.DoesNotExist: 
		return JsonResponse({'message': 'The artist does not exist'}, status=status.HTTP_404_NOT_FOUND) 
	if request.method == 'PUT': 
		# Busco el artista para revisar sus tracks
		results = Track.objects.filter(artist_id=artist_id)
		for t in results:
			serializer = TrackSerializer(t)
			content = JSONRenderer().render(serializer.data)
			stream = io.BytesIO(content)
			data = JSONParser().parse(stream)
			data['times_played'] += 1
			serializer = TrackSerializer(t, data=data)
			if serializer.is_valid():
			    serializer.save()
		return JsonResponse(data={}, status=status.HTTP_200_OK)

""" ALBUMS"""

# GET /albums
@api_view(['GET'])
def album_menu(request):
	if request.method == 'GET':
		results = Album.objects.all()
		name = request.GET.get('name', None)
		if name is not None:
			results = results.filter(name__icontains=name)
		serializer = AlbumSerializer(results, many=True)
		return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
	
# POST /artists/<artist_id>/albums
# GET /artists/<artist_id>/albums
@api_view(['GET','POST'])
def album_list(request, artist_id): 
	if request.method == 'GET':
		try:
			artist = Artist.objects.get(pk=artist_id) 
		except Artist.DoesNotExist: # El artista no existe
			return JsonResponse(data={}, status=status.HTTP_404_NOT_FOUND)
		results = Album.objects.filter(artist_id=artist_id)
		serializer = AlbumSerializer(results, many=True) 
		return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
	elif request.method == 'POST':
		try:
			artist = Artist.objects.get(pk=artist_id) 
		except Artist.DoesNotExist: # El artista no existe
			return JsonResponse(data={}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
		data = JSONParser().parse(request)
		data['artist_id'] = artist_id
		try:
			string = data['name'] + ':' + artist_id
		except KeyError: # Falta el atributo name
			return JsonResponse(data=data, status=status.HTTP_400_BAD_REQUEST)
		data['id'] = b64encode(string.encode()).decode('utf-8')[0:22]
		album = Album.objects.filter(id=data['id'])
		if album: # Ya existe un album con ese id, asi que lo retorno con error
			serializer = AlbumSerializer(album[0])
			content = JSONRenderer().render(serializer.data)
			stream = io.BytesIO(content)
			data = JSONParser().parse(stream)
			return JsonResponse(data=data, status=status.HTTP_409_CONFLICT)
		# Si no, lo creo y lo retorno
		serializer = AlbumSerializer(data=data)
		if serializer.is_valid():
		    serializer.save()
		    return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
		# Otros errores de formato
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET /albums/<album_id>
# DELETE /albums/<album_id>
@api_view(['GET', 'DELETE'])
def album_detail(request, album_id):
	try: 
		album = Album.objects.get(pk=album_id) 
	except Album.DoesNotExist: # El album no existe
		return JsonResponse({'message': 'The album does not exist'}, status=status.HTTP_404_NOT_FOUND) 
	if request.method == 'GET': 
		serializer = AlbumSerializer(album) 
		return JsonResponse(serializer.data, status=status.HTTP_200_OK) 
	elif request.method == 'DELETE': 
		album.delete() 
	return JsonResponse({'message': 'Album was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)    

# PUT /albums/<album_id>/tracks/play
@api_view(['PUT'])
def album_play(request, album_id):
	try: 
		album = Album.objects.get(pk=album_id) 
	except Album.DoesNotExist: # El album no existe
		return JsonResponse({'message': 'The album does not exist'}, status=status.HTTP_404_NOT_FOUND) 
	if request.method == 'PUT': 
		# Busco el album para revisar sus tracks
		results = Track.objects.filter(album_id=album_id)
		for t in results:
			serializer = TrackSerializer(t)
			content = JSONRenderer().render(serializer.data)
			stream = io.BytesIO(content)
			data = JSONParser().parse(stream)
			data['times_played'] += 1
			serializer = TrackSerializer(t, data=data)
			if serializer.is_valid():
			    serializer.save()
		return JsonResponse(data={}, status=status.HTTP_200_OK) 


""" TRACKS """

# GET /tracks
@api_view(['GET'])
def track_menu(request):
	if request.method == 'GET':
		results = Track.objects.all()
		name = request.GET.get('name', None)
		if name is not None:
			results = results.filter(name__icontains=name)
		serializer = TrackSerializer(results, many=True)
		return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

# POST /albums/<album_id>/tracks
# GET /albums/<album_id>/tracks
@api_view(['GET','POST'])
def track_list(request, album_id):
	if request.method == 'GET': 
		try:
			album = Album.objects.get(pk=album_id) 
		except Album.DoesNotExist: # El album no existe
			return JsonResponse(data={}, status=status.HTTP_404_NOT_FOUND) 
		results = Track.objects.filter(album_id=album_id)
		serializer = TrackSerializer(results, many=True) 
		return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
	elif request.method == 'POST':
		try:
			album = Album.objects.get(pk=album_id) 
		except Album.DoesNotExist: # El album no existe
			return JsonResponse(data={}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
		data = JSONParser().parse(request)
		data['album_id'] = album_id
		data['artist_id'] = album.artist_id.id
		try:
			string = data['name'] + ':' + album_id
		except KeyError: # Falta el atributo name
			return JsonResponse(data=data, status=status.HTTP_400_BAD_REQUEST)
		data['id'] = b64encode(string.encode()).decode('utf-8')[0:22]
		track = Track.objects.filter(id=data['id'])
		if track: # Ya existe un track con este id, asi que lo retorno con error
			serializer = TrackSerializer(track[0])
			content = JSONRenderer().render(serializer.data)
			stream = io.BytesIO(content)
			data = JSONParser().parse(stream)
			return JsonResponse(data=data, status=status.HTTP_409_CONFLICT)
		# Si no, lo creo y lo retorno
		serializer = TrackSerializer(data=data)
		if serializer.is_valid():
		    serializer.save()
		    return JsonResponse(serializer.data, status=status.HTTP_201_CREATED) 
		# Otros errores de formato
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET /tracks/<track_id>
# DELETE /tracks/<track_id>
@api_view(['GET', 'DELETE'])
def track_detail(request, track_id):
	try: 
		track = Track.objects.get(pk=track_id) 
	except Track.DoesNotExist: # El track no existe
		return JsonResponse({'message': 'The track does not exist'}, status=status.HTTP_404_NOT_FOUND) 
	if request.method == 'GET': 
		serializer = TrackSerializer(track) 
		return JsonResponse(serializer.data, status=status.HTTP_200_OK) 
	elif request.method == 'DELETE': 
		track.delete() 
	return JsonResponse({'message': 'Track was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)    

# GET /artists/<artist_id>/tracks
@api_view(['GET'])
def track_list_artist(request, artist_id):
	try:
		artist = Artist.objects.get(pk=artist_id) 
	except Artist.DoesNotExist: # El artista no existe
	    return JsonResponse({'message': 'The artist does not exist'}, status=status.HTTP_404_NOT_FOUND) 
	if request.method == 'GET': 
		results = Track.objects.filter(artist_id=artist_id)
		serializer = TrackSerializer(results, many=True) 
		return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
	
# PUT /tracks/<track_id>/play
@api_view(['PUT'])
def track_play(request, track_id):
	try: 
		track = Track.objects.get(pk=track_id) 
	except Track.DoesNotExist: # El track no existe
		return JsonResponse({'message': 'The track does not exist'}, status=status.HTTP_404_NOT_FOUND) 
	if request.method == 'PUT': 
		# Busco el track
		serializer = TrackSerializer(track)
		content = JSONRenderer().render(serializer.data)
		stream = io.BytesIO(content)
		data = JSONParser().parse(stream)
		# Modifico su times_played
		data['times_played'] += 1
		# Lo vuelvo a serializar para guardarlo
		serializer = TrackSerializer(track, data=data)
		if serializer.is_valid():
		    serializer.save()
		    return JsonResponse(serializer.data, status=status.HTTP_200_OK) 
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		