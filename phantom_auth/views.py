# phantom_auth/views.py
import secrets
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PhantomNonce
from .utils import verify_signature
from .serializers import ConnectInitSerializer, VerifySignatureSerializer

User = get_user_model()

class InitConnectView(APIView):
    def post(self, request):
        serializer = ConnectInitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        public_key = serializer.validated_data['public_key']

        nonce = secrets.token_urlsafe(32)
        PhantomNonce.objects.update_or_create(
            public_key=public_key,
            defaults={'nonce': nonce}
        )
        return Response({'message': nonce})


class VerifySignatureView(APIView):
    def post(self, request):
        serializer = VerifySignatureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        public_key = serializer.validated_data['public_key']
        signature = serializer.validated_data['signature']

        try:
            nonce_obj = PhantomNonce.objects.get(public_key=public_key)
        except PhantomNonce.DoesNotExist:
            return Response({'detail': 'Nonce not found'}, status=400)

        if nonce_obj.is_expired():
            nonce_obj.delete()
            return Response({'detail': 'Nonce expired'}, status=403)

        if not verify_signature(public_key, signature, nonce_obj.nonce):
            return Response({'detail': 'Invalid signature'}, status=403)

        nonce_obj.delete()

        user, created = User.objects.get_or_create(public_key=public_key)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })