import re

from django.utils import timezone
from jsonrpcclient import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import Track, ListeningSession
from .serializers import TrackSerializer
from tasks import reward_user_async
from .utils import request_airdrop
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

class RewardUserView(APIView):
    def post(self, request):
        public_key = request.data.get("public_key")

        if not public_key:
            return Response({"error": "public_key is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = requests.post(
                "http://localhost:3000/airdrop",
                json={"user": public_key, "amount": 1_000_000_000},  # 1 токен с 9 знаками после запятой
                timeout=10
            )

            if response.status_code == 200:
                return Response({"status": "success"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "airdrop failed", "details": response.text}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.exceptions.RequestException as e:
            return Response({"error": "request failed", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StartSessionView(APIView):

    def post(self, request, pk):
        public_key = request.data.get("public_key")
        if not public_key:
            return Response({"error": "public_key is required"}, status=status.HTTP_400_BAD_REQUEST)

        track = get_object_or_404(Track, pk=pk)
        session = ListeningSession.objects.create(public_key=public_key, track=track)
        return Response({"session_id": session.id, "start_time": session.start_time}, status=status.HTTP_201_CREATED)


class EndSessionView(APIView):

    def post(self, request, pk):
        public_key = request.data.get("public_key")
        session_id = request.data.get("session_id")

        if not public_key or not session_id:
            return Response({"error": "public_key and session_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        session = get_object_or_404(ListeningSession, id=session_id, public_key=public_key, track__pk=pk)

        if session.end_time is not None:
            return Response({"status": "already_ended"}, status=status.HTTP_200_OK)

        session.end_time = timezone.now()
        session.save()

        if session.duration() >= 30 and not session.rewarded:
            self._airdrop(public_key, amount=1_000_000_000)
            session.rewarded = True
            session.save()
            return Response({"status": "rewarded", "duration": session.duration()}, status=status.HTTP_200_OK)

        return Response({"status": "not_eligible", "duration": session.duration()}, status=status.HTTP_200_OK)

    def _airdrop(self, public_key, amount):
        try:
            resp = requests.post(
                "http://localhost:3000/airdrop",
                json={"user": public_key, "amount": amount},
                timeout=10,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            print("Airdrop error:", e)

