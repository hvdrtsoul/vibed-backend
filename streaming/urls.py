from django.urls import path
from .views import TrackListView, TrackStreamView, TrackCoverView

urlpatterns = [
    path('tracks/', TrackListView.as_view(), name='track-list'),
    path('tracks/<int:pk>/stream/', TrackStreamView.as_view(), name='track-stream'),
path('tracks/<int:pk>/cover', TrackCoverView.as_view(), name='track-cover'),
]
