import re
from secrets import randbelow


def roll_dice_formula(formula: str,
                      critical_value: int | None = None,
                      critical_mult: int | None = None):
    # 12d12+3+2-5+6+4
    pattern = r'^(\d+)?d(\d+)([a-z!]*)?(\d+)?(([+-]\d+)*)$'
    re_match = re.fullmatch(pattern, formula)
    if not re_match:
        print('Invalid Formula')
        return 'Invalid Formula.'

    dice = int(re_match.group(1)) if re_match.group(1) is not None else 1
    faces, operator, operator_num, modifiers = int(re_match.group(
        2)), re_match.group(3), re_match.group(4), re_match.group(5)

    modifier_values = re.findall(r'([+-]\d+)', modifiers)

    total_modifier = sum(int(item) for item in modifier_values)

    rolls = [randbelow(faces) + 1 for _ in range(dice)]

    print('Dice value: ', dice)
    print('Die Face: ', faces)
    print('Operator: ', operator)
    print('Operator Num (opc): ', operator_num)
    print('Modifiers: ', modifiers)
    print()
    print('Rolagens: ', rolls)
    print(f'Operator {operator} Resolve:',
          resolve_operator(rolls, operator, operator_num, faces))
    print('Modifier: ', _resolve_modifier(modifiers))
    # Fazer todas as variações de dados que der


def resolve_operator(rolls: list[int], operator: str, operator_num: str, face: int) -> int | None | list[int]:
    operator_num_flag = False
    first_value_index = 0
    if not operator:
        return None
    if operator_num:
        operator_num_flag = True
        int_operator_num = int(operator_num)
        total_amount = int_operator_num if int_operator_num < len(
            rolls) else int_operator_num

    def _handle_keep_drop(ascending: bool):
        sorted_rolls = sorted(rolls, reverse=ascending)
        if not operator_num_flag or operator_num == '1':
            return sorted_rolls[first_value_index]

        elif int(operator_num) > 1:
            return sorted_rolls[first_value_index:total_amount]

    match operator:
        case 'kh':
            return _handle_keep_drop(True)
            # TODO use the operator num to determine how many will be kept
        case 'kl':
            return _handle_keep_drop(False)
        case '!':
            explosive_rolls = [
                randbelow(face) + 1 for value in rolls if value == face]
            return explosive_rolls


def _resolve_modifier(modifier: str):
    values = list(map(int, re.findall(r'([+-]\d*)', modifier)))
    return sum(values)
    ...


if __name__ == '__main__':
    roll_dice_formula('12d6kh1+3+5-43+6-9')
