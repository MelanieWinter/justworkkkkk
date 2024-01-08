from django import forms
from .models import Song

class SongSelectionForm(forms.Form):
    selected_songs = forms.ModelMultipleChoiceField(
        queryset=Song.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )