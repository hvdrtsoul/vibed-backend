import re

from jsonrpcclient import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import Track, ListeningSession
from .serializers import TrackSerializer
from .solana_utils import reward_user_with_tokens
from tasks import reward_user_async

from django.http import StreamingHttpResponse, HttpResponseNotModified
from wsgiref.util import FileWrapper
import os

class TrackListView(APIView):
    def get(self, request):
        tracks = Track.objects.all()
        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data)

class TrackCoverView(APIView):
    def get(self, request, pk):
        track = get_object_or_404(Track, pk=pk)

        cover_path = track.cover_image.path
        return FileResponse(open(cover_path, 'rb'), content_type='image/jpeg')

class TrackStreamView(APIView):

    def get(self, request, pk):
        track = get_object_or_404(Track, pk=pk)
        """
        session = ListeningSession.objects.create(user=request.user, track=track)

        if not session.rewarded:
            reward_user_async.delay(request.user.wallet_address, amount=1.0)
            session.rewarded = True
            session.save()
        """
        file_path = track.audio_file.path
        file_size = os.path.getsize(file_path)

        range_header = request.headers.get('Range', '').strip()
        if range_header:
            print("RANGE HEADER")
            range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
            if range_match:
                start = int(range_match.group(1))
                end = int(range_match.group(2) or file_size - 1)
                length = end - start + 1

                response = StreamingHttpResponse(open(file_path, 'rb'), status=206)
                response['Content-Type'] = 'audio/mpeg'
                response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
                response['Content-Length'] = str(length)
                response['Accept-Ranges'] = 'bytes'
                response.streaming_content = self.read_file_chunks(file_path, start, end)
                return response

        response = StreamingHttpResponse(open(file_path, 'rb'), content_type='audio/mpeg')
        response['Content-Length'] = str(file_size)
        response['Accept-Ranges'] = 'bytes'
        return response

    def read_file_chunks(self, file_path, start, end, chunk_size=8192):
        with open(file_path, 'rb') as f:
            f.seek(start)
            remaining = end - start + 1
            while remaining > 0:
                chunk = f.read(min(chunk_size, remaining))
                if not chunk:
                    break
                yield chunk
                remaining -= len(chunk)