class Weapon:
    """Representa uma arma em D&D 5e"""
    
    def __init__(self, name: str = "", damage_dice: str = "1d4", damage_type: str = "slashing",
                 properties: list = None, weapon_range: str = "melee", ability: str = "strength",
                 proficient: bool = False, magical_bonus: int = 0, add_ability_to_damage: bool = True):
        self.name = name
        self.damage_dice = damage_dice  # Ex: "1d8", "2d6"
        self.damage_type = damage_type  # slashing, piercing, bludgeoning, etc.
        self.properties = properties or []  # finesse, versatile, two-handed, etc.
        self.weapon_range = weapon_range  # melee, ranged
        self.ability = ability  # strength ou dexterity
        self.proficient = proficient
        self.magical_bonus = magical_bonus  # +1, +2, +3 weapons
        self.add_ability_to_damage = add_ability_to_damage  # Se deve adicionar modificador de habilidade ao dano
        self.equipped = False
    
    def get_attack_bonus(self, character) -> int:
        """Calcula o bônus de ataque"""
        bonus = 0
        
        # Modificador de atributo (suporta todos os atributos)
        valid_abilities = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']
        if self.ability.lower() in valid_abilities:
            bonus += character.stats.get_modifier(self.ability.lower())
        
        # Proficiência (verifica automaticamente se o personagem é proficiente)
        if self.proficient or character.is_proficient_with_weapon(self):
            bonus += character.proficiency_bonus
        
        # Bônus mágico
        bonus += self.magical_bonus
        
        return bonus
    
    def get_damage_bonus(self, character) -> int:
        """Calcula o bônus de dano"""
        bonus = 0
        
        # Modificador de atributo (apenas se add_ability_to_damage for True)
        if self.add_ability_to_damage:
            valid_abilities = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']
            if self.ability.lower() in valid_abilities:
                bonus += character.stats.get_modifier(self.ability.lower())
        
        # Bônus mágico
        bonus += self.magical_bonus
        
        return bonus
    
    def has_property(self, prop: str) -> bool:
        """Verifica se a arma tem uma propriedade específica"""
        return prop.lower() in [p.lower() for p in self.properties]
    
    def to_dict(self) -> dict:
        """Serializa para dicionário"""
        return {
            'name': self.name,
            'damage_dice': self.damage_dice,
            'damage_type': self.damage_type,
            'properties': self.properties,
            'weapon_range': self.weapon_range,
            'ability': self.ability,
            'proficient': self.proficient,
            'magical_bonus': self.magical_bonus,
            'add_ability_to_damage': self.add_ability_to_damage,
            'equipped': self.equipped
        }
    
    @staticmethod
    def from_dict(data: dict):
        """Desserializa de dicionário"""
        weapon = Weapon(
            name=data.get('name', ''),
            damage_dice=data.get('damage_dice', '1d4'),
            damage_type=data.get('damage_type', 'slashing'),
            properties=data.get('properties', []),
            weapon_range=data.get('weapon_range', 'melee'),
            ability=data.get('ability', 'strength'),
            proficient=data.get('proficient', False),
            magical_bonus=data.get('magical_bonus', 0),
            add_ability_to_damage=data.get('add_ability_to_damage', True)  # True por padrão para retrocompatibilidade
        )
        weapon.equipped = data.get('equipped', False)
        return weapon

