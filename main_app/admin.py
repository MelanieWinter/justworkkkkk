from django.contrib import admin
from .models import Song, Playlist, Photo


# Register your models her
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(Photo)