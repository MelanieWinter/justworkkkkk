from django import forms
from .models import Song, Playlist

class SongSelectionForm(forms.Form):
    selected_songs = forms.ModelMultipleChoiceField(
        queryset=Song.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

class PlaylistForm(forms.ModelForm):
    songs = forms.ModelMultipleChoiceField(
        queryset=Song.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Playlist
        fields = ['name', 'description', 'songs']