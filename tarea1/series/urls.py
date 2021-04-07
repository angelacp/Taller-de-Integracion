from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("<str:serie>/<int:season_id>/", views.season_detail, name="season_detail"),
	path("<str:name>/", views.character_detail, name="character_detail"),
	path("search", views.search_results, name="search_results"),
]