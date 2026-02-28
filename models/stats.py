from dataclasses import dataclass
from typing import Dict

@dataclass
class Stats:
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    
    @staticmethod
    def calculate_modifier(score: int) -> int:
        """Calcula o modificador baseado no valor do atributo"""
        return (score - 10) // 2
    
    def get_modifier(self, stat_name: str) -> int:
        """Retorna o modificador de um atributo específico"""
        score = getattr(self, stat_name.lower())
        return self.calculate_modifier(score)
    
    def get_all_modifiers(self) -> Dict[str, int]:
        """Retorna todos os modificadores em um dicionário"""
        return {
            'strength': self.calculate_modifier(self.strength),
            'dexterity': self.calculate_modifier(self.dexterity),
            'constitution': self.calculate_modifier(self.constitution),
            'intelligence': self.calculate_modifier(self.intelligence),
            'wisdom': self.calculate_modifier(self.wisdom),
            'charisma': self.calculate_modifier(self.charisma),
        }
    
    def apply_racial_bonuses(self, bonuses: Dict[str, int]):
        """Aplica bônus raciais aos atributos"""
        for stat, bonus in bonuses.items():
            current_value = getattr(self, stat.lower())
            setattr(self, stat.lower(), current_value + bonus)
    
    def to_dict(self) -> Dict[str, int]:
        """Converte stats para dicionário"""
        return {
            'strength': self.strength,
            'dexterity': self.dexterity,
            'constitution': self.constitution,
            'intelligence': self.intelligence,
            'wisdom': self.wisdom,
            'charisma': self.charisma,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> 'Stats':
        """Cria Stats a partir de um dicionário"""
        return cls(**data)
