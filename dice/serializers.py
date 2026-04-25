from rest_framework import serializers
import re


def validate_dice_notation(formula: str):
    """
    Validates the string to ensure it's a valid xdY dice notation. 
    It accepts 3d6, 1d20, 4d6+4, 2d8+3+2+5.
    """
    pattern = r'^(\d+)d(\d+)(([+-]\d+)*)$'
    match = re.fullmatch(pattern, formula.replace(" ", ""))

    if not match:
        raise serializers.ValidationError(
            f"Invalid Formula: {formula}. Use the XdY+modifier format. Ex: 3d6+5 "
        )

    dice_amount = int(match.group(1))
    faces = int(match.group(2))

    if dice_amount > 20:
        raise serializers.ValidationError(
            f"20 dice max per roll. Received: {dice_amount}")

    if faces not in {4, 6, 8, 10, 12, 20, 100}:
        raise serializers.ValidationError(
            f"d{faces} is a invalid die. use d4, d6, d8, d10, d12, d20, d100."
        )


class RollDiceSerializer(serializers.Serializer):
    formula = serializers.CharField(
        default="1d20", max_length=50, validators=[validate_dice_notation,])


if __name__ == '__main__':
    aa = "2d6+3+6+5-6+3"
    validate_dice_notation("2d6+3+6+5-6+3")
    pattern = r'^(\d+)d(\d+)(([+-]\d+)*)$'
    match = re.fullmatch(pattern, aa.replace(" ", ""))
    if not match:
        print('Vish')
    print(sum([+3, 4, 5, -7]))
