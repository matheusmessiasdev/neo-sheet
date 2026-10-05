import pytest
from secrets import randbelow
from unittest.mock import patch
from dice.services.roll_base import (
    roll_dice_formula,
    resolve_operator,
    _resolve_modifier,
    _resolve_formula_extracting,
)


class TestResolveFormulaExtracting:
    """Test the dice formula  parser."""

    def test_simple_formula(self):
        dice, faces, operator, operator_num, mod = _resolve_formula_extracting(
            '2d6')
        assert dice == 2
        assert faces == 6
        assert operator == ''
        assert operator_num is None
        assert mod == ''

    def test_formula_with_modifier(self):
        dice, faces, operator, operator_num, mod = _resolve_formula_extracting(
            '3d8+5')
        assert dice == 3
        assert faces == 8
        assert operator == ''
        assert operator_num is None
        assert mod == '+5'

    def test_formula_with_keep_high(self):
        dice, faces, operator, operator_num, mod = _resolve_formula_extracting(
            '4d6kh3')
        assert dice == 4
        assert faces == 6
        assert operator == 'kh'
        assert operator_num == '3'
        assert mod == ''

    def test_formula_with_keep_low(self):
        dice, faces, operator, operator_num, mod = _resolve_formula_extracting(
            '5d20kl2')
        assert dice == 5
        assert faces == 20
        assert operator == 'kl'
        assert operator_num == '2'
        assert mod == ''

    def test_formula_with_explosive(self):
        dice, faces, operator, operator_num, mod = _resolve_formula_extracting(
            '3d6!')
        assert dice == 3
        assert faces == 6
        assert operator == '!'
        assert operator_num is None
        assert mod == ''


class TestResolveModifier:
    """Test the sum of modifiers."""

    def test_single_modifier(self):
        assert _resolve_modifier('+3') == 3
        assert _resolve_modifier('-5') == -5

    def test_multiple_modifiers(self):
        assert _resolve_modifier('+3-2+5') == 6
        assert _resolve_modifier('-1-2-3') == -6

    def test_no_modifier(self):
        assert _resolve_modifier('') == 0


class TestResolveOperator:
    """Test the roll operators (kh, kl, !)."""

    def test_no_operator(self):
        rolls = [3, 5, 2, 4]
        result = resolve_operator(rolls, '', None, 6)
        assert result == rolls

    def test_keep_high_single(self):
        rolls = [3, 5, 2, 4]
        result = resolve_operator(rolls, 'kh', '1', 6)
        assert result == [5]

    def test_keep_high_multiple(self):
        rolls = [3, 5, 2, 4]
        result = resolve_operator(rolls, 'kh', '2', 6)
        assert result == [5, 4]

    def test_keep_low_single(self):
        rolls = [3, 5, 2, 4]
        result = resolve_operator(rolls, 'kl', '1', 6)
        assert result == [2]

    def test_keep_low_multiple(self):
        rolls = [3, 5, 2, 4]
        result = resolve_operator(rolls, 'kl', '2', 6)
        assert result == [2, 3]

    def test_explosive(self):
        with patch('dice.services.roll_base.randbelow', side_effect=[5, 5, 2]):
            rolls = [6, 6, 3]
            result = resolve_operator(rolls, '!', None, 6)
            assert result == [6, 6, 6, 6, 3]


class TestRollDiceFormula:
    """Test rolling main function."""

    @patch('dice.services.roll_base.randbelow')
    def test_simple_roll(self, mock_randbelow):
        mock_randbelow.side_effect = [3, 5, 2]
        result = roll_dice_formula('3d6')
        assert result['dice_notation'] == '3d6'
        assert result['rolls'] == [4, 6, 3]
        assert result['total'] == 13
        assert result['modifier'] == 0
        assert result['total_with_modifier'] == 13
        assert result['is_critical'] is True
        assert result['is_fumble'] is False

    @patch('dice.services.roll_base.randbelow')
    def test_roll_with_modifier(self, mock_randbelow):
        mock_randbelow.side_effect = [3, 5, 2]
        result = roll_dice_formula('3d6+2')
        assert result['total'] == 13
        assert result['modifier'] == 2
        assert result['total_with_modifier'] == 15

    @patch('dice.services.roll_base.randbelow')
    def test_roll_with_keep_high(self, mock_randbelow):
        mock_randbelow.side_effect = [3, 1, 5, 2]
        result = roll_dice_formula('4d6kh2')
        assert result['rolls'] == [4, 2, 6, 3]
        assert result['rolls_final'] == [6, 4]
        assert result['total'] == 10

    @patch('dice.services.roll_base.randbelow')
    def test_roll_with_keep_low(self, mock_randbelow):
        mock_randbelow.side_effect = [3, 1, 5, 2]
        result = roll_dice_formula('4d6kl2')
        assert result['rolls_final'] == [2, 3]
        assert result['total'] == 5

    @patch('dice.services.roll_base.randbelow')
    def test_roll_with_critical(self, mock_randbelow):
        mock_randbelow.side_effect = [19, 5]
        result = roll_dice_formula('2d20', critical_value=20)
        assert result['is_critical'] is True
        assert result['is_fumble'] is False

    @patch('dice.services.roll_base.randbelow')
    def test_roll_with_fumble(self, mock_randbelow):
        mock_randbelow.side_effect = [0, 0]
        result = roll_dice_formula('2d20')
        assert result['is_fumble'] is True
        assert result['is_critical'] is False

    @patch('dice.services.roll_base.randbelow')
    def test_roll_with_drop(self, mock_randbelow):
        mock_randbelow.side_effect = [3, 1, 5, 2]
        result = roll_dice_formula('4d6', drop=1)
        assert result['rolls_final'] == [4, 2, 6]
        assert result['total'] == 12

    @patch('dice.services.roll_base.randbelow')
    def test_roll_with_explosive(self, mock_randbelow):

        mock_randbelow.side_effect = [5, 5, 2, 5, 4]
        result = roll_dice_formula('3d6!')

        assert len(result['rolls_final']) >= 3
