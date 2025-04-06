# endpoint/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException # Import APIException

from .serializers import endpointRequestSerializer, endpointResponseSerializer
from .services import get_ai_response, AIServiceError # Import service function and custom error

class endpointAPIView(APIView):
    """
    API endpoint to interact with different AI endpoint models.
    """
    def post(self, request, *args, **kwargs):
        serializer = endpointRequestSerializer(data=request.data)
        if serializer.is_valid():
            model_name = serializer.validated_data['model']
            prompt = serializer.validated_data['prompt']

            try:
                ai_response = get_ai_response(model_name, prompt)
                response_data = {
                    "model": model_name,
                    "response": ai_response
                }
                response_serializer = endpointResponseSerializer(response_data)
                return Response(response_serializer.data, status=status.HTTP_200_OK)

            except AIServiceError as e:
                # Handle specific AI service errors (e.g., API key missing, service down)
                # These already inherit from APIException, so DRF handles them.
                # You can customize the response further if needed.
                # return Response({"error": str(e)}, status=e.status_code)
                raise e # Re-raise to let DRF handle formatting

            except ValueError as e:
                # Handle invalid model name errors from get_ai_response
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                # Catch any other unexpected errors during AI call
                print(f"Unexpected error in endpointAPIView: {e}") # Log the error
                # Return a generic server error
                raise APIException("An unexpected error occurred while processing your request.")

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)