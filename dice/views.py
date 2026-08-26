from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from secrets import randbelow
from .serializers import RollDiceSerializer
from .services.roll_base import roll_dice_formula
import re
# Create your views here.


# xdY
@api_view(['POST'])
def roll_base_dice(request):
    """
    Rolls dices based of the dice notation (XdY). 
    Compatible with Operators (kh, kl, !).
    """

    serializer = RollDiceSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=422)

    data = serializer.validated_data
    formula = data['formula']
    critical_value = data['critical_value']
    print(data['critical_value'])
    critical_mult = data['critical_mult']
    drop = data['drop']

    return Response(roll_dice_formula(formula, critical_value, critical_mult, drop))
