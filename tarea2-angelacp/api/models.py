from django.db import models

# Create your models here.
class Artist(models.Model):
	id = models.CharField(max_length=22, primary_key=True, default=None)
	name = models.CharField(max_length=250)
	age = models.IntegerField()
	# albums = url
	# tracks = url
	#self = models.CharField(max_length=250, default=None)

class Album(models.Model):
	id = models.CharField(max_length=22, primary_key=True, default=None)
	name = models.CharField(max_length=250)
	genre = models.CharField(max_length=50)
	artist_id = models.ForeignKey(Artist, related_name='albums', on_delete=models.CASCADE)
	# artist = url
	# tracks = url
	#self = models.CharField(max_length=250, default=None)

	def __str__(self):
		return '%s - %s' % (self.name, self.genre)

class Track(models.Model):
	id = models.CharField(max_length=22, primary_key=True, default=None)
	name = models.CharField(max_length=250)
	duration = models.FloatField()
	times_played = models.IntegerField(default=0)
	album_id = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
	artist_id = models.ForeignKey(Artist, related_name='tracks', on_delete=models.CASCADE)
	# artists = url
	# album = url
	#self = models.CharField(max_length=250, default=None)