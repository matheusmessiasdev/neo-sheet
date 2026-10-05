from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from secrets import randbelow
from .serializers import RollDiceSerializer, RollDiceResponseSerializer
from .services.roll_base import roll_dice_formula
from drf_spectacular.utils import extend_schema
import re
from django_ratelimit.decorators import ratelimit
from django.conf import settings
# Create your views here.


@extend_schema(
    tags=['Dice'],
    summary='Roll Dice',
    auth=[],
    description=(
        'Rolls dice based on XdY notation (ex: 2d6, 3d8+5).\n'
        'Supports operators:\n'
        '- `kh` (keep highest): 4d6kh3\n'
        '- `kl` (keep lowest): 4d6kl2\n'
        '- `!` (explosive): 3d6!\n'
    ),
    request=RollDiceSerializer,
    responses={200: RollDiceResponseSerializer},
)
@api_view(['POST'])
@ratelimit(key='ip', rate=settings.RATELIMITS['dice_roll'], method='POST', block=True)
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
