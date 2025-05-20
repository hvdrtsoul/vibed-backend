from rest_framework import serializers

class ConnectInitSerializer(serializers.Serializer):
    public_key = serializers.CharField()

class VerifySignatureSerializer(serializers.Serializer):
    public_key = serializers.CharField()
    signature = serializers.CharField()
