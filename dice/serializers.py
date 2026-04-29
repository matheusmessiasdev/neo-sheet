from rest_framework import serializers
import re


def validate_dice_notation(formula: str):
    """
    Validates the string to ensure it's a valid xdY dice notation.
    It accepts 3d6, 1d20, 4d6+4, 2d8+3+2+5.
    """
    pattern = r'^(\d+)d(\d+)([a-z!]*)?(\d+)?(([+-]\d+)*)$'
    re_match = re.fullmatch(pattern, formula.replace(" ", ""))

    if not re_match:
        raise serializers.ValidationError(
            f"Invalid Formula: {formula}. Use the XdY+modifier format. Ex: 3d6+5"
        )
    operator_set = {'kh', '!', 'kl'}
    dice_amount = int(re_match.group(1))
    faces = int(re_match.group(2))
    operator_value = re_match.group(2)

    if dice_amount > 20:
        raise serializers.ValidationError(
            f"20 dice max per roll. Received: {dice_amount}")

    if faces not in {4, 6, 8, 10, 12, 20, 100}:
        raise serializers.ValidationError(
            f"d{faces} is a invalid die. use d4, d6, d8, d10, d12, d20, d100."
        )
    if operator_value is not None and operator_value in operator_set:
        raise serializers.ValidationError(
            f"Unknown Operator. Use the specified formats kh, kl, !"
        )


class RollDiceSerializer(serializers.Serializer):
    formula = serializers.CharField(
        default="1d20", max_length=50, validators=[validate_dice_notation,])


if __name__ == '__main__':
    ...
