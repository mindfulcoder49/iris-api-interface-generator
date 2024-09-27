# views.py

from rest_framework import viewsets
from .models import APIQuery, APIQueryTemplate
from .serializers import APIQuerySerializer, APIQueryTemplateSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
import openai
from openai import OpenAI
import json
from django.conf import settings
import requests

class APIQueryViewSet(viewsets.ModelViewSet):
    queryset = APIQuery.objects.all().order_by('-created_at')
    serializer_class = APIQuerySerializer

class APIQueryTemplateViewSet(viewsets.ModelViewSet):
    queryset = APIQueryTemplate.objects.all().order_by('-created_at')
    serializer_class = APIQueryTemplateSerializer

@api_view(['GET'])
def get_templates(request):
    templates = APIQueryTemplate.objects.all()
    serializer = APIQueryTemplateSerializer(templates, many=True)
    
    # Modify the serialized data to parse the form_fields string
    modified_data = serializer.data
    for template in modified_data:
        form_fields_str = template.get('form_fields', '[]')
        try:
            template['form_fields'] = json.loads(form_fields_str)
        except json.JSONDecodeError:
            template['form_fields'] = []  # Default to empty list if there's a JSON parsing error
    
    return Response(modified_data)


@api_view(['POST'])
def save_query(request):
    # Extract data from the request
    response_text = request.data.get('response')
    query_text = request.data.get('query', '')  # Default to empty string if not provided

    if not response_text:
        return Response({'error': 'No response data provided.'}, status=400)

    # Create a new APIQuery instance
    api_query = APIQuery(query=query_text, response=response_text)
    api_query.save()

    return Response({'message': 'Query saved successfully!'})

@api_view(['POST'])
def save_template(request):
    form_fields = request.data.get('form_fields')
    base_url = request.data.get('base_url')

    if not form_fields or not base_url:
        return Response({'error': 'Missing form_fields or base_url'}, status=400)

    # Convert form_fields to JSON if it's a string
    if isinstance(form_fields, str):
        try:
            form_fields = json.loads(form_fields)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON in form_fields'}, status=400)

    # Ensure form_fields is stored as a JSON string with double quotes
    form_fields_str = json.dumps(form_fields)  # Convert the JSON object back to a string

    # Create a new APIQueryTemplate instance
    api_query_template = APIQueryTemplate(form_fields=form_fields_str, base_url=base_url)
    api_query_template.save()

    return Response({'message': 'Template saved successfully!'})


@api_view(['POST'])
def query_openai(request):
    # Extract query data from the POST request
    prompt = request.data.get('prompt')
    if not prompt:
        return Response({"error": "Prompt is required."}, status=400)

    try:
        # Set up the OpenAI API key
        openai.api_key = settings.OPENAI_API_KEY

        # Define the function schema
        functions = [
            { 
                "type": "function",
                "function": {
                    "name": "return_form_fields",
                    "description": "Return the base URL and form fields based on the API documentation.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "base_url": {
                                "type": "string", 
                                "description": "The base URL. MUST BE RETURNED"
                            },
                            "form_fields": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string", "description": "The name of the field"},
                                        "label": {"type": "string", "description": "The label of the field"},
                                        "type": {
                                            "type": "string",
                                            "description": "The type of the field",
                                            "enum": ["text", "number", "select"]
                                        },
                                        "options": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "Options for select type fields"
                                        },
                                        "value": {
                                            "type": "string",
                                            "description": "Default value for the field"
                                        }
                                    },
                                    "required": ["name", "label", "type"],
                                    "additionalProperties": False  # Added this line
                                }
                            }
                        },
                        "required": ["base_url","form_fields"],
                        "additionalProperties": False  # Already present
                    },
                }
            }
        ]
    

        # Set up the messages
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that reads API documentation and generates a base URL form fields for a web form. "
                    "Use the 'return_form_fields' function to output the base URL and form fields, and ensure that both the base URL and form fields "
                    "match the parameters described in the API documentation."
                )
            },
            {"role": "user", "content": prompt}
        ]

        client = OpenAI()
        # Call OpenAI ChatCompletion API with function calling
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-4-0613" if available
            messages=messages,
            tools=functions,
        )

    
        # Check if the assistant made any tool calls
        if response.choices[0].message.tool_calls:
            # Extract the first tool call
            tool_call = response.choices[0].message.tool_calls[0]
            function_call = tool_call.function

            # Check if the function call is 'return_form_fields'
            if function_call.name == "return_form_fields":
                # Parse the arguments
                arguments = json.loads(function_call.arguments)
                form_fields = arguments.get("form_fields", [])
                base_url = arguments.get("base_url", "")
                return Response({"base_url": base_url, "form_fields": form_fields})
            else:
                return Response({"error": "Unexpected function called."}, status=500)
        else:
            return Response({"error": "No function call was made by the assistant."}, status=500)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def submit_query(request):
    try:
        base_url = request.data.get('base_url')
        form_data = request.data.get('form_data')

        if not base_url or not form_data:
            return Response({'error': 'Missing base_url or form_data'}, status=400)

        # Try making the GET request first
        try:
            response = requests.get(base_url, params=form_data)
            response.raise_for_status()  # Check for HTTP errors

        except requests.exceptions.RequestException:
            # If GET request fails, try a POST request
            headers = {'Content-Type': 'application/json'}
            response = requests.post(base_url, json=form_data, headers=headers)
            response.raise_for_status()  # Check for HTTP errors

        # Return the response data to the frontend
        return Response(response.json())

    except requests.exceptions.HTTPError as http_err:
        return Response({'error': f'HTTP error occurred: {http_err}'}, status=response.status_code)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

