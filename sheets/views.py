from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.schema import base_schema
# Create your views here.


@api_view(['GET'])
def blank_sheet(request):

    return Response(base_schema())
    ...
