from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services.schema import base_schema
from .services.profile_template import PROFILE_TEMPLATE_SCHEMA
from .serializers import ProfileTemplateSerializer
# Create your views here.


@api_view(['GET'])
def blank_sheet(request):

    return Response(base_schema())
    ...


@api_view(['GET'])
def profile_template(request):

    return Response(PROFILE_TEMPLATE_SCHEMA, status=status.HTTP_200_OK)
    ...


@api_view(['POST'])
def profiles(request):
    serializer = ProfileTemplateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=422)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    ...
