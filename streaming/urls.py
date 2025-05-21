from django.urls import path
from .views import TrackListView, TrackStreamView, TrackCoverView, RewardUserView, StartSessionView, EndSessionView

urlpatterns = [
    path('tracks/', TrackListView.as_view(), name='track-list'),
    path('tracks/<int:pk>/stream/', TrackStreamView.as_view(), name='track-stream'),
    path('tracks/<int:pk>/cover', TrackCoverView.as_view(), name='track-cover'),
    path('get-reward', RewardUserView.as_view(), name='get-reward'),
    path("track/<int:pk>/start/", StartSessionView.as_view(), name="start-session"),
    path("track/<int:pk>/end/", EndSessionView.as_view(), name="end-session"),
]
