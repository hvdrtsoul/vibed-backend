from django.contrib import admin
from .models import Track, ListeningSessionModel

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist')
    search_fields = ('title', 'artist')

@admin.register(ListeningSessionModel)
class ListeningSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'started_at', 'listened_seconds', 'rewarded')
    list_filter = ('rewarded',)
