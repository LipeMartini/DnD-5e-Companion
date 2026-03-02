"""
Sistema de Fighting Styles para D&D 5e
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class FightingStyle:
    """Representa um estilo de luta"""
    name: str
    description: str
    classes: List[str]  # Classes que podem escolher este estilo
    mechanical_effect: str  # Descrição do efeito mecânico
    
    def __str__(self):
        return self.name


# ========== FIGHTING STYLES ==========

ARCHERY = FightingStyle(
    name='Archery',
    description='Você ganha +2 de bônus nas jogadas de ataque que fizer com armas de ataque à distância.',
    classes=['Fighter', 'Ranger'],
    mechanical_effect='+2 para acertar com armas de alcance'
)

DEFENSE = FightingStyle(
    name='Defense',
    description='Enquanto estiver usando armadura, você ganha +1 de bônus na CA.',
    classes=['Fighter', 'Ranger', 'Paladin'],
    mechanical_effect='+1 CA quando usar armadura'
)

DUELING = FightingStyle(
    name='Dueling',
    description='Quando você empunhar uma arma de ataque corpo a corpo em uma mão e nenhuma outra arma, você ganha +2 de bônus nas jogadas de dano com essa arma.',
    classes=['Fighter', 'Ranger', 'Paladin'],
    mechanical_effect='+2 dano com arma de uma mão (sem outra arma)'
)

GREAT_WEAPON_FIGHTING = FightingStyle(
    name='Great Weapon Fighting',
    description='Quando você rolar 1 ou 2 num dado de dano de um ataque com arma corpo a corpo que você esteja empunhando com duas mãos, você pode rolar o dado novamente e usar a nova rolagem. A arma deve ter a propriedade duas mãos ou versátil para ganhar esse benefício.',
    classes=['Fighter', 'Paladin'],
    mechanical_effect='Rerolar 1s e 2s em dano com armas de duas mãos'
)

PROTECTION = FightingStyle(
    name='Protection',
    description='Quando uma criatura que você possa ver atacar um alvo que esteja a até 1,5 metro de você, você pode usar sua reação para impor desvantagem na jogada de ataque da criatura. Você deve estar empunhando um escudo.',
    classes=['Fighter', 'Paladin'],
    mechanical_effect='Reação: impor desvantagem em ataque (requer escudo)'
)

TWO_WEAPON_FIGHTING = FightingStyle(
    name='Two-Weapon Fighting',
    description='Quando você estiver engajado em uma luta com duas armas, você pode adicionar o seu modificador de habilidade de dano na jogada de dano de seu segundo ataque.',
    classes=['Fighter', 'Ranger'],
    mechanical_effect='Adiciona mod. de habilidade ao dano do ataque bônus'
)


# Dicionário de todos os estilos de luta
ALL_FIGHTING_STYLES: Dict[str, FightingStyle] = {
    'Archery': ARCHERY,
    'Defense': DEFENSE,
    'Dueling': DUELING,
    'Great Weapon Fighting': GREAT_WEAPON_FIGHTING,
    'Protection': PROTECTION,
    'Two-Weapon Fighting': TWO_WEAPON_FIGHTING,
}


def get_available_fighting_styles(class_name: str) -> List[FightingStyle]:
    """
    Retorna os estilos de luta disponíveis para uma classe
    
    Args:
        class_name: Nome da classe
        
    Returns:
        Lista de FightingStyle disponíveis para a classe
    """
    available = []
    for style in ALL_FIGHTING_STYLES.values():
        if class_name in style.classes:
            available.append(style)
    return available


def get_fighting_style(style_name: str) -> Optional[FightingStyle]:
    """
    Retorna um estilo de luta pelo nome
    
    Args:
        style_name: Nome do estilo
        
    Returns:
        FightingStyle ou None se não encontrado
    """
    return ALL_FIGHTING_STYLES.get(style_name)
