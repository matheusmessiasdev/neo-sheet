from jsonschema import validate
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.request import HttpRequest
from rest_framework import status
from .services.schema import base_schema
from .services.schema_validator import schema_validator
from .services.profile_template import PROFILE_BLANK_SCHEMA, PROFILE_TEMPLATE_SCHEMA, SCHEMAS_JSON_SCHEMA
from .serializers import ProfileSerializer
# Create your views here.


@api_view(['GET'])
def blank_sheet(request):
    """
    Base Schema that is returned from the profiles created.
    """

    return Response(base_schema())
    ...


@api_view(['GET'])
def blank_profile(request):
    """
    Base Schema used for creating a Profile. 
    It is not a valid profile, as system_id and display_name must be filled.
    """

    return Response(PROFILE_BLANK_SCHEMA)
    ...


@api_view(['GET'])
def profile_template(request):
    """
    Profile template to auxiliate it's creation.
    """
    return Response(PROFILE_TEMPLATE_SCHEMA, status=status.HTTP_200_OK)
    ...


@api_view(['POST'])
def profiles(request: HttpRequest):
    request_data = request.data
    serializer = ProfileSerializer(data=request_data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=422)
    serializer.save()
    print(schema_validator(request_data.get('schemas')))

    return Response(serializer.data, status=status.HTTP_201_CREATED)
    ...
