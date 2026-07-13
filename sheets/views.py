from .services.profile_template import PROFILE_BLANK_SCHEMA, PROFILE_TEMPLATE_SCHEMA, SCHEMAS_JSON_SCHEMA
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http.request import HttpRequest
from .services.schema import base_schema
from .services.sheet_from_profile import configure_sheet_from_profile
from .models import ProfileModel
from .serializers import ProfileSerializer, ProfileListSerializer
from django.shortcuts import render
from jsonschema import validate
from django.shortcuts import get_object_or_404
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


class ProfilesViewSet(viewsets.ModelViewSet):
    """
    List of system profiles avaliable.
    """
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = ProfileModel.objects.all().only("system_id", "display_name")
    lookup_field = "system_id"

    def get_serializer_class(self):
        if self.request.method == "POST" or self.request.method == "PATCH":
            return ProfileSerializer
        else:
            return ProfileListSerializer

    def list(self, request):
        queryset = ProfileModel.objects.all().only("system_id", "display_name")
        serializer = ProfileListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, system_id):
        profile = ProfileModel.objects.get(system_id=system_id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


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
