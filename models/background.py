from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Background:
    name: str
    skill_proficiencies: List[str]
    tool_proficiencies: List[str]
    languages: List[str]
    equipment: List[str]
    features: List[str]
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'skill_proficiencies': self.skill_proficiencies,
            'tool_proficiencies': self.tool_proficiencies,
            'languages': self.languages,
            'equipment': self.equipment,
            'features': self.features,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Background':
        return cls(**data)
    
class BackgroundDatabase:
    """Banco de dados de antecedentes disponíveis"""
    
    @staticmethod
    def get_all_backgrounds() -> Dict[str, Background]:
        return {
            'Acolyte': Background(
                name='Acolyte',
                skill_proficiencies=['Insight', 'Religion'],
                tool_proficiencies=[],
                languages=['Two extra language'],
                equipment=['Holy symbol', 'Prayer book', 'Common clothes', 'Pouch containing 15 gp'],
                features=['Shelter of the Faithful']
            ),
            'Charlatan': Background(
                name='Charlatan',
                skill_proficiencies=['Deception', 'Sleight of Hand'],
                tool_proficiencies=['Disguise Kit', 'Forgery Kit'],
                languages=[],
                equipment=['Fine clothes', 'Disguise kit', 'Tool of the con of your choice', 'Pouch containing 15 gp'],
                features=['False Identity']
            ),
            'Criminal': Background(
                name='Criminal',
                skill_proficiencies=['Deception', 'Stealth'],
                tool_proficiencies=['Thieves\' Tools'],
                languages=[],
                equipment=['Dark common clothes with hood', 'Crowbar', 'Pocket knife', 'Pouch containing 15 gp'],
                features=['Criminal Contact']
            ),
            'Entertainer': Background(
                name='Entertainer',
                skill_proficiencies=['Acrobatics', 'Performance'],
                tool_proficiencies=['Disguise Kit', 'Musical Instrument'],
                languages=[],
                equipment=['Entertainer\'s clothes', 'Musical instrument', 'The favor of an admirer (love letter, lock of hair, or trinket)', 'Pouch containing 15 gp'],
                features=['By Popular Demand']
            ),
            'Folk Hero': Background(
                name='Folk Hero',
                skill_proficiencies=['Animal Handling', 'Survival'],
                tool_proficiencies=['Land vehicles'],
                languages=[],
                equipment=['A set of artisan\'s tools (one of your choice)', 'Shovel', 'Iron pot', 'Common clothes', 'Pouch containing 10 gp'],
                features=['Rustic Hospitality']
            ),
            'Guild Artisan': Background(
                name='Guild Artisan',
                skill_proficiencies=['Insight', 'Persuasion'],
                tool_proficiencies=['Artisan\'s tools'],
                languages=[],
                equipment=['Artisan\'s tools', 'Guild membership', 'Traveler\'s clothes', 'Pouch containing 15 gp'],
                features=['Guild Membership']
            ),
            'Hermit': Background(
                name='Hermit',
                skill_proficiencies=['Medicine', 'Religion'],
                tool_proficiencies=['Herbalism Kit'],
                languages=[],
                equipment=['Scroll case', 'Winter blanket', 'Common clothes', 'Herbalism kit', '5 gp'],
                features=['Discovery']
            ),
            'Noble': Background(
                name='Noble',
                skill_proficiencies=['History', 'Persuasion'],
                tool_proficiencies=[],
                languages=['One extra language'],
                equipment=['Fine clothes', 'Signet ring', 'Scroll of pedigree', 'Purse containing 25 gp'],
                features=['Position of Privilege']
            ),
            'Outlander': Background(
                name='Outlander',
                skill_proficiencies=['Athletics', 'Survival'],
                tool_proficiencies=['One type of musical instrument'],
                languages=['One extra language'],
                equipment=['Staff', 'Hunter\'s trap', 'Trophy from an animal you killed', 'Traveler\'s clothes', 'Pouch containing 10 gp'],
                features=['Wanderer']
            ),
            'Sage': Background(
                name='Sage',
                skill_proficiencies=['Arcana', 'History'],
                tool_proficiencies=[],
                languages=['Two extra languages'],
                equipment=['Quill', 'Book of lore', 'Common clothes', 'Pouch containing 10 gp'],
                features=['Researcher']
            ),
            'Sailor': Background(
                name='Sailor',
                skill_proficiencies=['Athletics', 'Perception'],
                tool_proficiencies=['Navigator\'s tools', 'Water vehicles'],
                languages=[],
                equipment=['Belaying pin', '50 feet of silk rope', 'Lucky charm', 'Common clothes', 'Pouch containing 10 gp'],
                features=['Ship\'s Passage']
            ),
            'Soldier': Background(
                name='Soldier',
                skill_proficiencies=['Athletics', 'Intimidation'],
                tool_proficiencies=['Land vehicles'],
                languages=[],
                equipment=['Uniform of your unit', 'A set of dice or a deck of cards', 'Common clothes', 'Pouch containing 10 gp'],
                features=['Military Rank']
            ),
            'Urchin': Background(
                name='Urchin',
                skill_proficiencies=['Sleight of Hand', 'Stealth'],
                tool_proficiencies=['Disguise Kit', 'Thieves\' Tools'],
                languages=[],
                equipment=['Small knife', 'Map of hometown', 'Pet mouse', 'Token of parents', 'Common clothes', 'Pouch containing 10 gp'],
                features=['City Secrets']
            )
        }
    
    @staticmethod
    def get_background(background_name: str) -> Background:
        backgrounds = BackgroundDatabase.get_all_backgrounds()
        return backgrounds.get(background_name, backgrounds['Acolyte'])