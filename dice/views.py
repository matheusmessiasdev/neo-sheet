from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from secrets import randbelow
# Create your views here.


# xdY
@api_view(['POST'])
def roll_base_dice(request):
    if request.method == 'POST':

        return Response({"message": "Hello, world!", })
