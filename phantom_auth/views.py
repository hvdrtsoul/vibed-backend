# phantom_auth/views.py
import secrets

import requests
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

class TokenBalanceView(APIView):
    def post(self, request):
        public_key = request.data.get("publicKey")
        if not public_key:
            return Response({"error": "publicKey is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = requests.post(
                "http://localhost:3000/balance",
                json={"publicKey": public_key},
                timeout=5
            )
            response.raise_for_status()
            balance_data = response.json()

            raw_balance = balance_data.get("balance")
            if raw_balance is None:
                return Response({"error": "Balance not found in response"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            balance_float = float(raw_balance) / 1_000_000_000

            return Response({"balance": balance_float})

        except requests.RequestException as e:
            return Response(
                {"error": f"Request to balance service failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
