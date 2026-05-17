from .services.profile_template import PROFILE_BLANK_SCHEMA, PROFILE_TEMPLATE_SCHEMA, SCHEMAS_JSON_SCHEMA
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http.request import HttpRequest
from .services.schema import base_schema
from .services.sheet_from_profile import configure_sheet_from_profile
from .models import ProfileModel
from .serializers import ProfileSerializer, ProfilesSerializer
from django.shortcuts import render
from jsonschema import validate
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


class ProfilesList(generics.ListAPIView):
    """
    List of profiles avaliable.
    """

    def get_queryset(self):
        return ProfileModel.objects.all().only('system_id', 'display_name')
    serializer_class = ProfilesSerializer
    ...


@api_view(['GET'])
def show_profile(request: HttpRequest, system_id):
    profile = ProfileModel.objects.get(system_id=system_id)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)
    ...


@api_view(['GET'])
def sheet_from_profile(request: HttpRequest, system_id):
    profile = ProfileModel.objects.get(system_id=system_id)
    serializer = ProfileSerializer(profile)
    return Response(configure_sheet_from_profile(profile))
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

    return Response(serializer.data, status=status.HTTP_201_CREATED)
    ...
