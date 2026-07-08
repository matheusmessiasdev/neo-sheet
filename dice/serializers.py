from rest_framework import serializers
import re


def validate_dice_notation(formula: str):
    """
    Validates the string to ensure it's a valid xdY dice notation.
    It accepts 3d6, 1d20, 4d6+4, 2d8+3+2+5.
    """
    pattern = r'^(\d+)?d(\d+)([a-z!]*)?(\d+)?(([+-]\d+)*)$'
    re_match = re.fullmatch(pattern, formula.replace(" ", ""))

    VALID_OPERATORS = {'kh', '!', 'kl', ''}

    if not re_match:
        raise serializers.ValidationError(
            f"Invalid Formula: {formula}. Use the XdY+modifier format. Ex: 3d6+5"
        )
    dice_amount = int(re_match.group(1))
    faces = int(re_match.group(2))
    operator = re_match.group(3)

    if dice_amount > 999:
        raise serializers.ValidationError(
            f"999 dice max per roll. Received: {dice_amount}")

    if faces > 100_000:
        raise serializers.ValidationError(
            f"d{faces} is a invalid die."
        )
    if operator not in VALID_OPERATORS:
        raise serializers.ValidationError(
            f"Unknown Operator. Use the specified formats kh, kl, !"
        )


class RollDiceSerializer(serializers.Serializer):
    formula = serializers.CharField(
        default="1d20", max_length=50, validators=[validate_dice_notation,])
    critical_value = serializers.IntegerField(
        min_value=1, max_value=100, allow_null=True, default=None)
    critical_mult = serializers.IntegerField(
        min_value=1, max_value=100, allow_null=True, default=1)
    drop = serializers.IntegerField(min_value=0,
                                    max_value=999, allow_null=True, default=0)


if __name__ == '__main__':
    ...
