import re
from secrets import randbelow
from itertools import chain


def roll_dice_formula(formula: str,
                      critical_value: int | None = 20,
                      critical_mult: int | None = 1,
                      drop: int = 0):

    dice, faces, operator, \
        operator_num, modifiers = _resolve_formula_extracting(formula=formula)

    modifier_total = _resolve_modifier(modifiers)
    rolls = [randbelow(faces) + 1 for _ in range(dice)]
    resolved_operator = resolve_operator(rolls, operator, operator_num, faces)
    fumble_flag = max(rolls) <= 1
    if critical_value is None or critical_value > faces:
        critical_value = faces
    crit_flag = max(rolls) >= critical_value
    resolved_operator = resolved_operator[:-
                                          drop] if drop > 0 else resolved_operator
    rolls_total = sum(resolved_operator)

    return {"dice_notation":  formula,
            "rolls": rolls,
            "rolls_final": resolved_operator,
            "is_critical": crit_flag,
            "is_fumble": fumble_flag,
            "total": rolls_total,
            "modifier": modifier_total,
            "total_with_modifier": sum((rolls_total, modifier_total)),
            "context": {
                "dice": dice,
                "faces": faces,
                "critical_value": critical_value,
                "critical_mult": critical_mult,
                "dropped_dice": drop,
            },
            }


def resolve_operator(rolls: list[int], operator: str, operator_num: str, face: int) -> list[int]:
    FIRST_ELEMENT = 0

    if operator_num:
        int_operator_num = int(operator_num)

    def _handle_keep_drop(ascending: bool) -> list[int]:
        sorted_rolls = sorted(rolls, reverse=ascending)
        if not operator_num or operator_num == '1':
            return [sorted_rolls[FIRST_ELEMENT]]
        elif int(operator_num) > 1:
            return sorted_rolls[FIRST_ELEMENT:int_operator_num]
        else:
            return rolls

    match operator:
        case 'kh':
            return _handle_keep_drop(True)
            # TODO use the operator num to determine how many will be kept
        case 'kl':
            return _handle_keep_drop(False)
        case '!':
            explosive_rolls = [
                randbelow(face) + 1 for value in rolls if value == face]
            return list(chain(explosive_rolls, rolls))
        case '':
            return rolls
        case _:
            return list()


def _resolve_modifier(modifier: str):
    values = tuple(map(int, re.findall(r'([+-]\d*)', modifier)))
    return sum(values)


def _resolve_formula_extracting(formula: str) -> tuple[int, int,
                                                       str, str, str]:
    pattern = r'^(\d+)?d(\d+)([a-z!]*)?(\d+)?(([+-]\d+)*)$'
    re_match = re.fullmatch(pattern, formula)
    if not re_match:
        print('Formula Invalida')
        return 'Invalid Formula.'  # type: ignore

    _dice = int(re_match.group(1)) if re_match.group(1) is not None else 1
    _faces, _operator, _operator_num, _modifiers = int(re_match.group(
        2)), re_match.group(3), re_match.group(4), re_match.group(5)
    return _dice, _faces, _operator, _operator_num, _modifiers


if __name__ == '__main__':
    print(roll_dice_formula('2d20'))
    ...
