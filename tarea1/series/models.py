from django.db import models

# Create your models here.

class Character(models.Model):
	character_id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100)
	occupation = models.JSONField()
	img = models.CharField(max_length=200)
	status = models.CharField(max_length=100)
	nickname = models.CharField(max_length=100)
	appearance = models.JSONField()
	better_call_saul_appearance = models.JSONField()
	portrayed = models.CharField(max_length=100)
	category = models.JSONField()

class Episode(models.Model):
	episode_id = models.IntegerField(primary_key=True)
	title = models.CharField(max_length=100)
	season = models.IntegerField()
	episode = models.IntegerField()
	air_date = models.CharField(max_length=100)
	characters = models.JSONField()
	series = models.CharField(max_length=100)

class Quote(models.Model):
	quote_id = models.IntegerField(primary_key=True)
	quote = models.TextField()
	author = models.CharField(max_length=100)
	series = models.CharField(max_length=100)

class Season(models.Model):
	season_id = models.IntegerField()
	serie = models.CharField(max_length=100)
	# episodes para una season s: s.episodes_set.objects.all()
"""
class Serie(models.Model):
	name = models.CharField(max_length=100)
	# seasons para una serie s: s.seasons_set.objects.all()

class Season(models.Model):
	id_season = models.IntegerField()
	serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
	# episodes para una season s: s.episodes_set.objects.all()

class Episode(models.Model):
	episode_id = models.IntegerField(primary_key=True)
	title = models.CharField(max_length=100)
	episode = models.IntegerField()
	season = models.ForeignKey(Season, on_delete=models.CASCADE)
	air_date = models.CharField(max_length=100)
	# characters para un episode e: e.characters_set.objects.all()

class Character(models.Model):
	character_id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100)
	occupation = models.TextField()
	img = models.CharField(max_length=200)
	status = models.CharField(max_length=100)
	nickname = models.CharField(max_length=100)
	seasons = models.ManyToManyField(Season)
	#appearance =  #array de temporadas en breaking bad
	#better_call_saul_appearance = # array de temps de better call saul
	portrayed = models.CharField(max_length=100)
	category = models.ManyToManyField(Serie)
	episodes = models.ManyToManyField(Episode)
	# quotes para un character c: c.quotes_set.objects.all()

class Quote(models.Model):
	quote_id = models.IntegerField(primary_key=True)
	quote = models.TextField()
	author = models.ForeignKey(Character, on_delete=models.CASCADE)
	series = models.ForeignKey(Serie, on_delete=models.CASCADE)
"""