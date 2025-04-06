# endpoint/serializers.py
from rest_framework import serializers
from .services import SUPPORTED_MODELS # Import supported models list

class endpointRequestSerializer(serializers.Serializer):
    model = serializers.CharField(max_length=50)
    prompt = serializers.CharField()

    def validate_model(self, value):
        """Check if the requested model is supported."""
        if value.lower() not in SUPPORTED_MODELS:
            raise serializers.ValidationError(
                f"Unsupported model: '{value}'. "
                f"Available models: {', '.join(SUPPORTED_MODELS.keys())}"
            )
        return value.lower() # Return lowercase model name

class endpointResponseSerializer(serializers.Serializer):
    model = serializers.CharField(max_length=50)
    response = serializers.CharField()