from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class CharacterClass:
    name: str
    hit_die: int
    primary_ability: List[str] = field(default_factory=list)
    saving_throw_proficiencies: List[str] = field(default_factory=list)
    skill_proficiencies_count: int = 2
    available_skills: List[str] = field(default_factory=list)
    armor_proficiencies: List[str] = field(default_factory=list)
    weapon_proficiencies: List[str] = field(default_factory=list)
    tool_proficiencies: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'hit_die': self.hit_die,
            'primary_ability': self.primary_ability,
            'saving_throw_proficiencies': self.saving_throw_proficiencies,
            'skill_proficiencies_count': self.skill_proficiencies_count,
            'available_skills': self.available_skills,
            'armor_proficiencies': self.armor_proficiencies,
            'weapon_proficiencies': self.weapon_proficiencies,
            'tool_proficiencies': self.tool_proficiencies,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CharacterClass':
        return cls(**data)

class ClassDatabase:
    """Banco de dados de classes disponíveis"""
    
    @staticmethod
    def get_all_classes() -> Dict[str, CharacterClass]:
        return {
            'Barbarian': CharacterClass(
                name='Barbarian',
                hit_die=12,
                primary_ability=['strength'],
                saving_throw_proficiencies=['strength', 'constitution'],
                skill_proficiencies_count=2,
                available_skills=['Animal Handling', 'Athletics', 'Intimidation', 'Nature', 'Perception', 'Survival'],
                armor_proficiencies=['Light armor', 'Medium armor', 'Shields'],
                weapon_proficiencies=['Simple weapons', 'Martial weapons'],
            ),
            'Bard': CharacterClass(
                name='Bard',
                hit_die=8,
                primary_ability=['charisma'],
                saving_throw_proficiencies=['dexterity', 'charisma'],
                skill_proficiencies_count=3,
                available_skills=['Acrobatics', 'Animal Handling', 'Arcana', 'Athletics', 'Deception', 
                                'History', 'Insight', 'Intimidation', 'Investigation', 'Medicine', 
                                'Nature', 'Perception', 'Performance', 'Persuasion', 'Religion', 
                                'Sleight of Hand', 'Stealth', 'Survival'],
                armor_proficiencies=['Light armor'],
                weapon_proficiencies=['Simple weapons', 'Hand crossbows', 'Longswords', 'Rapiers', 'Shortswords'],
                tool_proficiencies=['Three musical instruments'],
            ),
            'Cleric': CharacterClass(
                name='Cleric',
                hit_die=8,
                primary_ability=['wisdom'],
                saving_throw_proficiencies=['wisdom', 'charisma'],
                skill_proficiencies_count=2,
                available_skills=['History', 'Insight', 'Medicine', 'Persuasion', 'Religion'],
                armor_proficiencies=['Light armor', 'Medium armor', 'Shields'],
                weapon_proficiencies=['Simple weapons'],
            ),
            'Druid': CharacterClass(
                name='Druid',
                hit_die=8,
                primary_ability=['wisdom'],
                saving_throw_proficiencies=['intelligence', 'wisdom'],
                skill_proficiencies_count=2,
                available_skills=['Arcana', 'Animal Handling', 'Insight', 'Medicine', 'Nature', 'Perception', 'Religion', 'Survival'],
                armor_proficiencies=['Light armor', 'Medium armor', 'Shields (non-metal)'],
                weapon_proficiencies=['Clubs', 'Daggers', 'Darts', 'Javelins', 'Maces', 'Quarterstaffs', 'Scimitars', 'Sickles', 'Slings', 'Spears'],
                tool_proficiencies=['Herbalism kit'],
            ),
            'Fighter': CharacterClass(
                name='Fighter',
                hit_die=10,
                primary_ability=['strength', 'dexterity'],
                saving_throw_proficiencies=['strength', 'constitution'],
                skill_proficiencies_count=2,
                available_skills=['Acrobatics', 'Animal Handling', 'Athletics', 'History', 'Insight', 'Intimidation', 'Perception', 'Survival'],
                armor_proficiencies=['All armor', 'Shields'],
                weapon_proficiencies=['Simple weapons', 'Martial weapons'],
            ),
            'Monk': CharacterClass(
                name='Monk',
                hit_die=8,
                primary_ability=['dexterity', 'wisdom'],
                saving_throw_proficiencies=['strength', 'dexterity'],
                skill_proficiencies_count=2,
                available_skills=['Acrobatics', 'Athletics', 'History', 'Insight', 'Religion', 'Stealth'],
                weapon_proficiencies=['Simple weapons', 'Shortswords'],
                tool_proficiencies=['One type of artisan tools or musical instrument'],
            ),
            'Paladin': CharacterClass(
                name='Paladin',
                hit_die=10,
                primary_ability=['strength', 'charisma'],
                saving_throw_proficiencies=['wisdom', 'charisma'],
                skill_proficiencies_count=2,
                available_skills=['Athletics', 'Insight', 'Intimidation', 'Medicine', 'Persuasion', 'Religion'],
                armor_proficiencies=['All armor', 'Shields'],
                weapon_proficiencies=['Simple weapons', 'Martial weapons'],
            ),
            'Ranger': CharacterClass(
                name='Ranger',
                hit_die=10,
                primary_ability=['dexterity', 'wisdom'],
                saving_throw_proficiencies=['strength', 'dexterity'],
                skill_proficiencies_count=3,
                available_skills=['Animal Handling', 'Athletics', 'Insight', 'Investigation', 'Nature', 'Perception', 'Stealth', 'Survival'],
                armor_proficiencies=['Light armor', 'Medium armor', 'Shields'],
                weapon_proficiencies=['Simple weapons', 'Martial weapons'],
            ),
            'Rogue': CharacterClass(
                name='Rogue',
                hit_die=8,
                primary_ability=['dexterity'],
                saving_throw_proficiencies=['dexterity', 'intelligence'],
                skill_proficiencies_count=4,
                available_skills=['Acrobatics', 'Athletics', 'Deception', 'Insight', 'Intimidation', 'Investigation', 'Perception', 'Performance', 'Persuasion', 'Sleight of Hand', 'Stealth'],
                armor_proficiencies=['Light armor'],
                weapon_proficiencies=['Simple weapons', 'Hand crossbows', 'Longswords', 'Rapiers', 'Shortswords'],
                tool_proficiencies=['Thieves tools'],
            ),
            'Sorcerer': CharacterClass(
                name='Sorcerer',
                hit_die=6,
                primary_ability=['charisma'],
                saving_throw_proficiencies=['constitution', 'charisma'],
                skill_proficiencies_count=2,
                available_skills=['Arcana', 'Deception', 'Insight', 'Intimidation', 'Persuasion', 'Religion'],
                weapon_proficiencies=['Daggers', 'Darts', 'Slings', 'Quarterstaffs', 'Light crossbows'],
            ),
            'Warlock': CharacterClass(
                name='Warlock',
                hit_die=8,
                primary_ability=['charisma'],
                saving_throw_proficiencies=['wisdom', 'charisma'],
                skill_proficiencies_count=2,
                available_skills=['Arcana', 'Deception', 'History', 'Intimidation', 'Investigation', 'Nature', 'Religion'],
                armor_proficiencies=['Light armor'],
                weapon_proficiencies=['Simple weapons'],
            ),
            'Wizard': CharacterClass(
                name='Wizard',
                hit_die=6,
                primary_ability=['intelligence'],
                saving_throw_proficiencies=['intelligence', 'wisdom'],
                skill_proficiencies_count=2,
                available_skills=['Arcana', 'History', 'Insight', 'Investigation', 'Medicine', 'Religion'],
                weapon_proficiencies=['Daggers', 'Darts', 'Slings', 'Quarterstaffs', 'Light crossbows'],
            ),
        }
    
    @staticmethod
    def get_class(class_name: str) -> CharacterClass:
        classes = ClassDatabase.get_all_classes()
        return classes.get(class_name, classes['Fighter'])
