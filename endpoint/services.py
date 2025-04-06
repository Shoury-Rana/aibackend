# endpoint/services.py
import os
from django.conf import settings
import openai
import google.generativeai as genai
import anthropic
from rest_framework.exceptions import APIException

# --- Configure API Clients ---

# OpenAI
if settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY
else:
    print("Warning: OPENAI_API_KEY not found in settings.")

# Google Gemini
if settings.GEMINI_API_KEY:
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
    except Exception as e:
        print(f"Warning: Failed to configure Google Gemini: {e}")
else:
    print("Warning: GEMINI_API_KEY not found in settings.")

# Anthropic Claude
if settings.ANTHROPIC_API_KEY:
    try:
        anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    except Exception as e:
        print(f"Warning: Failed to configure Anthropic Claude: {e}")
        anthropic_client = None
else:
    print("Warning: ANTHROPIC_API_KEY not found in settings.")
    anthropic_client = None

# --- Service Functions ---

class AIServiceError(APIException):
    status_code = 503
    default_detail = 'AI service temporarily unavailable, please try again later.'
    default_code = 'ai_service_unavailable'

def call_endpointgpt(prompt: str) -> str:
    """Calls the OpenAI endpointGPT API."""
    if not settings.OPENAI_API_KEY:
        raise AIServiceError("OpenAI API key not configured.")
    try:
        # Using the newer client structure if available (adjust based on your openai lib version)
        client = openai.OpenAI() # Assumes API key is set via env var or openai.api_key
        response = client.endpoint.completions.create(
            model="gpt-3.5-turbo", # Or "gpt-4" etc.
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        # Check if response and choices are valid before accessing
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content.strip()
        else:
            raise AIServiceError("Invalid response structure received from OpenAI.")

    except openai.APIError as e:
        print(f"OpenAI API Error: {e}")
        raise AIServiceError(f"OpenAI API error: {e.status_code}")
    except Exception as e:
        print(f"Error calling endpointGPT: {e}")
        raise AIServiceError("An unexpected error occurred with OpenAI.")


def call_gemini(prompt: str) -> str:
    """Calls the Google Gemini API."""
    if not settings.GEMINI_API_KEY:
         raise AIServiceError("Gemini API key not configured.")
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        # Add more robust error handling/checking based on Gemini's response structure
        if response.parts:
             return response.text # Accessing the text directly if available
        elif response.prompt_feedback and response.prompt_feedback.block_reason:
             raise AIServiceError(f"Gemini request blocked: {response.prompt_feedback.block_reason.name}")
        else:
             # Fallback or inspect response structure if .text isn't directly available
             print("Gemini Response:", response) # Log for debugging
             raise AIServiceError("Unexpected response structure from Gemini.")

    except Exception as e:
        # Catch specific Google API errors if possible, otherwise generic
        print(f"Error calling Gemini: {e}")
        # You might want to check the type of exception e here
        raise AIServiceError("An error occurred with Google Gemini.")


def call_claude(prompt: str) -> str:
    """Calls the Anthropic Claude API."""
    global anthropic_client # Access the globally configured client
    if not settings.ANTHROPIC_API_KEY or anthropic_client is None:
        raise AIServiceError("Anthropic API key not configured or client failed to initialize.")
    try:
        message = anthropic_client.messages.create(
            model="claude-3-opus-20240229", # Or other Claude models like sonnet, haiku
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        # Check response structure before accessing
        if message.content and isinstance(message.content, list) and message.content[0].text:
            return message.content[0].text.strip()
        else:
             raise AIServiceError("Invalid response structure received from Anthropic.")

    except anthropic.APIError as e:
        print(f"Anthropic API Error: {e}")
        raise AIServiceError(f"Anthropic API error: {e.status_code}")
    except Exception as e:
        print(f"Error calling Claude: {e}")
        raise AIServiceError("An unexpected error occurred with Anthropic Claude.")

# --- Main Dispatcher ---

SUPPORTED_MODELS = {
    "endpointgpt": call_endpointgpt,
    "gemini": call_gemini,
    "claude": call_claude,
}

def get_ai_response(model_name: str, prompt: str) -> str:
    """
    Dispatches the request to the correct AI model service.
    """
    model_func = SUPPORTED_MODELS.get(model_name.lower())

    if not model_func:
        raise ValueError(f"Unsupported model: {model_name}. Supported models are: {', '.join(SUPPORTED_MODELS.keys())}")

    return model_func(prompt)