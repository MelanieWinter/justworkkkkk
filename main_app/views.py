from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from .spotify import get_spotify_data
from django.db import models
from .forms import SongSelectionForm, PlaylistForm
from .models import Song, Playlist


def home(request):
    songs, tracks = None, None

    if request.method == 'POST':
        artist_query = request.POST.get('artist_query')
        track_query = request.POST.get('track_query')

        if artist_query:
            songs = get_spotify_data(artist_query, search_type='artist')

        if track_query:
            tracks = get_spotify_data(track_query, search_type='track')

    return render(request, 'home.html', {'songs': songs, 'tracks': tracks})

def process_song_selection(request):
    if request.method == 'POST':
        selected_song_ids = request.POST.getlist('selected_songs')

        # Update the 'selected' field for the selected songs
        Song.objects.filter(spotify_id__in=selected_song_ids).update(selected=True)
        return render(request, 'home.html', {})
    
class PlaylistCreate(CreateView):
    model = Playlist
    fields = ['name', 'description', 'songs']

    def form_valid(self, form):
        form.instance.user = self.request.user
        result = super().form_valid(form)
        return result
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = Song.objects.all()
        context['playlist_form'] = PlaylistForm()
        return context

class PlaylistCreate(CreateView):
    model = Playlist
    fields = ['name', 'description', 'songs']

    def form_valid(self, form):
        form.instance.user = self.request.user
        result = super().form_valid(form)
        return result
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = Song.objects.all()
        context['playlist_form'] = PlaylistForm()
        return context