# Armas pré-definidas — Player's Handbook completo
# ── Armas Simples Corpo-a-Corpo ──────────────────────────────────────────────
COMMON_WEAPONS = {
    'Clava': Weapon('Clava', '1d4', 'bludgeoning', ['light'], 'melee', 'strength'),
    'Adaga': Weapon('Adaga', '1d4', 'piercing', ['finesse', 'light', 'thrown'], 'melee', 'dexterity'),
    'Grande Clava': Weapon('Grande Clava', '1d8', 'bludgeoning', ['two-handed'], 'melee', 'strength'),
    'Machadinha': Weapon('Machadinha', '1d6', 'slashing', ['light', 'thrown'], 'melee', 'strength'),
    'Azagaia': Weapon('Azagaia', '1d6', 'piercing', ['thrown'], 'melee', 'strength'),
    'Martelo Leve': Weapon('Martelo Leve', '1d4', 'bludgeoning', ['light', 'thrown'], 'melee', 'strength'),
    'Maça': Weapon('Maça', '1d6', 'bludgeoning', [], 'melee', 'strength'),
    'Cajado': Weapon('Cajado', '1d6', 'bludgeoning', ['versatile'], 'melee', 'strength'),
    'Foice': Weapon('Foice', '1d4', 'slashing', ['light'], 'melee', 'strength'),
    'Lança': Weapon('Lança', '1d6', 'piercing', ['thrown', 'versatile'], 'melee', 'strength'),
    # ── Armas Simples à Distância ─────────────────────────────────────────────
    'Besta Leve': Weapon('Besta Leve', '1d8', 'piercing', ['ammunition', 'loading', 'two-handed'], 'ranged', 'dexterity'),
    'Dardo': Weapon('Dardo', '1d4', 'piercing', ['finesse', 'thrown'], 'melee', 'dexterity'),
    'Arco Curto': Weapon('Arco Curto', '1d6', 'piercing', ['ammunition', 'two-handed'], 'ranged', 'dexterity'),
    'Funda': Weapon('Funda', '1d4', 'bludgeoning', ['ammunition'], 'ranged', 'dexterity'),
    # ── Armas Marciais Corpo-a-Corpo ──────────────────────────────────────────
    'Machado de Batalha': Weapon('Machado de Batalha', '1d8', 'slashing', ['versatile'], 'melee', 'strength'),
    'Mangual': Weapon('Mangual', '1d8', 'bludgeoning', [], 'melee', 'strength'),
    'Glaive': Weapon('Glaive', '1d10', 'slashing', ['heavy', 'reach', 'two-handed'], 'melee', 'strength'),
    'Machado Grande': Weapon('Machado Grande', '1d12', 'slashing', ['heavy', 'two-handed'], 'melee', 'strength'),
    'Espada Grande': Weapon('Espada Grande', '2d6', 'slashing', ['heavy', 'two-handed'], 'melee', 'strength'),
    'Alabarda': Weapon('Alabarda', '1d10', 'slashing', ['heavy', 'reach', 'two-handed'], 'melee', 'strength'),
    'Lança de Cavalaria': Weapon('Lança de Cavalaria', '1d12', 'piercing', ['reach', 'special'], 'melee', 'strength'),
    'Espada Longa': Weapon('Espada Longa', '1d8', 'slashing', ['versatile'], 'melee', 'strength'),
    'Malho': Weapon('Malho', '2d6', 'bludgeoning', ['heavy', 'two-handed'], 'melee', 'strength'),
    'Estrela da Manhã': Weapon('Estrela da Manhã', '1d8', 'piercing', [], 'melee', 'strength'),
    'Pique': Weapon('Pique', '1d10', 'piercing', ['heavy', 'reach', 'two-handed'], 'melee', 'strength'),
    'Rapieira': Weapon('Rapieira', '1d8', 'piercing', ['finesse'], 'melee', 'dexterity'),
    'Cimitarra': Weapon('Cimitarra', '1d6', 'slashing', ['finesse', 'light'], 'melee', 'dexterity'),
    'Espada Curta': Weapon('Espada Curta', '1d6', 'piercing', ['finesse', 'light'], 'melee', 'dexterity'),
    'Tridente': Weapon('Tridente', '1d6', 'piercing', ['thrown', 'versatile'], 'melee', 'strength'),
    'Picareta de Guerra': Weapon('Picareta de Guerra', '1d8', 'piercing', [], 'melee', 'strength'),
    'Martelo de Guerra': Weapon('Martelo de Guerra', '1d8', 'bludgeoning', ['versatile'], 'melee', 'strength'),
    'Chicote': Weapon('Chicote', '1d4', 'slashing', ['finesse', 'reach'], 'melee', 'dexterity'),
    # ── Armas Marciais à Distância ────────────────────────────────────────────
    'Zarabatana': Weapon('Zarabatana', '1', 'piercing', ['ammunition', 'loading'], 'ranged', 'dexterity'),
    'Besta de Mão': Weapon('Besta de Mão', '1d6', 'piercing', ['ammunition', 'light', 'loading'], 'ranged', 'dexterity'),
    'Besta Pesada': Weapon('Besta Pesada', '1d10', 'piercing', ['ammunition', 'heavy', 'loading', 'two-handed'], 'ranged', 'dexterity'),
    'Arco Longo': Weapon('Arco Longo', '1d8', 'piercing', ['ammunition', 'heavy', 'two-handed'], 'ranged', 'dexterity'),
    'Rede': Weapon('Rede', '0', 'special', ['thrown', 'special'], 'ranged', 'strength'),
}
