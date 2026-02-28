import random
from typing import List, Tuple

class DiceRoller:
    @staticmethod
    def roll(dice_notation: str) -> Tuple[int, List[int]]:
        """
        Rola dados usando notação padrão (ex: '2d6+3', '1d20', '4d6kh3')
        Retorna: (total, lista de resultados individuais)
        """
        dice_notation = dice_notation.lower().replace(" ", "")
        
        modifier = 0
        if '+' in dice_notation:
            dice_part, mod_part = dice_notation.split('+')
            modifier = int(mod_part)
        elif '-' in dice_notation:
            dice_part, mod_part = dice_notation.split('-')
            modifier = -int(mod_part)
        else:
            dice_part = dice_notation
        
        keep_highest = None
        if 'kh' in dice_part:
            dice_part, keep_part = dice_part.split('kh')
            keep_highest = int(keep_part)
        
        num_dice, die_size = map(int, dice_part.split('d'))
        
        rolls = [random.randint(1, die_size) for _ in range(num_dice)]
        
        if keep_highest:
            sorted_rolls = sorted(rolls, reverse=True)
            kept_rolls = sorted_rolls[:keep_highest]
            total = sum(kept_rolls) + modifier
            return total, rolls
        
        total = sum(rolls) + modifier
        return total, rolls
    
    @staticmethod
    def roll_ability_score() -> Tuple[int, List[int]]:
        """
        Rola 4d6, mantém os 3 maiores (método padrão para atributos)
        """
        return DiceRoller.roll('4d6kh3')
    
    @staticmethod
    def roll_d20(modifier: int = 0) -> Tuple[int, int]:
        """
        Rola 1d20 com modificador
        Retorna: (total, valor do d20)
        """
        d20_roll = random.randint(1, 20)
        return d20_roll + modifier, d20_roll
