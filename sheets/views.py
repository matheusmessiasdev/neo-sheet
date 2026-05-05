from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.schema import base_schema
from .services.profile_template import PROFILE_TEMPLATE_SCHEMA
# Create your views here.


@api_view(['GET'])
def blank_sheet(request):

    return Response(base_schema())
    ...


@api_view(['GET'])
def profile_template(request):

    return Response(PROFILE_TEMPLATE_SCHEMA)
    ...
