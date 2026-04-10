"""
Subclasses (Arquétipos) para D&D 5e
Cada classe tem suas próprias subclasses que são escolhidas em níveis específicos
"""

from dataclasses import dataclass
from typing import List, Dict, Optional

from .app_settings import AppSettings

SOURCE_CORE = "phb"
SOURCE_TASHAS = "tashas"
SOURCE_XANATHARS = "xanathars"

SOURCE_LABELS = {
    SOURCE_CORE: "Player's Handbook",
    SOURCE_TASHAS: "Tasha's Cauldron of Everything",
    SOURCE_XANATHARS: "Xanathar's Guide to Everything",
}

OPTIONAL_SOURCE_FLAGS = {
    SOURCE_TASHAS: "tashas_spells",
    SOURCE_XANATHARS: "xanathars_spells",
}

@dataclass
class SubclassFeature:
    """Representa uma feature específica de uma subclasse"""
    name: str
    level: int
    description: str
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'level': self.level,
            'description': self.description
        }
    
    @staticmethod
    def from_dict(data: dict):
        return SubclassFeature(
            name=data['name'],
            level=data['level'],
            description=data['description']
        )

@dataclass
class Subclass:
    """Representa uma subclasse/arquétipo de personagem"""
    name: str
    class_name: str  # Classe pai (Barbarian, Fighter, etc.)
    description: str
    features: List[SubclassFeature]
    selection_level: int = 3  # Nível em que a subclasse é escolhida
    source: str = SOURCE_CORE
    
    def get_features_at_level(self, level: int) -> List[SubclassFeature]:
        """Retorna features disponíveis em um nível específico"""
        return [f for f in self.features if f.level == level]
    
    def get_all_features_up_to_level(self, level: int) -> List[SubclassFeature]:
        """Retorna todas as features até um nível específico"""
        return [f for f in self.features if f.level <= level]
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'class_name': self.class_name,
            'description': self.description,
            'features': [f.to_dict() for f in self.features],
            'selection_level': self.selection_level,
            'source': self.source,
        }
    
    @staticmethod
    def from_dict(data: dict):
        return Subclass(
            name=data['name'],
            class_name=data['class_name'],
            description=data['description'],
            features=[SubclassFeature.from_dict(f) for f in data['features']],
            selection_level=data.get('selection_level', 3),
            source=data.get('source', SOURCE_CORE)
        )


# ========== BARBARIAN SUBCLASSES ==========

BERSERKER = Subclass(
    name="Path of the Berserker",
    class_name="Barbarian",
    description="For some barbarians, rage is a means to an end — that end being violence. The Path of the Berserker is a path of untrammeled fury, slick with blood.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Frenzy",
            level=3,
            description="You can go into a frenzy when you rage. If you do so, for the duration of your rage you can make a single melee weapon attack as a bonus action on each of your turns after this one. When your rage ends, you suffer one level of exhaustion."
        ),
        SubclassFeature(
            name="Mindless Rage",
            level=6,
            description="You can't be charmed or frightened while raging. If you are charmed or frightened when you enter your rage, the effect is suspended for the duration of the rage."
        ),
        SubclassFeature(
            name="Intimidating Presence",
            level=10,
            description="You can use your action to frighten someone with your menacing presence. When you do so, choose one creature that you can see within 30 feet of you. If the creature can see or hear you, it must succeed on a Wisdom saving throw (DC equal to 8 + your proficiency bonus + your Charisma modifier) or be frightened of you until the end of your next turn. On subsequent turns, you can use your action to extend the duration of this effect on the frightened creature until the end of your next turn. This effect ends if the creature ends its turn out of line of sight or more than 60 feet away from you. If the creature succeeds on its saving throw, you can't use this feature on that creature again for 24 hours."
        ),
        SubclassFeature(
            name="Retaliation",
            level=14,
            description="When you take damage from a creature that is within 5 feet of you, you can use your reaction to make a melee weapon attack against that creature."
        )
    ]
)

SCHOOL_OF_WAR_MAGIC = Subclass(
    name="School of War Magic",
    class_name="Wizard",
    description="War Magic wizards blend battlefield tactics with arcane wards, deflecting blows while unleashing precise counterstrikes.",
    selection_level=2,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Arcane Deflection",
            level=2,
            description="When you are hit by an attack or fail a saving throw, you can use your reaction to gain +2 AC or +4 to the saving throw, but you can cast only cantrips until the end of your next turn."
        ),
        SubclassFeature(
            name="Tactical Wit",
            level=2,
            description="You add your Intelligence modifier to initiative rolls, reflecting your battlefield foresight."
        ),
        SubclassFeature(
            name="Power Surge",
            level=6,
            description="You can store power surges whenever you successfully Counterspell or Dispel Magic; when you cast a spell and hit a target, you can expend a surge to deal extra force damage."
        ),
        SubclassFeature(
            name="Durable Magic",
            level=10,
            description="While you are concentrating on a spell, you gain a +2 bonus to AC and all saving throws."
        ),
        SubclassFeature(
            name="Deflecting Shroud",
            level=14,
            description="When you use Arcane Deflection, you can cause energy to lash out at up to three creatures within 60 feet, dealing force damage equal to half your wizard level."
        )
    ]
)

THE_HEXBLADE = Subclass(
    name="The Hexblade",
    class_name="Warlock",
    description="Hexblade patrons are sentient weapons from the Shadowfell, granting warlocks cursed blades and martial prowess tied to gravely serious bargains.",
    selection_level=1,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Expanded Spell List",
            level=1,
            description="You gain access to spells such as Shield, Wrathful Smite, Branding Smite, Elemental Weapon, Banishing Smite, and more that reflect martial shadow magic."
        ),
        SubclassFeature(
            name="Hexblade's Curse",
            level=1,
            description="As a bonus action you can curse a creature for 1 minute, gaining bonus damage, critting on 19-20, and healing when it dies; usable once per short or long rest."
        ),
        SubclassFeature(
            name="Hex Warrior",
            level=1,
            description="You gain proficiency with medium armor, shields, and martial weapons, and can use Charisma for attack and damage rolls with one weapon you touch (extending to pact weapons)."
        ),
        SubclassFeature(
            name="Accursed Specter",
            level=6,
            description="When you slay a humanoid, you can bind its spirit to rise as a specter under your command until your next long rest, gaining bonus temporary hit points when it drains foes."
        ),
        SubclassFeature(
            name="Armor of Hexes",
            level=10,
            description="If the target of your Hexblade's Curse hits you, you can roll a d6; on 4 or higher the attack instead misses you as shadowy wards deflect it."
        ),
        SubclassFeature(
            name="Master of Hexes",
            level=14,
            description="When the creature cursed by your Hexblade's Curse dies, you can apply the curse to a new creature within 30 feet without expending another use."
        )
    ]
)

THE_CELESTIAL = Subclass(
    name="The Celestial",
    class_name="Warlock",
    description="Celestial patrons are empyreal beings who pass fragments of radiant power to warlocks sworn to champion hope and healing.",
    selection_level=1,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Expanded Spell List",
            level=1,
            description="You gain access to spells such as Cure Wounds, Guiding Bolt, Lesser Restoration, Revivify, Guardian of Faith, and more focused on radiant support."
        ),
        SubclassFeature(
            name="Bonus Cantrips",
            level=1,
            description="You learn the Light and Sacred Flame cantrips; they count as warlock cantrips for you but don't count against your known list."
        ),
        SubclassFeature(
            name="Healing Light",
            level=1,
            description="You gain a pool of d6s equal to 1 + your warlock level that you can spend as a bonus action to heal a creature within 60 feet."
        ),
        SubclassFeature(
            name="Radiant Soul",
            level=6,
            description="You gain resistance to radiant damage and, once per turn when you deal radiant or fire damage, you can add your Charisma modifier to one damage roll."
        ),
        SubclassFeature(
            name="Celestial Resilience",
            level=10,
            description="When you finish a short or long rest, you and up to five allies gain temporary hit points (your warlock level + Charisma modifier), and you gain resistance to a damage type you choose."
        ),
        SubclassFeature(
            name="Searing Vengeance",
            level=14,
            description="When you drop to 0 hit points, you can instead explode with radiant light, healing to half your hit points, forcing nearby foes to save or be blinded and take radiant damage."
        )
    ]
)

FORGE_DOMAIN = Subclass(
    name="Forge Domain",
    class_name="Cleric",
    description="Forge clerics serve gods of artisans, industry, and fire, channeling divine craftsmanship to strengthen armor, weapons, and allies.",
    selection_level=1,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Bonus Proficiencies",
            level=1,
            description="You gain proficiency with heavy armor and smith's tools."
        ),
        SubclassFeature(
            name="Blessing of the Forge",
            level=1,
            description="At the end of a long rest you can imbue a weapon or armor with magic, granting a +1 bonus to AC or attack and damage rolls until your next long rest."
        ),
        SubclassFeature(
            name="Channel Divinity: Artisan's Blessing",
            level=2,
            description="You can conduct a 1-hour ritual to craft a nonmagical metal item worth up to 100 gp, transforming raw materials into finished gear."
        ),
        SubclassFeature(
            name="Soul of the Forge",
            level=6,
            description="You gain resistance to fire damage, a +1 bonus to AC while wearing heavy armor, and your weapon attacks deal extra fire damage against constructs."
        ),
        SubclassFeature(
            name="Divine Strike",
            level=8,
            description="Once on each of your turns you can deal an extra 1d8 fire damage with a weapon attack (2d8 at 14th level)."
        ),
        SubclassFeature(
            name="Saint of Forge and Fire",
            level=17,
            description="While wearing heavy armor you gain immunity to fire damage and resistance to bludgeoning, piercing, and slashing damage from nonmagical attacks."
        )
    ]
)

GRAVE_DOMAIN = Subclass(
    name="Grave Domain",
    class_name="Cleric",
    description="Grave clerics stand between life and death, ensuring the natural order of passing and preventing undead profanations.",
    selection_level=1,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Circle of Mortality",
            level=1,
            description="Your healing spells are maximized on creatures at 0 hit points, and you gain spare the dying as a bonus action cantrip with 30-foot range."
        ),
        SubclassFeature(
            name="Eyes of the Grave",
            level=1,
            description="You can sense undead within 60 feet that aren't behind total cover a number of times per long rest equal to your Wisdom modifier."
        ),
        SubclassFeature(
            name="Channel Divinity: Path to the Grave",
            level=2,
            description="As an action you curse a creature, granting vulnerability to all damage from the next attack or spell that hits it before the end of your next turn."
        ),
        SubclassFeature(
            name="Sentinel at Death's Door",
            level=6,
            description="You can use your reaction to prevent a critical hit within 30 feet, turning it into a normal hit a number of times per long rest equal to your Wisdom modifier."
        ),
        SubclassFeature(
            name="Potent Spellcasting",
            level=8,
            description="You add your Wisdom modifier to the damage you deal with any cleric cantrip."
        ),
        SubclassFeature(
            name="Keeper of Souls",
            level=17,
            description="When a creature dies within 60 feet of you, you or another creature of your choice regain hit points equal to the creature's number of Hit Dice (once per turn)."
        )
    ]
)

FORGE_DOMAIN = Subclass(
    name="Forge Domain",
    class_name="Cleric",
    description="Forge clerics serve gods of artisans, industry, and fire, channeling divine craftsmanship to strengthen armor, weapons, and allies.",
    selection_level=1,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Bonus Proficiencies",
            level=1,
            description="You gain proficiency with heavy armor and smith's tools."
        ),
        SubclassFeature(
            name="Blessing of the Forge",
            level=1,
            description="At the end of a long rest you can imbue a weapon or armor with magic, granting a +1 bonus to AC or attack and damage rolls until your next long rest."
        ),
        SubclassFeature(
            name="Channel Divinity: Artisan's Blessing",
            level=2,
            description="You can conduct a 1-hour ritual to craft a nonmagical metal item worth up to 100 gp, transforming raw materials into finished gear."
        ),
        SubclassFeature(
            name="Soul of the Forge",
            level=6,
            description="You gain resistance to fire damage, a +1 bonus to AC while wearing heavy armor, and your weapon attacks deal extra fire damage against constructs."
        ),
        SubclassFeature(
            name="Divine Strike",
            level=8,
            description="Once on each of your turns you can deal an extra 1d8 fire damage with a weapon attack (2d8 at 14th level)."
        ),
        SubclassFeature(
            name="Saint of Forge and Fire",
            level=17,
            description="While wearing heavy armor you gain immunity to fire damage and resistance to bludgeoning, piercing, and slashing damage from nonmagical attacks."
        )
    ]
)

GRAVE_DOMAIN = Subclass(
    name="Grave Domain",
    class_name="Cleric",
    description="Grave clerics stand between life and death, ensuring the natural order of passing and preventing undead profanations.",
    selection_level=1,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Circle of Mortality",
            level=1,
            description="Your healing spells are maximized on creatures at 0 hit points, and you gain spare the dying as a bonus action cantrip with 30-foot range."
        ),
        SubclassFeature(
            name="Eyes of the Grave",
            level=1,
            description="You can sense undead within 60 feet that aren't behind total cover a number of times per long rest equal to your Wisdom modifier."
        ),
        SubclassFeature(
            name="Channel Divinity: Path to the Grave",
            level=2,
            description="As an action you curse a creature, granting vulnerability to all damage from the next attack or spell that hits it before the end of your next turn."
        ),
        SubclassFeature(
            name="Sentinel at Death's Door",
            level=6,
            description="You can use your reaction to prevent a critical hit within 30 feet, turning it into a normal hit a number of times per long rest equal to your Wisdom modifier."
        ),
        SubclassFeature(
            name="Potent Spellcasting",
            level=8,
            description="You add your Wisdom modifier to the damage you deal with any cleric cantrip."
        ),
        SubclassFeature(
            name="Keeper of Souls",
            level=17,
            description="When a creature dies within 60 feet of you, you or another creature of your choice regain hit points equal to the creature's number of Hit Dice (once per turn)."
        )
    ]
)

FORGE_DOMAIN = Subclass(
    name="Forge Domain",
    class_name="Cleric",
    description="Forge clerics serve gods of artisans, industry, and fire, channeling divine craftsmanship to strengthen armor, weapons, and allies.",
    selection_level=1,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Bonus Proficiencies",
            level=1,
            description="You gain proficiency with heavy armor and smith's tools."
        ),
        SubclassFeature(
            name="Blessing of the Forge",
            level=1,
            description="At the end of a long rest you can imbue a weapon or armor with magic, granting a +1 bonus to AC or attack and damage rolls until your next long rest."
        ),
        SubclassFeature(
            name="Channel Divinity: Artisan's Blessing",
            level=2,
            description="You can conduct a 1-hour ritual to craft a nonmagical metal item worth up to 100 gp, transforming raw materials into finished gear."
        ),
        SubclassFeature(
            name="Soul of the Forge",
            level=6,
            description="You gain resistance to fire damage, a +1 bonus to AC while wearing heavy armor, and your weapon attacks deal extra fire damage against constructs."
        ),
        SubclassFeature(
            name="Divine Strike",
            level=8,
            description="Once on each of your turns you can deal an extra 1d8 fire damage with a weapon attack (2d8 at 14th level)."
        ),
        SubclassFeature(
            name="Saint of Forge and Fire",
            level=17,
            description="While wearing heavy armor you gain immunity to fire damage and resistance to bludgeoning, piercing, and slashing damage from nonmagical attacks."
        )
    ]
)

GRAVE_DOMAIN = Subclass(
    name="Grave Domain",
    class_name="Cleric",
    description="Grave clerics stand between life and death, ensuring the natural order of passing and preventing undead profanations.",
    selection_level=1,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Circle of Mortality",
            level=1,
            description="Your healing spells are maximized on creatures at 0 hit points, and you gain spare the dying as a bonus action cantrip with 30-foot range."
        ),
        SubclassFeature(
            name="Eyes of the Grave",
            level=1,
            description="You can sense undead within 60 feet that aren't behind total cover a number of times per long rest equal to your Wisdom modifier."
        ),
        SubclassFeature(
            name="Channel Divinity: Path to the Grave",
            level=2,
            description="As an action you curse a creature, granting vulnerability to all damage from the next attack or spell that hits it before the end of your next turn."
        ),
        SubclassFeature(
            name="Sentinel at Death's Door",
            level=6,
            description="You can use your reaction to prevent a critical hit within 30 feet, turning it into a normal hit a number of times per long rest equal to your Wisdom modifier."
        ),
        SubclassFeature(
            name="Potent Spellcasting",
            level=8,
            description="You add your Wisdom modifier to the damage you deal with any cleric cantrip."
        ),
        SubclassFeature(
            name="Keeper of Souls",
            level=17,
            description="When a creature dies within 60 feet of you, you or another creature of your choice regain hit points equal to the creature's number of Hit Dice (once per turn)."
        )
    ]
)






SCHOOL_OF_SCRIBES = Subclass(
    name="School of Scribes",
    class_name="Wizard",
    description="Scribes are devoted chroniclers of magic who awaken their spellbooks and ink spells into reality with living quills.",
    selection_level=2,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Wizardly Quill",
            level=2,
            description="You conjure a quill that never runs out of ink, halves the time needed to copy spells, and can write on its own."
        ),
        SubclassFeature(
            name="Awakened Spellbook",
            level=2,
            description="Your spellbook becomes sentient, letting you temporarily change a spell's damage type or cast certain spells as rituals even if not prepared."
        ),
        SubclassFeature(
            name="Manifest Mind",
            level=6,
            description="You can project your book's mind as a spectral image that scouts, delivers spells, and shares sight and sound with you."
        ),
        SubclassFeature(
            name="Master Scrivener",
            level=10,
            description="You can create quickened scrolls each day and increase the power of spells cast via scrolls you create."
        ),
        SubclassFeature(
            name="One with the Word",
            level=14,
            description="Your spellbook can absorb spells directed at you, and if it takes damage you can sacrifice prepared spells to prevent the harm."
        )
    ]
)

THE_FATHOMLESS = Subclass(
    name="The Fathomless",
    class_name="Warlock",
    description="Fathomless patrons dwell in the crushing depths—krakens, ancient merfolk, or unknowable leviathans granting abyssal power.",
    selection_level=1,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Expanded Spell List",
            level=1,
            description="You gain aquatic-themed spells such as Fog Cloud, Silence, Lightning Bolt, Control Water, and Cone of Cold."
        ),
        SubclassFeature(
            name="Tentacle of the Deeps",
            level=1,
            description="You can summon a spectral tentacle that lashes foes, dealing cold damage and slowing them."
        ),
        SubclassFeature(
            name="Gift of the Sea",
            level=1,
            description="You gain a swimming speed equal to your walking speed and can breathe underwater."
        ),
        SubclassFeature(
            name="Oceanic Soul",
            level=6,
            description="You adapt to the deep, gaining resistance to cold damage and the ability to speak with aquatic creatures."
        ),
        SubclassFeature(
            name="Guardian Coil",
            level=6,
            description="Your tentacle can protect allies by reducing damage taken when they are struck."
        ),
        SubclassFeature(
            name="Grasping Tentacles",
            level=10,
            description="You can cast Evard's Black Tentacles without a slot once per rest, gaining temporary hit points when you do."
        ),
        SubclassFeature(
            name="Fathomless Plunge",
            level=14,
            description="You can teleport yourself and up to five willing creatures through a watery portal, emulating a sudden plunge through the depths." 
        )
    ]
)

THE_GENIE = Subclass(
    name="The Genie",
    class_name="Warlock",
    description="Genie patrons hail from the Elemental Planes. Each type (Dao, Djinni, Efreeti, Marid) grants magic tied to their element and a mystic vessel.",
    selection_level=1,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Expanded Spell List",
            level=1,
            description="You gain additional spells based on your genie's kind, such as Sanctuary, Spike Growth, Fireball, or Create Food and Water."
        ),
        SubclassFeature(
            name="Genie's Vessel",
            level=1,
            description="You carry a vessel that grants the Bottled Respite ability and lets you add damage once per turn of the type tied to your patron."
        ),
        SubclassFeature(
            name="Elemental Gift",
            level=6,
            description="You gain resistance to your patron's damage type and a flying speed (or burrow/swim for some genies) for short bursts."
        ),
        SubclassFeature(
            name="Sanctuary Vessel",
            level=10,
            description="You can bring allies into your vessel to rest safely, and they gain temporary hit points when they emerge."
        ),
        SubclassFeature(
            name="Limited Wish",
            level=14,
            description="Once per long rest you can produce a limited wish, duplicating a spell of 6th level or lower without material components."
        )
    ]
)

ABERRANT_MIND = Subclass(
    name="Aberrant Mind",
    class_name="Sorcerer",
    description="Aberrant Mind sorcerers manifest psionic magic from eldritch truths, alien influence, or far realm mutations.",
    selection_level=1,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Aberrant Mind Spells",
            level=1,
            description="You gain additional spells focused on telepathy, psychic force, and aberrant themes; they don't count against your known spells."
        ),
        SubclassFeature(
            name="Telepathic Speech",
            level=1,
            description="You can form a telepathic bond as a bonus action, allowing conversation regardless of language."
        ),
        SubclassFeature(
            name="Psionic Sorcery",
            level=6,
            description="You can spend sorcery points to cast your Aberrant Mind spells without verbal, somatic, or material components, and your spells become subtle manifestations of psionic power."
        ),
        SubclassFeature(
            name="Psychic Defenses",
            level=6,
            description="You gain resistance to psychic damage and advantage on saving throws against being charmed or frightened."
        ),
        SubclassFeature(
            name="Revelation in Flesh",
            level=14,
            description="As a bonus action you can spend sorcery points to gain aberrant transformations such as flight, aquatic adaptation, or phase-walking."
        ),
        SubclassFeature(
            name="Warping Implosion",
            level=18,
            description="You can briefly open a psychic maelstrom, teleporting yourself and pulling creatures toward where you stood, dealing force damage."
        )
    ]
)

CLOCKWORK_SOUL = Subclass(
    name="Clockwork Soul",
    class_name="Sorcerer",
    description="Clockwork Soul sorcerers draw their power from lawful planes of order, enforcing balance amid chaos.",
    selection_level=1,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Clockwork Magic",
            level=1,
            description="You gain additional spells that embody precision and control, such as Alarm, Aid, Dispel Magic, and Wall of Force."
        ),
        SubclassFeature(
            name="Restore Balance",
            level=1,
            description="As a reaction you can cancel advantage or disadvantage on a roll within 60 feet, reasserting equilibrium."
        ),
        SubclassFeature(
            name="Bastion of Law",
            level=6,
            description="You can spend sorcery points to surround a creature with protective clockwork energy that converts incoming damage into depleted dice."
        ),
        SubclassFeature(
            name="Trance of Order",
            level=14,
            description="You can enter a state for 1 minute where attack rolls against you can't gain advantage and any roll you make below 10 on an attack or ability check counts as a 10."
        ),
        SubclassFeature(
            name="Clockwork Cavalcade",
            level=18,
            description="You can summon a 30-foot cube of clockwork entities that repair structures, restore hit points, and end certain conditions, before vanishing in sparks of order."
        )
    ]
)

PHANTOM = Subclass(
    name="Phantom",
    class_name="Rogue",
    description="Phantoms walk the line between life and death, communing with fallen spirits to harvest their knowledge and power.",
    selection_level=3,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Whispers of the Dead",
            level=3,
            description="When you finish a long rest, you can choose one skill or tool proficiency the ghosts share with you, temporarily gaining it."
        ),
        SubclassFeature(
            name="Wails from the Grave",
            level=3,
            description="Immediately after you deal Sneak Attack damage, you can deal half that damage to a second creature you can see within 30 feet as spectral energy leaps from the first target."
        ),
        SubclassFeature(
            name="Tokens of the Departed",
            level=9,
            description="When a creature dies near you, you can snare a soul trinket, gaining bonuses to death saves, ability checks, and the ability to ask the spirit questions."
        ),
        SubclassFeature(
            name="Ghost Walk",
            level=13,
            description="You can take on a spectral form as a bonus action, gaining a flight speed, resistance to all damage but force, and the ability to move through objects for 10 minutes."
        ),
        SubclassFeature(
            name="Death's Friend",
            level=17,
            description="Your connection to death deepens, letting you regain expended Wails from the Grave uses when you finish a short rest and granting bonus damage when you have no uses left."
        )
    ]
)

SOULKNIFE = Subclass(
    name="Soulknife",
    class_name="Rogue",
    description="Soulknives wield psionic blades of pure thought, cutting through minds as easily as flesh.",
    selection_level=3,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Psionic Power",
            level=3,
            description="You gain psionic energy dice and abilities such as Psi-Bolstered Knack to rescue failed rolls and Psychic Whispers to speak telepathically."
        ),
        SubclassFeature(
            name="Psychic Blades",
            level=3,
            description="You can manifest a pair of psychic blades as part of your attacks, dealing psychic damage and vanishing after a hit."
        ),
        SubclassFeature(
            name="Soul Blades",
            level=9,
            description="You unlock Homing Strikes to reroll misses and Psychic Teleportation to hurl a blade and teleport to it."
        ),
        SubclassFeature(
            name="Psychic Veil",
            level=13,
            description="You can become invisible for 1 hour or until you deal damage, thanks to psionic camouflage."
        ),
        SubclassFeature(
            name="Rend Mind",
            level=17,
            description="When you use Psychic Blades to hit a creature, you can force it to make a Wisdom save or be stunned for 1 minute, taking extra psychic damage on subsequent turns."
        )
    ]
)

FEY_WANDERER = Subclass(
    name="Fey Wanderer",
    class_name="Ranger",
    description="Fey Wanderers have seen the Feywild's beauty and danger firsthand, carrying its magic back into the mortal world.",
    selection_level=3,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Fey Wanderer Magic",
            level=3,
            description="You gain additional spells like Charm Person, Misty Step, and Greater Invisibility which are always prepared."
        ),
        SubclassFeature(
            name="Dreadful Strikes",
            level=3,
            description="Once per turn when you hit a creature with a weapon attack, you can deal extra psychic damage and mark it with fey magic."
        ),
        SubclassFeature(
            name="Otherworldly Glamour",
            level=3,
            description="You gain proficiency in one skill of your choice and can add Wisdom modifier to Charisma checks, reflecting your enchanting presence."
        ),
        SubclassFeature(
            name="Beguiling Twist",
            level=7,
            description="When a creature succeeds on a saving throw against your enchantment or fear effects, you can redirect the magic to another target."
        ),
        SubclassFeature(
            name="Fey Reinforcements",
            level=11,
            description="You can summon a fey spirit without material components, and it gains extra hit points equal to your Wisdom modifier."
        ),
        SubclassFeature(
            name="Misty Wanderer",
            level=15,
            description="You can cast Misty Step without expending a spell slot several times per long rest and can bring allies with you."
        )
    ]
)

SWARMKEEPER = Subclass(
    name="Swarmkeeper",
    class_name="Ranger",
    description="Swarmkeepers bond with nature spirits that manifest as swarms of insects, birds, or other tiny creatures supporting every attack.",
    selection_level=3,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Swarmkeeper Magic",
            level=3,
            description="You gain additional spells such as Faerie Fire, Web, and Insect Plague that are always prepared."
        ),
        SubclassFeature(
            name="Gathered Swarm",
            level=3,
            description="When you hit with a weapon attack, your swarm can move the target, move you, or deal extra damage."
        ),
        SubclassFeature(
            name="Writhing Tide",
            level=7,
            description="You can briefly gain a flying speed as the swarm lifts you into the air."
        ),
        SubclassFeature(
            name="Mighty Swarm",
            level=11,
            description="Your swarm's attacks deal more damage and can knock creatures prone or move them further."
        ),
        SubclassFeature(
            name="Swarming Dispersal",
            level=15,
            description="When you take damage, you can have your swarm teleport you and grant resistance to that damage."
        )
    ]
)

OATH_OF_GLORY = Subclass(
    name="Oath of Glory",
    class_name="Paladin",
    description="Glory paladins seek the spotlight of heroism, pushing themselves and allies toward legendary deeds.",
    selection_level=3,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Oath Spells",
            level=3,
            description="You gain an oath spell list focused on heroism and mobility, including Guiding Bolt, Enhance Ability, Haste, Compulsion, and more."
        ),
        SubclassFeature(
            name="Channel Divinity: Peerless Athlete",
            level=3,
            description="You can use Channel Divinity to gain a massive boost to Strength and Dexterity checks, letting you leap, climb, or swim with Olympian prowess for 10 minutes."
        ),
        SubclassFeature(
            name="Channel Divinity: Inspiring Smite",
            level=3,
            description="Immediately after you deal Divine Smite damage, you can distribute temporary hit points to creatures within 30 feet, sharing your triumph."
        ),
        SubclassFeature(
            name="Aura of Alacrity",
            level=7,
            description="You and allies within 5 feet (10 feet at 18th level) gain a speed bonus when they start their turn in your aura, encouraging swift strikes."
        ),
        SubclassFeature(
            name="Glorious Defense",
            level=15,
            description="When you or a creature within 10 feet is hit, you can use your reaction to grant a bonus to AC that may cause the attack to miss and, if it misses, you can make one weapon attack."
        ),
        SubclassFeature(
            name="Living Legend",
            level=20,
            description="As a bonus action you can become a living legend for 1 minute, gaining advantage on Charisma checks, turning misses into hits, and rerolling failed saving throws once per turn."
        )
    ]
)

OATH_OF_THE_WATCHERS = Subclass(
    name="Oath of the Watchers",
    class_name="Paladin",
    description="Watchers paladins guard the mortal realms from extraplanar threats, ever vigilant against cosmic intruders.",
    selection_level=3,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Oath Spells",
            level=3,
            description="Your oath spells emphasize detection and banishment, including Alarm, Moonbeam, Counterspell, Banishment, Hold Monster, and more."
        ),
        SubclassFeature(
            name="Channel Divinity: Watcher's Will",
            level=3,
            description="You can use Channel Divinity to grant advantage on Intelligence, Wisdom, and Charisma saves to yourself and allies within 30 feet."
        ),
        SubclassFeature(
            name="Channel Divinity: Abjure the Extraplanar",
            level=3,
            description="As an action you can rebuke aberrations, celestials, elementals, fey, and fiends, forcing them to make a saving throw or be turned."
        ),
        SubclassFeature(
            name="Aura of the Sentinel",
            level=7,
            description="You and allies within 10 feet (30 at 18th level) add your proficiency bonus to initiative rolls."
        ),
        SubclassFeature(
            name="Vigilant Rebuke",
            level=15,
            description="When a creature within 30 feet succeeds on a saving throw due to Watcher's Will, you can deal psychic damage to the attacker as a reaction."
        ),
        SubclassFeature(
            name="Mortal Bulwark",
            level=20,
            description="As a bonus action you can manifest a ward for 1 minute, gaining truesight, advantage against extraplanar foes, and the ability to banish them when you hit."
        )
    ]
)

WAY_OF_MERCY = Subclass(
    name="Way of Mercy",
    class_name="Monk",
    description="Mercy monks blend masked theatrics with pressure-point strikes, delivering both miraculous healing and lethal harm.",
    selection_level=3,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Implements of Mercy",
            level=3,
            description="You gain proficiency with Insight, Medicine, and the herbalism kit, adopting ceremonial garb to hide your face."
        ),
        SubclassFeature(
            name="Hand of Healing",
            level=3,
            description="You can spend ki to heal as an action or as part of Flurry of Blows, restoring hit points equal to a Martial Arts die + your Wisdom modifier."
        ),
        SubclassFeature(
            name="Hand of Harm",
            level=3,
            description="When you hit a creature with an unarmed strike, you can spend 1 ki to deal extra necrotic damage equal to one Martial Arts die + your Wisdom modifier and potentially impose the poisoned condition."
        ),
        SubclassFeature(
            name="Physician's Touch",
            level=6,
            description="Your healing ends disease and poison, while your Hand of Harm can poison targets without requiring a save."
        ),
        SubclassFeature(
            name="Flurry of Healing and Harm",
            level=11,
            description="When you use Flurry of Blows, you can replace attacks with Hand of Healing or Hand of Harm at reduced ki costs, spreading aid or suffering across the battlefield."
        ),
        SubclassFeature(
            name="Hand of Ultimate Mercy",
            level=17,
            description="As an action you can spend 5 ki points to touch a creature and revive it to full consciousness, curing diseases, poisons, and restoring hit points."
        )
    ]
)

WAY_OF_THE_ASTRAL_SELF = Subclass(
    name="Way of the Astral Self",
    class_name="Monk",
    description="Astral Self monks project a luminous avatar that manifests their true inner power as spectral arms, visage, and body.",
    selection_level=3,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Arms of the Astral Self",
            level=3,
            description="You can spend 1 ki point to summon spectral arms for 10 minutes, using Wisdom for attacks, dealing force damage, and gaining reach plus the ability to shove with ki."
        ),
        SubclassFeature(
            name="Visage of the Astral Self",
            level=6,
            description="You can manifest an astral mask that grants darkvision, advantage on Insight and intimidation, and the ability to speak telepathically."
        ),
        SubclassFeature(
            name="Body of the Astral Self",
            level=11,
            description="Your astral form grants resistance to elemental damage types and lets you deflect attacks with reactions that reduce damage to others."
        ),
        SubclassFeature(
            name="Awakening of the Astral Self",
            level=17,
            description="You can spend ki to fully manifest head, arms, and body at once, gaining additional attacks, extra reach, and the ability to impose multiple saving throws on foes."
        )
    ]
)

PSI_WARRIOR = Subclass(
    name="Psi Warrior",
    class_name="Fighter",
    description="Psi Warriors awaken latent psionic power, projecting invisible force to shield allies and crush foes.",
    selection_level=3,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Psionic Power",
            level=3,
            description="You gain psionic energy dice that fuel abilities such as Psionic Strike for bonus force damage, Telekinetic Movement to reposition objects or allies, and Protective Field to reduce incoming damage."
        ),
        SubclassFeature(
            name="Telekinetic Adept",
            level=7,
            description="You learn Psi-Powered Leap for burst movement and Telekinetic Thrust to knock enemies prone or hurl them away when you use Psionic Strike."
        ),
        SubclassFeature(
            name="Guarded Mind",
            level=10,
            description="You gain resistance to psychic damage and can end charmed or frightened on yourself by expending a psionic die."
        ),
        SubclassFeature(
            name="Bulwark of Force",
            level=15,
            description="As a bonus action you can give yourself and allies half cover for 1 minute, creating a shimmering telekinetic barrier."
        ),
        SubclassFeature(
            name="Telekinetic Master",
            level=18,
            description="You can cast Telekinesis once per long rest without components, and while concentrating you can make a bonus-action attack that deals force damage equal to your psionic die."
        )
    ]
)

RUNE_KNIGHT = Subclass(
    name="Rune Knight",
    class_name="Fighter",
    description="Rune Knights study giant runes, carving sigils onto weapons and armor to harness primeval magic.",
    selection_level=3,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Bonus Proficiencies",
            level=3,
            description="You gain proficiency with smith's tools and learn Giant, reflecting your study of rune lore."
        ),
        SubclassFeature(
            name="Rune Carver & Giant's Might",
            level=3,
            description="You learn to inscribe two runes that grant magic powers (like Cloud, Fire, Frost, etc.), and you can invoke Giant's Might to grow in size, deal extra damage, and gain advantage on Strength checks and saves."
        ),
        SubclassFeature(
            name="Runic Shield",
            level=7,
            description="When an ally within 60 feet is hit, you can use your reaction to force a reroll, protecting them with rune magic."
        ),
        SubclassFeature(
            name="Great Stature",
            level=10,
            description="You grow taller (1d4 inches) and your Giant's Might damage increases."
        ),
        SubclassFeature(
            name="Master of Runes",
            level=15,
            description="You can activate each rune you know twice per short rest instead of once."
        ),
        SubclassFeature(
            name="Runic Juggernaut",
            level=18,
            description="Your Giant's Might size increases, you gain bonus Strength checks advantage constantly, and your additional damage die becomes d10s."
        )
    ]
)

CIRCLE_OF_SPORES = Subclass(
    name="Circle of Spores",
    class_name="Druid",
    description="Spores druids mingle with fungal colonies, wielding decay and rebirth as weapons while surrounding themselves with necrotic blooms.",
    selection_level=2,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Circle Spells",
            level=2,
            description="You gain access to a roster of necrotic- and fungus-themed spells such as Chill Touch, Blindness/Deafness, Animate Dead, and more, which are always prepared for you."
        ),
        SubclassFeature(
            name="Halo of Spores",
            level=2,
            description="As a reaction you can deal necrotic damage to creatures that start their turn within 10 feet of you, representing the spores orbiting your body."
        ),
        SubclassFeature(
            name="Symbiotic Entity",
            level=2,
            description="You can expend Wild Shape to awaken spores, gaining temporary hit points, bonus necrotic damage, and augmented Halo of Spores while the effect lasts."
        ),
        SubclassFeature(
            name="Fungal Infestation",
            level=6,
            description="When a Small or Medium creature dies within 10 feet of you, you can animate it as a zombie that immediately takes a turn after yours."
        ),
        SubclassFeature(
            name="Spreading Spores",
            level=10,
            description="You can hurl your Halo of Spores to create a 10-foot cube of necrotic fungus that damages enemies and can be moved as a bonus action."
        ),
        SubclassFeature(
            name="Fungal Body",
            level=14,
            description="You become more plant than humanoid: you can't be blinded, deafened, frightened, or poisoned, and critical hits deal normal damage to you."
        )
    ]
)

CIRCLE_OF_STARS = Subclass(
    name="Circle of Stars",
    class_name="Druid",
    description="Stars druids seek constellations as guides, shaping their Wild Shape into living starlight and reading omens from the night sky.",
    selection_level=2,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Star Map",
            level=2,
            description="You craft a star map focus that grants you Guiding Bolt, augury-like guidance, and acts as a spellcasting focus."
        ),
        SubclassFeature(
            name="Starry Form",
            level=2,
            description="You can expend Wild Shape to become a constellation (Archer, Chalice, or Dragon), gaining unique bonuses such as radiant arrow attacks, boosted healing, or improved concentration."
        ),
        SubclassFeature(
            name="Circle Spells",
            level=2,
            description="You always have certain star-themed spells prepared, including Guiding Bolt, Moonbeam, Conjure Animals, and more."
        ),
        SubclassFeature(
            name="Cosmic Omen",
            level=6,
            description="When you finish a long rest you roll to see whether benevolent (Weal) or malevolent (Woe) omens guide you, granting reaction abilities to add or subtract d6s from rolls."
        ),
        SubclassFeature(
            name="Twinkling Constellations",
            level=10,
            description="Your Starry Form options improve: Archer deals more damage, Chalice heals more, and Dragon grants a flying speed."
        ),
        SubclassFeature(
            name="Full of Stars",
            level=14,
            description="While in Starry Form you gain resistance to bludgeoning, piercing, and slashing damage, embodying stellar resilience."
        )
    ]
)

CIRCLE_OF_WILDFIRE = Subclass(
    name="Circle of Wildfire",
    class_name="Druid",
    description="Wildfire druids embrace the cycle of destruction and renewal, summoning elemental flames to purge and regrow the natural world.",
    selection_level=2,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Circle Spells",
            level=2,
            description="You always have wildfire-themed spells prepared, from Burning Hands to Flamestrike and Flame Strike."
        ),
        SubclassFeature(
            name="Summon Wildfire Spirit",
            level=2,
            description="You can expend Wild Shape to summon a Wildfire Spirit that acts on its own initiative, blasting foes and teleporting you and allies through flames."
        ),
        SubclassFeature(
            name="Enhanced Bond",
            level=6,
            description="While your Wildfire Spirit is summoned, your fire spells deal extra damage or your healing spells heal extra points, and the spirit can deliver certain spells for you."
        ),
        SubclassFeature(
            name="Cauterizing Flames",
            level=10,
            description="When a creature dies within 30 feet of you or your spirit, motes of flame either heal allies or scorch enemies."
        ),
        SubclassFeature(
            name="Blazing Revival",
            level=14,
            description="If you drop to 0 hit points and your spirit is present, you can have it sacrifice itself to revive you with half hit points and move you to safety."
        )
    ]
)

PEACE_DOMAIN = Subclass(
    name="Peace Domain",
    class_name="Cleric",
    description="Clerics of peace safeguard diplomacy, mediation, and bonds between allies, magically knitting companions into a united front.",
    selection_level=1,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Implements of Peace",
            level=1,
            description="You gain proficiency with Insight, Performance, or Persuasion (your choice), ensuring you can calm tempers in any court."
        ),
        SubclassFeature(
            name="Emboldening Bond",
            level=1,
            description="Through a ritual you bond willing creatures. While bonded and within 30 feet of another bonded ally, once per turn a creature can add 1d4 to an attack roll, ability check, or saving throw."
        ),
        SubclassFeature(
            name="Channel Divinity: Balm of Peace",
            level=2,
            description="You can use an action to move up to your speed without provoking attacks, touching creatures along the way and restoring 2d6 + your Wisdom modifier hit points to each."
        ),
        SubclassFeature(
            name="Protective Bond",
            level=6,
            description="Bonded creatures can use their reactions to teleport next to one another and absorb damage, representing their shared protection."
        ),
        SubclassFeature(
            name="Potent Spellcasting",
            level=8,
            description="You add your Wisdom modifier to damage rolls of any cleric cantrip."
        ),
        SubclassFeature(
            name="Expansive Bond",
            level=17,
            description="Your bond range increases to 60 feet and when a bonded ally uses the reaction to take damage for another, they both gain resistance to that damage type for the triggering instance."
        )
    ]
)

TWILIGHT_DOMAIN = Subclass(
    name="Twilight Domain",
    class_name="Cleric",
    description="Twilight clerics usher creatures safely through darkness, wielding dusk and dawn to protect their companions.",
    selection_level=1,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Bonus Proficiencies",
            level=1,
            description="You gain proficiency with martial weapons and heavy armor, ready to stand watch through the longest night."
        ),
        SubclassFeature(
            name="Eyes of Night",
            level=1,
            description="You have darkvision out to 300 feet and can share it with a limited number of allies for 1 hour."
        ),
        SubclassFeature(
            name="Vigilant Blessing",
            level=1,
            description="As an action you grant advantage on the next initiative roll to yourself or an ally, providing perpetual vigilance."
        ),
        SubclassFeature(
            name="Channel Divinity: Twilight Sanctuary",
            level=2,
            description="You emanate a calming sphere of twilight for 1 minute, granting temp HP or ending charmed/frightened on allies that start their turns inside."
        ),
        SubclassFeature(
            name="Steps of Night",
            level=6,
            description="While in dim light or darkness you can use a bonus action to gain a flying speed equal to your walking speed for 1 minute."
        ),
        SubclassFeature(
            name="Divine Strike",
            level=8,
            description="Once on each of your turns when you hit with a weapon attack, you deal an extra 1d8 radiant damage (2d8 at 14th level)."
        ),
        SubclassFeature(
            name="Twilight Shroud",
            level=17,
            description="Creatures granted temp HP by your Twilight Sanctuary also benefit from half cover while inside the sphere, sheltering them from harm."
        )
    ]
)

COLLEGE_OF_CREATION = Subclass(
    name="College of Creation",
    class_name="Bard",
    description="Creation bards tap into the Song of Creation, weaving music and art into tangible reality.",
    selection_level=3,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Mote of Potential",
            level=3,
            description="Whenever one of your Bardic Inspiration dice is rolled, you can add an extra effect depending on whether the die was used for an ability check, attack, or saving throw, causing additional damage, healing, or bursts of light."
        ),
        SubclassFeature(
            name="Performance of Creation",
            level=3,
            description="As an action you can create a nonmagical item worth up to 20 × your bard level in gold pieces, which lasts hours equal to your Charisma modifier. At higher levels the size and value increase."
        ),
        SubclassFeature(
            name="Animating Performance",
            level=6,
            description="You can animate a Large or smaller nonmagical item, turning it into a dancing companion that fights for you using your spell save DC."
        ),
        SubclassFeature(
            name="Creative Crescendo",
            level=14,
            description="Performance of Creation can now maintain several creations at once, and you can create larger or more valuable objects without expending spell slots."
        )
    ]
)

COLLEGE_OF_ELOQUENCE = Subclass(
    name="College of Eloquence",
    class_name="Bard",
    description="Eloquence bards are masters of rhetoric who use flawless oratory to sway allies and foes alike.",
    selection_level=3,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Silver Tongue",
            level=3,
            description="Whenever you make a Persuasion or Deception check, treat any d20 roll of 9 or lower as a 10, ensuring near-perfect social poise."
        ),
        SubclassFeature(
            name="Unsettling Words",
            level=3,
            description="As a bonus action you can expend a Bardic Inspiration use to subtract the die from a creature's next saving throw before the end of your next turn."
        ),
        SubclassFeature(
            name="Unfailing Inspiration",
            level=6,
            description="If a creature adds one of your Bardic Inspiration dice and still fails, the die is not expended."
        ),
        SubclassFeature(
            name="Universal Speech",
            level=6,
            description="You can make yourself understood by any creature, granting a number of targets equal to your Charisma modifier the ability to comprehend you for 1 hour."
        ),
        SubclassFeature(
            name="Infectious Inspiration",
            level=14,
            description="When you see an ally within 60 feet succeed using your Bardic Inspiration, you can (once per turn) grant a second creature a free Bardic Inspiration without expending a use."
        )
    ]
)

KNOWLEDGE_DOMAIN = Subclass(
    name="Knowledge Domain",
    class_name="Cleric",
    description="The gods of knowledge value learning and understanding above all. Clerics of this domain serve as scholars, sages, and guardians of ancient lore, preserving secrets and uncovering lost truths.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Blessings of Knowledge",
            level=1,
            description="You learn two languages of your choice. You also become proficient in two of the following skills of your choice: Arcana, History, Nature, or Religion. Your proficiency bonus is doubled for any ability check you make that uses either of those skills."
        ),
        SubclassFeature(
            name="Channel Divinity: Knowledge of the Ages",
            level=2,
            description="You can use your Channel Divinity to tap into a divine well of knowledge. As an action, you choose one skill or tool. For 10 minutes, you have proficiency with the chosen skill or tool."
        ),
        SubclassFeature(
            name="Channel Divinity: Read Thoughts",
            level=6,
            description="You can use your Channel Divinity to read a creature's thoughts. You can then attempt to leave a suggestion in its mind, as per the Suggestion spell, without expending a spell slot."
        ),
        SubclassFeature(
            name="Potent Spellcasting",
            level=8,
            description="You add your Wisdom modifier to the damage you deal with any cleric cantrip."
        ),
        SubclassFeature(
            name="Visions of the Past",
            level=17,
            description="You can call up visions of the past related to an object you touch or the location you are in. After meditating for 1 minute, you receive dreamlike, shadowy glimpses of events that occurred involving the object or in the location."
        )
    ]
)

LIGHT_DOMAIN = Subclass(
    name="Light Domain",
    class_name="Cleric",
    description="Clerics of the Light domain are enlightened souls infused with radiance and the power of fire. They bring light to the darkest places and banish shadows and fear.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Bonus Cantrip",
            level=1,
            description="You gain the Light cantrip if you don't already know it."
        ),
        SubclassFeature(
            name="Warding Flare",
            level=1,
            description="When you are attacked by a creature within 30 feet of you that you can see, you can use your reaction to impose disadvantage on that attack roll by interposing divine light. You can use this feature a number of times equal to your Wisdom modifier (minimum of once), regaining all expended uses when you finish a long rest."
        ),
        SubclassFeature(
            name="Channel Divinity: Radiance of the Dawn",
            level=2,
            description="You can use your Channel Divinity to dispel magical darkness and deal radiant damage. As an action, you present your holy symbol, and any magical darkness within 30 feet is dispelled. Additionally, each hostile creature within 30 feet must make a Constitution saving throw or take 2d10 + your cleric level radiant damage (half on a success)."
        ),
        SubclassFeature(
            name="Improved Flare",
            level=6,
            description="You can now use your Warding Flare feature to protect a creature other than yourself."
        ),
        SubclassFeature(
            name="Potent Spellcasting",
            level=8,
            description="You add your Wisdom modifier to the damage you deal with any cleric cantrip."
        ),
        SubclassFeature(
            name="Corona of Light",
            level=17,
            description="You can use your action to activate an aura of radiant light that lasts for 1 minute. It sheds bright light in a 60-foot radius and dim light for an additional 30 feet. Any hostile creature that starts its turn in the aura has disadvantage on saving throws against spells that deal fire or radiant damage until your aura ends."
        )
    ]
)

NATURE_DOMAIN = Subclass(
    name="Nature Domain",
    class_name="Cleric",
    description="The Nature domain grants clerics the power to command the primal forces of the natural world. These clerics serve deities of the wild, acting as intermediaries between civilization and nature.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Acolyte of Nature",
            level=1,
            description="You learn one druid cantrip of your choice. You also gain proficiency in one of the following skills of your choice: Animal Handling, Nature, or Survival."
        ),
        SubclassFeature(
            name="Bonus Proficiency",
            level=1,
            description="You gain proficiency with heavy armor."
        ),
        SubclassFeature(
            name="Channel Divinity: Charm Animals and Plants",
            level=2,
            description="You can use your Channel Divinity to charm animals and plants. As an action, you present your holy symbol. Each beast or plant creature within 30 feet of you that can see you must make a Wisdom saving throw or be charmed for 1 minute or until it takes damage."
        ),
        SubclassFeature(
            name="Dampen Elements",
            level=6,
            description="When you or a creature within 30 feet of you takes acid, cold, fire, lightning, or thunder damage, you can use your reaction to grant resistance to that instance of damage."
        ),
        SubclassFeature(
            name="Divine Strike",
            level=8,
            description="Once on each of your turns when you hit a creature with a weapon attack, you can cause the attack to deal an extra 1d8 cold, lightning, or thunder damage of your choice. The extra damage increases to 2d8 at 14th level."
        ),
        SubclassFeature(
            name="Master of Nature",
            level=17,
            description="When you use your Channel Divinity: Charm Animals and Plants, you can affect any number of creatures you choose within range, and charmed creatures no longer become hostile to you or your allies when the charm ends."
        )
    ]
)

TEMPEST_DOMAIN = Subclass(
    name="Tempest Domain",
    class_name="Cleric",
    description="The Tempest domain calls down the fury of the storm. Clerics of this domain can unleash thunder and lightning upon their foes and harness the chaotic power of wind and rain.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Bonus Proficiencies",
            level=1,
            description="You gain proficiency with martial weapons and heavy armor."
        ),
        SubclassFeature(
            name="Wrath of the Storm",
            level=1,
            description="When a creature within 5 feet of you that you can see hits you with an attack, you can use your reaction to strike it with lightning or thunder. The creature takes 2d8 lightning or thunder damage (your choice), and it must make a Dexterity saving throw or take the full damage (half on success). You can use this feature a number of times equal to your Wisdom modifier (minimum of once)."
        ),
        SubclassFeature(
            name="Channel Divinity: Destructive Wrath",
            level=2,
            description="You can use your Channel Divinity to maximize lightning or thunder damage. When you roll lightning or thunder damage, you can use your Channel Divinity to deal maximum damage instead of rolling."
        ),
        SubclassFeature(
            name="Thunderbolt Strike",
            level=6,
            description="When you deal lightning damage to a Large or smaller creature, you can also push it up to 10 feet away from you."
        ),
        SubclassFeature(
            name="Divine Strike",
            level=8,
            description="Once on each of your turns when you hit with a weapon attack, you can deal an extra 1d8 thunder damage. The extra damage increases to 2d8 at 14th level."
        ),
        SubclassFeature(
            name="Stormborn",
            level=17,
            description="You have a flying speed equal to your walking speed whenever you are in stormy conditions (rain, wind, or lightning)."
        )
    ]
)

TRICKERY_DOMAIN = Subclass(
    name="Trickery Domain",
    class_name="Cleric",
    description="Clerics of the Trickery domain serve gods of mischief, deception, and thieves. They delight in confounding their foes, stealing from the arrogant, and spreading misdirection wherever they go.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Blessing of the Trickster",
            level=1,
            description="You can use your action to touch a willing creature other than yourself to give it advantage on Dexterity (Stealth) checks for 1 hour."
        ),
        SubclassFeature(
            name="Channel Divinity: Invoke Duplicity",
            level=2,
            description="You can use your Channel Divinity to create an illusory duplicate of yourself. As an action, you create a perfect illusion of yourself that lasts for 1 minute. You can cast spells from the duplicate's space, and you gain advantage on attack rolls against a creature if both you and your illusion are within 5 feet of it."
        ),
        SubclassFeature(
            name="Channel Divinity: Cloak of Shadows",
            level=6,
            description="You can use your Channel Divinity to vanish. As an action, you become invisible until the end of your next turn."
        ),
        SubclassFeature(
            name="Divine Strike",
            level=8,
            description="Once on each of your turns when you hit a creature with a weapon attack, you can cause the attack to deal an extra 1d8 poison damage. The extra damage increases to 2d8 at 14th level."
        ),
        SubclassFeature(
            name="Improved Duplicity",
            level=17,
            description="You can create up to four duplicates of yourself using Invoke Duplicity, and moving any of the duplicates uses no additional action."
        )
    ]
)

TOTEM_WARRIOR = Subclass(
    name="Path of the Totem Warrior",
    class_name="Barbarian",
    description="The Path of the Totem Warrior is a spiritual journey, as the barbarian accepts a spirit animal as guide, protector, and inspiration.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Spirit Seeker",
            level=3,
            description="Yours is a path that seeks attunement with the natural world, giving you a kinship with beasts. You gain the ability to cast the Beast Sense and Speak with Animals spells, but only as rituals."
        ),
        SubclassFeature(
            name="Totem Spirit",
            level=3,
            description="You choose a totem spirit and gain its feature. You must make or acquire a physical totem object—an amulet or similar adornment—that incorporates fur or feathers, claws, teeth, or bones of the totem animal.\n\nBear: While raging, you have resistance to all damage except psychic damage.\nEagle: While raging, other creatures have disadvantage on opportunity attack rolls against you.\nWolf: While raging, your friends have advantage on melee attack rolls against any creature within 5 feet of you that is hostile to you."
        ),
        SubclassFeature(
            name="Aspect of the Beast",
            level=6,
            description="You gain a magical benefit based on the totem animal of your choice.\n\nBear: You gain the might of a bear. Your carrying capacity (including maximum load and maximum lift) is doubled, and you have advantage on Strength checks made to push, pull, lift, or break objects.\nEagle: You gain the eyesight of an eagle. You can see up to 1 mile away with no difficulty, able to discern even fine details as though looking at something no more than 100 feet away from you. Additionally, dim light doesn't impose disadvantage on your Wisdom (Perception) checks.\nWolf: You gain the hunting sensibilities of a wolf. You can track other creatures while traveling at a fast pace, and you can move stealthily while traveling at a normal pace."
        ),
        SubclassFeature(
            name="Spirit Walker",
            level=10,
            description="You can cast the Commune with Nature spell, but only as a ritual. When you do so, a spiritual version of one of the animals you chose for Totem Spirit or Aspect of the Beast appears to you to convey the information you seek."
        ),
        SubclassFeature(
            name="Totemic Attunement",
            level=14,
            description="You gain a magical benefit based on a totem animal of your choice.\n\nBear: While you're raging, any creature within 5 feet of you that's hostile to you has disadvantage on attack rolls against targets other than you or another character with this feature.\nEagle: While raging, you have a flying speed equal to your current walking speed. This benefit works only in short bursts; you fall if you end your turn in the air and nothing else is holding you aloft.\nWolf: While you're raging, you can use a bonus action on your turn to knock a Large or smaller creature prone when you hit it with melee weapon attack."
        )
    ]
)

PATH_OF_THE_ANCESTRAL_GUARDIAN = Subclass(
    name="Path of the Ancestral Guardian",
    class_name="Barbarian",
    description="Barbarians of the Ancestral Guardian path fight alongside spectral ancestors who shield allies and harry foes.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Ancestral Protectors",
            level=3,
            description="When you rage, spectral warriors appear. The first creature you hit on each of your turns becomes hindered by them until the start of your next turn: it has disadvantage on attack rolls against targets other than you, and those targets gain resistance to the damage it deals."
        ),
        SubclassFeature(
            name="Spirit Shield",
            level=6,
            description="While raging you can use your reaction to reduce damage taken by a creature within 30 feet by 2d6 (scaling to 3d6 at 10th level and 4d6 at 15th) as ancestral spirits deflect the blow."
        ),
        SubclassFeature(
            name="Consult the Spirits",
            level=10,
            description="You cast Augury or Clairvoyance as a ritual, gaining temporary spiritual insight. When you do, your Consult takes on ethereal form guided by your ancestors."
        ),
        SubclassFeature(
            name="Vengeful Ancestors",
            level=14,
            description="When Spirit Shield reduces damage, the attacker takes force damage equal to the amount prevented as your guardians lash out."
        )
    ]
)

PATH_OF_THE_STORM_HERALD = Subclass(
    name="Path of the Storm Herald",
    class_name="Barbarian",
    description="Storm Heralds carry the fury of desert, sea, or tundra storms inside them, erupting in elemental auras when they rage.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Storm Aura",
            level=3,
            description="While raging you emit a 10-foot aura tied to desert, sea, or tundra. As a bonus action each turn you can unleash its effect, such as scorching nearby foes, jolting enemies with lightning, or granting temporary hit points against the chill. You can change the environment when you finish a long rest."
        ),
        SubclassFeature(
            name="Storm Soul",
            level=6,
            description="Your chosen storm grants permanent benefits: resistance to fire, lightning, or cold; the ability to breathe underwater or in extreme heat; and utility touches like lighting or miniature storms that reflect your aura type."
        ),
        SubclassFeature(
            name="Shielding Storm",
            level=10,
            description="Creatures of your choice in your aura gain the same damage resistance provided by your Storm Soul, letting you shelter allies from the elements."
        ),
        SubclassFeature(
            name="Raging Storm",
            level=14,
            description="Your aura lashes out when creatures in it harm your allies. Depending on your environment, you can knock foes prone with thunder, deal lightning damage, or reduce an enemy's speed as the tundra freezes their stride."
        )
    ]
)

PATH_OF_THE_ZEALOT = Subclass(
    name="Path of the Zealot",
    class_name="Barbarian",
    description="Zealots channel divine fury through their rage, becoming holy terrors who refuse to fall.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Divine Fury",
            level=3,
            description="While raging, the first creature you hit on each of your turns takes extra necrotic or radiant damage equal to 1d6 + half your barbarian level as divine wrath erupts through the blow."
        ),
        SubclassFeature(
            name="Warrior of the Gods",
            level=3,
            description="Spells that raise you from the dead don't require material components, making it easier for allies to return you to the fight."
        ),
        SubclassFeature(
            name="Fanatical Focus",
            level=6,
            description="Once per rage you can reroll a failed saving throw, representing your stubborn faith clawing you back from disaster."
        ),
        SubclassFeature(
            name="Zealous Presence",
            level=10,
            description="As a bonus action, unleash a battle cry that grants you and up to ten creatures advantage on attack rolls and saving throws for 1 minute or until you end the rage."
        ),
        SubclassFeature(
            name="Rage Beyond Death",
            level=14,
            description="While raging you fight on at 0 hit points without falling unconscious, only succumbing when your rage ends and you still have 0 hit points."
        )
    ]
)

PATH_OF_THE_BEAST = Subclass(
    name="Path of the Beast",
    class_name="Barbarian",
    description="Your inner beast awakens when you rage, letting you manifest natural weapons and hunt with feral instincts.",
    selection_level=3,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Form of the Beast",
            level=3,
            description="When you enter your rage you can manifest a bite, claws, or tail that lasts for the rage, each providing unique attack options and scaling damage."
        ),
        SubclassFeature(
            name="Bestial Soul",
            level=6,
            description="Your natural weapons count as magical and adapt to the environment, granting benefits like climbing, swimming, or breathing underwater depending on the terrain you rest in."
        ),
        SubclassFeature(
            name="Infectious Fury",
            level=10,
            description="Once per turn when you hit with your Form of the Beast, you can force a Wisdom save to either deal psychic damage or compel the target to use its reaction to attack another creature of your choice."
        ),
        SubclassFeature(
            name="Call the Hunt",
            level=14,
            description="When you enter your rage you can share your ferocity with willing creatures, granting them bonus damage while you gain temporary hit points for each one."
        )
    ]
)

PATH_OF_WILD_MAGIC = Subclass(
    name="Path of Wild Magic",
    class_name="Barbarian",
    description="Wild Magic barbarians embrace unpredictable forces, channeling planar energies that erupt each time they rage.",
    selection_level=3,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Magic Awareness",
            level=3,
            description="As an action you can sense magic for 1 minute, learning the school of any spell or magic item within 60 feet a number of times per long rest equal to your proficiency bonus."
        ),
        SubclassFeature(
            name="Wild Surge",
            level=3,
            description="Whenever you rage, roll on the Wild Magic table to produce random effects such as teleporting motes, spectral vines, or detonating bolts that linger for the rage's duration."
        ),
        SubclassFeature(
            name="Bolstering Magic",
            level=6,
            description="You can use an action to bolster a creature, either granting a bonus d3 to attack and ability checks for 10 minutes or restoring an expended spell slot of level equal to or less than half your proficiency bonus."
        ),
        SubclassFeature(
            name="Unstable Backlash",
            level=10,
            description="When you take damage or fail a save while raging, you can use a reaction to roll again on the Wild Magic table and immediately use the new effect, potentially changing your aura mid-battle."
        ),
        SubclassFeature(
            name="Controlled Surge",
            level=14,
            description="Whenever you roll on your Wild Magic table, you can roll twice and choose which effect manifests, exerting some control over the chaos."
        )
    ]
)

# ========== BARD SUBCLASSES ==========

COLLEGE_OF_LORE = Subclass(
    name="College of Lore",
    class_name="Bard",
    description="Bards of the College of Lore know something about most things, collecting bits of knowledge from sources as diverse as scholarly tomes and peasant tales.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Bonus Proficiencies",
            level=3,
            description="You gain proficiency with three skills of your choice."
        ),
        SubclassFeature(
            name="Cutting Words",
            level=3,
            description="You learn how to use your wit to distract, confuse, and otherwise sap the confidence and competence of others. When a creature that you can see within 60 feet of you makes an attack roll, an ability check, or a damage roll, you can use your reaction to expend one of your uses of Bardic Inspiration, rolling a Bardic Inspiration die and subtracting the number rolled from the creature's roll. You can choose to use this feature after the creature makes its roll, but before the DM determines whether the attack roll or ability check succeeds or fails, or before the creature deals its damage. The creature is immune if it can't hear you or if it's immune to being charmed."
        ),
        SubclassFeature(
            name="Additional Magical Secrets",
            level=6,
            description="You learn two spells of your choice from any class. A spell you choose must be of a level you can cast, as shown on the Bard table, or a cantrip. The chosen spells count as bard spells for you but don't count against the number of bard spells you know."
        ),
        SubclassFeature(
            name="Peerless Skill",
            level=14,
            description="When you make an ability check, you can expend one use of Bardic Inspiration. Roll a Bardic Inspiration die and add the number rolled to your ability check. You can choose to do so after you roll the die for the ability check, but before the DM tells you whether you succeed or fail."
        )
    ]
)

COLLEGE_OF_VALOR = Subclass(
    name="College of Valor",
    class_name="Bard",
    description="Bards of the College of Valor are daring skalds whose tales keep alive the memory of the great heroes of the past, and thereby inspire a new generation of heroes.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Bonus Proficiencies",
            level=3,
            description="You gain proficiency with medium armor, shields, and martial weapons."
        ),
        SubclassFeature(
            name="Combat Inspiration",
            level=3,
            description="You learn to inspire others in battle. A creature that has a Bardic Inspiration die from you can roll that die and add the number rolled to a weapon damage roll it just made. Alternatively, when an attack roll is made against the creature, it can use its reaction to roll the Bardic Inspiration die and add the number rolled to its AC against that attack, after seeing the roll but before knowing whether it hits or misses."
        ),
        SubclassFeature(
            name="Extra Attack",
            level=6,
            description="You can attack twice, instead of once, whenever you take the Attack action on your turn."
        ),
        SubclassFeature(
            name="Battle Magic",
            level=14,
            description="You have mastered the art of weaving spellcasting and weapon use into a single harmonious act. When you use your action to cast a bard spell, you can make one weapon attack as a bonus action."
        )
    ]
)

COLLEGE_OF_GLAMOUR = Subclass(
    name="College of Glamour",
    class_name="Bard",
    description="Glamour bards hail from the Feywild and wield otherworldly charisma to inspire adoration or obedience from all who witness their performances.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Mantle of Inspiration",
            level=3,
            description="As a bonus action you expend a Bardic Inspiration to grant temporary hit points and allow immediate movement without opportunity attacks to a number of creatures you can see."
        ),
        SubclassFeature(
            name="Enthralling Performance",
            level=3,
            description="After performing for at least 1 minute, you can charm and enthrall a number of humanoids, making them idolize you for 1 hour unless they succeed on a save."
        ),
        SubclassFeature(
            name="Mantle of Majesty",
            level=6,
            description="You can cloak yourself in fey magic for 1 minute, casting command as a bonus action each turn without expending spell slots, once per long rest."
        ),
        SubclassFeature(
            name="Unbreakable Majesty",
            level=14,
            description="As a bonus action you assume a magically majestic presence for 1 minute, imposing disadvantage on attacks against you and being able to force saves on creatures that target you."
        )
    ]
)

COLLEGE_OF_SWORDS = Subclass(
    name="College of Swords",
    class_name="Bard",
    description="Bards of the College of Swords have mastered blade and performance alike, dancing through battle with whirling steel and flourished magic.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Bonus Proficiencies",
            level=3,
            description="You gain proficiency with medium armor and scimitars, and you can use a weapon as a spellcasting focus for bard spells."
        ),
        SubclassFeature(
            name="Fighting Style",
            level=3,
            description="You adopt a Fighting Style from Dueling or Two-Weapon Fighting, reflecting your martial training."
        ),
        SubclassFeature(
            name="Blade Flourish",
            level=3,
            description="Whenever you take the Attack action you can expend a Bardic Inspiration die to perform a defensive, slashing, or mobile flourish that grants additional benefits."
        ),
        SubclassFeature(
            name="Extra Attack",
            level=6,
            description="You can attack twice, instead of once, whenever you take the Attack action on your turn."
        ),
        SubclassFeature(
            name="Master's Flourish",
            level=14,
            description="Your blade flourishes now use a d6 instead of expending Bardic Inspiration, letting you unleash them each turn."
        )
    ]
)

COLLEGE_OF_WHISPERS = Subclass(
    name="College of Whispers",
    class_name="Bard",
    description="Whispers bards unravel secrets and sow paranoia, wielding psychic blades and stolen identities to manipulate from the shadows.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Psychic Blades",
            level=3,
            description="When you hit a creature with a weapon attack, you can expend a Bardic Inspiration to deal extra psychic damage, scaling with your Bardic Inspiration die."
        ),
        SubclassFeature(
            name="Words of Terror",
            level=3,
            description="Over 1 minute of conversation you can instill paranoia in a humanoid, causing it to become frightened of a creature of your choice for 1 hour if it fails a save."
        ),
        SubclassFeature(
            name="Mantle of Whispers",
            level=6,
            description="When a humanoid dies within 30 feet, you can capture its shadow to disguise yourself as that person for 1 hour, gaining access to its memories for social checks."
        ),
        SubclassFeature(
            name="Shadow Lore",
            level=14,
            description="As an action you whisper dark knowledge to magically frighten a creature, charming it for 8 hours if it fails a Wisdom save and making it regard you or a target as a trusted friend."
        )
    ]
)

# ========== CLERIC SUBCLASSES ==========

LIFE_DOMAIN = Subclass(
    name="Life Domain",
    class_name="Cleric",
    description="The Life domain focuses on the vibrant positive energy—one of the fundamental forces of the universe—that sustains all life. The gods of life promote vitality and health through healing the sick and wounded, caring for those in need, and driving away the forces of death and undeath.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Bonus Proficiency",
            level=1,
            description="You gain proficiency with heavy armor."
        ),
        SubclassFeature(
            name="Disciple of Life",
            level=1,
            description="Your healing spells are more effective. Whenever you use a spell of 1st level or higher to restore hit points to a creature, the creature regains additional hit points equal to 2 + the spell's level."
        ),
        SubclassFeature(
            name="Channel Divinity: Preserve Life",
            level=2,
            description="You can use your Channel Divinity to heal the badly injured. As an action, you present your holy symbol and evoke healing energy that can restore a number of hit points equal to five times your cleric level. Choose any creatures within 30 feet of you, and divide those hit points among them. This feature can restore a creature to no more than half of its hit point maximum. You can't use this feature on an undead or a construct."
        ),
        SubclassFeature(
            name="Blessed Healer",
            level=6,
            description="The healing spells you cast on others heal you as well. When you cast a spell of 1st level or higher that restores hit points to a creature other than you, you regain hit points equal to 2 + the spell's level."
        ),
        SubclassFeature(
            name="Divine Strike",
            level=8,
            description="You gain the ability to infuse your weapon strikes with divine energy. Once on each of your turns when you hit a creature with a weapon attack, you can cause the attack to deal an extra 1d8 radiant damage to the target. When you reach 14th level, the extra damage increases to 2d8."
        ),
        SubclassFeature(
            name="Supreme Healing",
            level=17,
            description="When you would normally roll one or more dice to restore hit points with a spell, you instead use the highest number possible for each die. For example, instead of restoring 2d6 hit points to a creature, you restore 12."
        )
    ]
)

WAR_DOMAIN = Subclass(
    name="War Domain",
    class_name="Cleric",
    description="War has many manifestations. It can make heroes of ordinary people. It can be desperate and horrific, with acts of cruelty and cowardice eclipsing instances of excellence and courage. In either case, the gods of war watch over warriors and reward them for their great deeds.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Bonus Proficiencies",
            level=1,
            description="You gain proficiency with martial weapons and heavy armor."
        ),
        SubclassFeature(
            name="War Priest",
            level=1,
            description="Your god delivers bolts of inspiration to you while you are engaged in battle. When you use the Attack action, you can make one weapon attack as a bonus action. You can use this feature a number of times equal to your Wisdom modifier (a minimum of once). You regain all expended uses when you finish a long rest."
        ),
        SubclassFeature(
            name="Channel Divinity: Guided Strike",
            level=2,
            description="You can use your Channel Divinity to strike with supernatural accuracy. When you make an attack roll, you can use your Channel Divinity to gain a +10 bonus to the roll. You make this choice after you see the roll, but before the DM says whether the attack hits or misses."
        ),
        SubclassFeature(
            name="Channel Divinity: War God's Blessing",
            level=6,
            description="When a creature within 30 feet of you makes an attack roll, you can use your reaction to grant that creature a +10 bonus to the roll, using your Channel Divinity. You make this choice after you see the roll, but before the DM says whether the attack hits or misses."
        ),
        SubclassFeature(
            name="Divine Strike",
            level=8,
            description="You gain the ability to infuse your weapon strikes with divine energy. Once on each of your turns when you hit a creature with a weapon attack, you can cause the attack to deal an extra 1d8 damage of the same type dealt by the weapon to the target. When you reach 14th level, the extra damage increases to 2d8."
        ),
        SubclassFeature(
            name="Avatar of Battle",
            level=17,
            description="You gain resistance to bludgeoning, piercing, and slashing damage from nonmagical weapons."
        )
    ]
)

# Dicionário de subclasses por classe
BARBARIAN_SUBCLASSES = {
    "Path of the Berserker": BERSERKER,
    "Path of the Totem Warrior": TOTEM_WARRIOR,
    "Path of the Ancestral Guardian": PATH_OF_THE_ANCESTRAL_GUARDIAN,
    "Path of the Storm Herald": PATH_OF_THE_STORM_HERALD,
    "Path of the Zealot": PATH_OF_THE_ZEALOT,
    "Path of the Beast": PATH_OF_THE_BEAST,
    "Path of Wild Magic": PATH_OF_WILD_MAGIC,
}

BARD_SUBCLASSES = {
    "College of Lore": COLLEGE_OF_LORE,
    "College of Valor": COLLEGE_OF_VALOR,
    "College of Glamour": COLLEGE_OF_GLAMOUR,
    "College of Swords": COLLEGE_OF_SWORDS,
    "College of Whispers": COLLEGE_OF_WHISPERS,
    "College of Creation": COLLEGE_OF_CREATION,
    "College of Eloquence": COLLEGE_OF_ELOQUENCE,
}

CLERIC_SUBCLASSES = {
    "Knowledge Domain": KNOWLEDGE_DOMAIN,
    "Life Domain": LIFE_DOMAIN,
    "Light Domain": LIGHT_DOMAIN,
    "Nature Domain": NATURE_DOMAIN,
    "Tempest Domain": TEMPEST_DOMAIN,
    "Trickery Domain": TRICKERY_DOMAIN,
    "War Domain": WAR_DOMAIN,
    "Forge Domain": FORGE_DOMAIN,
    "Grave Domain": GRAVE_DOMAIN,
    "Peace Domain": PEACE_DOMAIN,
    "Twilight Domain": TWILIGHT_DOMAIN,
}

# ========== DRUID SUBCLASSES ==========

CIRCLE_OF_THE_LAND = Subclass(
    name="Circle of the Land",
    class_name="Druid",
    description="The Circle of the Land is made up of mystics and sages who safeguard ancient knowledge and rites through a vast oral tradition. These druids meet within sacred circles of trees or standing stones to whisper primal secrets in Druidic.",
    selection_level=2,
    features=[
        SubclassFeature(
            name="Bonus Cantrip",
            level=2,
            description="You learn one additional druid cantrip of your choice."
        ),
        SubclassFeature(
            name="Natural Recovery",
            level=2,
            description="You can regain some of your magical energy by sitting in meditation and communing with nature. During a short rest, you choose expended spell slots to recover. The spell slots can have a combined level that is equal to or less than half your druid level (rounded up), and none of the slots can be 6th level or higher. You can't use this feature again until you finish a long rest."
        ),
        SubclassFeature(
            name="Circle Spells",
            level=3,
            description="Your mystical connection to the land infuses you with the ability to cast certain spells. You gain access to circle spells connected to the land where you became a druid. Choose that land—arctic, coast, desert, forest, grassland, mountain, swamp, or Underdark—and consult the associated list of spells. Once you gain access to a circle spell, you always have it prepared, and it doesn't count against the number of spells you can prepare each day."
        ),
        SubclassFeature(
            name="Land's Stride",
            level=6,
            description="Moving through nonmagical difficult terrain costs you no extra movement. You can also pass through nonmagical plants without being slowed by them and without taking damage from them if they have thorns, spines, or a similar hazard. In addition, you have advantage on saving throws against plants that are magically created or manipulated to impede movement."
        ),
        SubclassFeature(
            name="Nature's Ward",
            level=10,
            description="You can't be charmed or frightened by elementals or fey, and you are immune to poison and disease."
        ),
        SubclassFeature(
            name="Nature's Sanctuary",
            level=14,
            description="Creatures of the natural world sense your connection to nature and become hesitant to attack you. When a beast or plant creature attacks you, that creature must make a Wisdom saving throw against your druid spell save DC. On a failed save, the creature must choose a different target, or the attack automatically misses. On a successful save, the creature is immune to this effect for 24 hours."
        )
    ]
)

CIRCLE_OF_THE_MOON = Subclass(
    name="Circle of the Moon",
    class_name="Druid",
    description="Druids of the Circle of the Moon are fierce guardians of the wilds. Their order gathers under the full moon to share news and trade warnings. They haunt the deepest parts of the wilderness, where they might go for weeks on end before crossing paths with another humanoid creature, let alone another druid.",
    selection_level=2,
    features=[
        SubclassFeature(
            name="Combat Wild Shape",
            level=2,
            description="You gain the ability to use Wild Shape on your turn as a bonus action, rather than as an action. Additionally, while you are transformed by Wild Shape, you can use a bonus action to expend one spell slot to regain 1d8 hit points per level of the spell slot expended."
        ),
        SubclassFeature(
            name="Circle Forms",
            level=2,
            description="The rites of your circle grant you the ability to transform into more dangerous animal forms. You can transform into a beast with a challenge rating as high as 1 (you ignore the Max. CR column of the Beast Shapes table, but must abide by the other limitations there). Starting at 6th level, you can transform into a beast with a challenge rating as high as your druid level divided by 3, rounded down."
        ),
        SubclassFeature(
            name="Primal Strike",
            level=6,
            description="Your attacks in beast form count as magical for the purpose of overcoming resistance and immunity to nonmagical attacks and damage."
        ),
        SubclassFeature(
            name="Elemental Wild Shape",
            level=10,
            description="You can expend two uses of Wild Shape at the same time to transform into an air elemental, an earth elemental, a fire elemental, or a water elemental."
        ),
        SubclassFeature(
            name="Thousand Forms",
            level=14,
            description="You have learned to use magic to alter your physical form in more subtle ways. You can cast the Alter Self spell at will."
        )
    ]
)

CIRCLE_OF_DREAMS = Subclass(
    name="Circle of Dreams",
    class_name="Druid",
    description="Dreams druids draw power from the Feywild, soothing allies and weaving restorative magic inspired by the Summer Court.",
    selection_level=2,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Balm of the Summer Court",
            level=2,
            description="You have a pool of fey energy represented by d6s equal to twice your druid level. As a bonus action you can heal a creature within 120 feet, spending up to half your druid level dice to restore hit points and grant temporary hit points."
        ),
        SubclassFeature(
            name="Hearth of Moonlight and Shadow",
            level=6,
            description="During a short or long rest you can create a 30-foot sphere ward that grants +5 to Stealth and Perception checks for resting creatures and blocks light from escaping."
        ),
        SubclassFeature(
            name="Hidden Paths",
            level=10,
            description="You can magically teleport up to 60 feet as a bonus action, and you can teleport an ally you touch up to 30 feet as an action, multiple times per long rest equal to your Wisdom modifier."
        ),
        SubclassFeature(
            name="Walker in Dreams",
            level=14,
            description="You can cast Dream, Scrying, or Teleportation Circle (to the last place you took a long rest on the same plane) without expending spell slots once per long rest."
        )
    ]
)

CIRCLE_OF_THE_SHEPHERD = Subclass(
    name="Circle of the Shepherd",
    class_name="Druid",
    description="Shepherd druids protect beasts and fey, summoning spiritual guardians that bolster allies and commanded creatures.",
    selection_level=2,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Speech of the Woods",
            level=2,
            description="You learn Sylvan and can communicate with beasts and many fey, understanding them regardless of language."
        ),
        SubclassFeature(
            name="Spirit Totem",
            level=2,
            description="As a bonus action you summon a bear, hawk, or unicorn spirit for 1 minute that grants buffs such as temporary hit points, advantage on Perception checks, or enhanced healing within its aura."
        ),
        SubclassFeature(
            name="Mighty Summoner",
            level=6,
            description="Creatures you conjure gain 2 extra hit points per Hit Die and their natural attacks count as magical for overcoming resistances."
        ),
        SubclassFeature(
            name="Guardian Spirit",
            level=10,
            description="When a creature you summoned ends its turn in your Spirit Totem aura, it regains hit points equal to half your druid level."
        ),
        SubclassFeature(
            name="Faithful Summons",
            level=14,
            description="When you are reduced to 0 hit points or incapacitated unwillingly, you can automatically cast Conjure Animals (as if using an 8th-level slot) to summon guardian beasts without concentration."
        )
    ]
)

DRUID_SUBCLASSES = {
    "Circle of the Land": CIRCLE_OF_THE_LAND,
    "Circle of the Moon": CIRCLE_OF_THE_MOON,
    "Circle of Dreams": CIRCLE_OF_DREAMS,
    "Circle of the Shepherd": CIRCLE_OF_THE_SHEPHERD,
    "Circle of Spores": CIRCLE_OF_SPORES,
    "Circle of Stars": CIRCLE_OF_STARS,
    "Circle of Wildfire": CIRCLE_OF_WILDFIRE,
}

# ========== FIGHTER SUBCLASSES ==========

CHAMPION = Subclass(
    name="Champion",
    class_name="Fighter",
    description="The archetypal Champion focuses on the development of raw physical power honed to deadly perfection. Those who model themselves on this archetype combine rigorous training with physical excellence to deal devastating blows.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Improved Critical",
            level=3,
            description="Your weapon attacks score a critical hit on a roll of 19 or 20."
        ),
        SubclassFeature(
            name="Remarkable Athlete",
            level=7,
            description="You can add half your proficiency bonus (rounded up) to any Strength, Dexterity, or Constitution check you make that doesn't already use your proficiency bonus. In addition, when you make a running long jump, the distance you can cover increases by a number of feet equal to your Strength modifier."
        ),
        SubclassFeature(
            name="Additional Fighting Style",
            level=10,
            description="You can choose a second option from the Fighting Style class feature."
        ),
        SubclassFeature(
            name="Superior Critical",
            level=15,
            description="Your weapon attacks score a critical hit on a roll of 18-20."
        ),
        SubclassFeature(
            name="Survivor",
            level=18,
            description="You attain the pinnacle of resilience in battle. At the start of each of your turns, you regain hit points equal to 5 + your Constitution modifier if you have no more than half of your hit points left. You don't gain this benefit if you have 0 hit points."
        )
    ]
)

BATTLE_MASTER = Subclass(
    name="Battle Master",
    class_name="Fighter",
    description="Those who emulate the archetypal Battle Master employ martial techniques passed down through generations. To a Battle Master, combat is an academic field, sometimes including subjects beyond battle such as weaponsmithing and calligraphy.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Combat Superiority",
            level=3,
            description="You learn maneuvers that are fueled by special dice called superiority dice. You learn three maneuvers of your choice. You have four superiority dice, which are d8s. A superiority die is expended when you use it. You regain all of your expended superiority dice when you finish a short or long rest. You gain another superiority die at 7th level and one more at 15th level."
        ),
        SubclassFeature(
            name="Student of War",
            level=3,
            description="You gain proficiency with one type of artisan's tools of your choice."
        ),
        SubclassFeature(
            name="Know Your Enemy",
            level=7,
            description="If you spend at least 1 minute observing or interacting with another creature outside combat, you can learn certain information about its capabilities compared to your own. The DM tells you if the creature is your equal, superior, or inferior in regard to two of the following characteristics of your choice: Strength score, Dexterity score, Constitution score, Armor Class, Current hit points, Total class levels (if any), Fighter class levels (if any)."
        ),
        SubclassFeature(
            name="Improved Combat Superiority",
            level=10,
            description="Your superiority dice turn into d10s. At 18th level, they turn into d12s."
        ),
        SubclassFeature(
            name="Relentless",
            level=15,
            description="When you roll initiative and have no superiority dice remaining, you regain 1 superiority die."
        )
    ]
)

ELDRITCH_KNIGHT = Subclass(
    name="Eldritch Knight",
    class_name="Fighter",
    description="The archetypal Eldritch Knight combines the martial mastery common to all fighters with a careful study of magic. Eldritch Knights use magical techniques similar to those practiced by wizards.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Spellcasting",
            level=3,
            description="You augment your martial prowess with the ability to cast spells. You learn two cantrips of your choice from the wizard spell list. You learn an additional wizard cantrip of your choice at 10th level. The Eldritch Knight Spellcasting table shows how many spell slots you have to cast your spells of 1st level and higher."
        ),
        SubclassFeature(
            name="Weapon Bond",
            level=3,
            description="You learn a ritual that creates a magical bond between yourself and one weapon. You perform the ritual over the course of 1 hour, which can be done during a short rest. The weapon must be within your reach throughout the ritual. Once you have bonded a weapon to yourself, you can't be disarmed of that weapon unless you are incapacitated. If it is on the same plane of existence, you can summon that weapon as a bonus action, causing it to teleport instantly to your hand."
        ),
        SubclassFeature(
            name="War Magic",
            level=7,
            description="When you use your action to cast a cantrip, you can make one weapon attack as a bonus action."
        ),
        SubclassFeature(
            name="Eldritch Strike",
            level=10,
            description="You learn how to make your weapon strikes undercut a creature's resistance to your spells. When you hit a creature with a weapon attack, that creature has disadvantage on the next saving throw it makes against a spell you cast before the end of your next turn."
        ),
        SubclassFeature(
            name="Arcane Charge",
            level=15,
            description="You gain the ability to teleport up to 30 feet to an unoccupied space you can see when you use your Action Surge. You can teleport before or after the additional action."
        ),
        SubclassFeature(
            name="Improved War Magic",
            level=18,
            description="When you use your action to cast a spell, you can make one weapon attack as a bonus action."
        )
    ]
)

ARCANE_ARCHER = Subclass(
    name="Arcane Archer",
    class_name="Fighter",
    description="Arcane Archers weave magic into arrow shots, bending trajectories and imbuing volleys with specialized arcane effects.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Arcane Archer Lore",
            level=3,
            description="You gain proficiency in either Arcana or Nature and learn the Prestidigitation or Druidcraft cantrip as you study elven arrowcraft."
        ),
        SubclassFeature(
            name="Arcane Shot",
            level=3,
            description="You learn magical shot options and can infuse arrows twice per short rest to impose effects such as banishing, ensnaring, or piercing defenses (save DC = 8 + proficiency bonus + Intelligence modifier)."
        ),
        SubclassFeature(
            name="Magic Arrow",
            level=7,
            description="Your arrows count as magical for overcoming resistance and immunity to nonmagical attacks."
        ),
        SubclassFeature(
            name="Curving Shot",
            level=7,
            description="When you miss with a magic arrow attack you can use a bonus action to reroll the attack against a different target within 60 feet of the original."
        ),
        SubclassFeature(
            name="Ever-Ready Shot",
            level=15,
            description="When you roll initiative and have no uses of Arcane Shot remaining, you regain one use."
        )
    ]
)

CAVALIER = Subclass(
    name="Cavalier",
    class_name="Fighter",
    description="Cavaliers are battlefield guardians who excel at mounted combat, locking down foes and defending allies with unyielding presence.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Bonus Proficiencies",
            level=3,
            description="You gain proficiency in one of the following skills of your choice: Animal Handling, History, Insight, Performance, or Persuasion. You also gain proficiency with one language or with smith's tools."
        ),
        SubclassFeature(
            name="Born to the Saddle",
            level=3,
            description="You have advantage on saving throws made to avoid falling off your mount, mounting or dismounting costs only 5 feet of movement, and you land on your feet if you fall while conscious."
        ),
        SubclassFeature(
            name="Unwavering Mark",
            level=3,
            description="When you hit a creature with a melee attack, you can mark it until the end of your next turn. Marked foes have disadvantage on attacks that don't include you, and if they hit an ally you can make a special bonus action attack dealing extra damage equal to half your fighter level."
        ),
        SubclassFeature(
            name="Warding Maneuver",
            level=7,
            description="As a reaction when you or a creature within 5 feet is hit, you can roll a d8 and add the number to AC. If the attack still hits, the target has resistance to the damage. Uses per long rest equal to your Constitution modifier."
        ),
        SubclassFeature(
            name="Hold the Line",
            level=10,
            description="Creatures you hit with opportunity attacks have their speed reduced to 0 for the rest of the turn, and you can make opportunity attacks against creatures that enter your reach."
        ),
        SubclassFeature(
            name="Ferocious Charger",
            level=15,
            description="If you move at least 10 feet toward a target before hitting it with a melee attack, it must succeed on a Strength saving throw or be knocked prone."
        ),
        SubclassFeature(
            name="Vigilant Defender",
            level=18,
            description="You can take a number of reactions each round equal to your proficiency bonus, though only one per turn, letting you defend multiple allies."
        )
    ]
)

SAMURAI = Subclass(
    name="Samurai",
    class_name="Fighter",
    description="Samurai steel their spirits with unwavering resolve, turning fighting spirit into bursts of accuracy, durability, and relentless assaults.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Bonus Proficiency",
            level=3,
            description="You gain proficiency in History, Insight, Performance, or Persuasion, or you can learn one language of your choice."
        ),
        SubclassFeature(
            name="Fighting Spirit",
            level=3,
            description="As a bonus action you can give yourself advantage on weapon attacks until the end of the current turn and gain temporary hit points equal to your fighter level. You can use this feature a number of times equal to your proficiency bonus per long rest."
        ),
        SubclassFeature(
            name="Elegant Courtier",
            level=7,
            description="You add your Wisdom modifier to Charisma (Persuasion) checks and gain proficiency in Wisdom saving throws if you don't already have it."
        ),
        SubclassFeature(
            name="Tireless Spirit",
            level=10,
            description="When you roll initiative and have no Fighting Spirit uses remaining, you regain one use."
        ),
        SubclassFeature(
            name="Rapid Strike",
            level=15,
            description="Once per turn when you have advantage on an attack roll, you can forgo that advantage to make an additional weapon attack as part of the same action."
        ),
        SubclassFeature(
            name="Strength Before Death",
            level=18,
            description="When damage would reduce you to 0 hit points, you can use your reaction to delay the effect, immediately taking an extra turn."
        )
    ]
)

FIGHTER_SUBCLASSES = {
    "Champion": CHAMPION,
    "Battle Master": BATTLE_MASTER,
    "Eldritch Knight": ELDRITCH_KNIGHT,
    "Arcane Archer": ARCANE_ARCHER,
    "Cavalier": CAVALIER,
    "Samurai": SAMURAI,
    "Psi Warrior": PSI_WARRIOR,
    "Rune Knight": RUNE_KNIGHT,
}

# ========== MONK SUBCLASSES ==========

WAY_OF_THE_OPEN_HAND = Subclass(
    name="Way of the Open Hand",
    class_name="Monk",
    description="Monks of the Way of the Open Hand are the ultimate masters of martial arts combat, whether armed or unarmed. They learn techniques to push and trip their opponents, manipulate ki to heal damage to their bodies, and practice advanced meditation that can protect them from harm.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Open Hand Technique",
            level=3,
            description="Whenever you hit a creature with one of the attacks granted by your Flurry of Blows, you can impose one of the following effects: knock it prone, push it up to 15 feet away, or prevent it from taking reactions until the end of your next turn."
        ),
        SubclassFeature(
            name="Wholeness of Body",
            level=6,
            description="You gain the ability to heal yourself. As an action, you can regain hit points equal to three times your monk level once per long rest."
        ),
        SubclassFeature(
            name="Tranquility",
            level=11,
            description="You can enter a meditation at the end of a long rest to gain the effect of a Sanctuary spell that lasts until the start of your next long rest (ending early as normal)."
        ),
        SubclassFeature(
            name="Quivering Palm",
            level=17,
            description="You can spend 3 ki points to set up lethal vibrations in a creature you hit with an unarmed strike. As an action later, you can force that creature to make a Constitution save, reducing it to 0 hit points on a failure or dealing 10d10 necrotic damage on a success."
        )
    ]
)

WAY_OF_SHADOW = Subclass(
    name="Way of Shadow",
    class_name="Monk",
    description="Monks of the Way of Shadow follow a tradition that values stealth and subterfuge. These monks might be called ninjas or shadowdancers, and they serve as spies and assassins. Sometimes the members of a ninja monastery are family members, forming a clan sworn to secrecy about their arts and missions.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Shadow Arts",
            level=3,
            description="You can use your ki to duplicate the effects of certain spells. As an action, you can spend 2 ki points to cast Darkness, Darkvision, Pass without Trace, or Silence, without providing material components. Additionally, you gain the Minor Illusion cantrip if you don't already know it."
        ),
        SubclassFeature(
            name="Shadow Step",
            level=6,
            description="You gain the ability to step from one shadow into another. When you are in dim light or darkness, as a bonus action you can teleport up to 60 feet to an unoccupied space you can see that is also in dim light or darkness. You then have advantage on the first melee attack you make before the end of the turn."
        ),
        SubclassFeature(
            name="Cloak of Shadows",
            level=11,
            description="You have learned to become one with the shadows. When you are in an area of dim light or darkness, you can use your action to become invisible. You remain invisible until you make an attack, cast a spell, or are in an area of bright light."
        ),
        SubclassFeature(
            name="Opportunist",
            level=17,
            description="You can exploit a creature's momentary distraction when it is hit by an attack. Whenever a creature within 5 feet of you is hit by an attack made by a creature other than you, you can use your reaction to make a melee attack against that creature."
        )
    ]
)

WAY_OF_THE_FOUR_ELEMENTS = Subclass(
    name="Way of the Four Elements",
    class_name="Monk",
    description="You follow a monastic tradition that teaches you to harness the elements. When you focus your ki, you can align yourself with the forces of creation and bend the four elements to your will, using them as an extension of your body.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Disciple of the Elements",
            level=3,
            description="You learn magical disciplines that harness the power of the four elements. You know the Elemental Attunement discipline and one other elemental discipline of your choice. You learn one additional elemental discipline of your choice at 6th, 11th, and 17th level.\n\nWhenever you learn a new elemental discipline, you can also replace one elemental discipline that you already know with a different discipline.\n\nSome elemental disciplines require you to spend ki points when you use them. You must spend the ki points when you use the discipline. The maximum number of ki points you can spend to cast a spell in this way (including its base ki point cost and any additional ki points you spend to increase its level) is determined by your monk level."
        ),
        SubclassFeature(
            name="Additional Elemental Discipline",
            level=6,
            description="You learn one additional elemental discipline of your choice. You can also replace one elemental discipline that you already know with a different discipline."
        ),
        SubclassFeature(
            name="Additional Elemental Discipline",
            level=11,
            description="You learn one additional elemental discipline of your choice. You can also replace one elemental discipline that you already know with a different discipline."
        ),
        SubclassFeature(
            name="Additional Elemental Discipline",
            level=17,
            description="You learn one additional elemental discipline of your choice. You can also replace one elemental discipline that you already know with a different discipline."
        )
    ]
)

WAY_OF_THE_DRUNKEN_MASTER = Subclass(
    name="Way of the Drunken Master",
    class_name="Monk",
    description="Drunken Masters channel erratic movements into baffling defense, staggering through battle while striking with deceptive precision.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Bonus Proficiencies",
            level=3,
            description="You gain proficiency in Performance and brewer's supplies, adopting the theatrics and rituals of intoxicated fighting." 
        ),
        SubclassFeature(
            name="Drunken Technique",
            level=3,
            description="Whenever you use Flurry of Blows you gain the benefit of Disengage and your walking speed increases by 10 feet until the end of the turn as you weave unpredictably."
        ),
        SubclassFeature(
            name="Tipsy Sway",
            level=6,
            description="You can stand from prone by expending only 5 feet of movement (Leap to Your Feet) and when a melee attack misses you, you can spend 1 ki to redirect it against another creature within 5 feet of you (Redirect Attack)."
        ),
        SubclassFeature(
            name="Drunkard's Luck",
            level=11,
            description="When you make a roll with disadvantage, you can spend 2 ki points to cancel the disadvantage for that roll, trusting improvised luck."
        ),
        SubclassFeature(
            name="Intoxicated Frenzy",
            level=17,
            description="When you use Flurry of Blows you can make up to three additional attacks (each against a different creature) beyond the normal two, unleashing a whirlwind of staggering strikes."
        )
    ]
)

WAY_OF_THE_KENSEI = Subclass(
    name="Way of the Kensei",
    class_name="Monk",
    description="Kensei monks hone body and blade together, treating chosen weapons as extensions of their ki-forged discipline.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Path of the Kensei",
            level=3,
            description="You designate two simple or martial weapons as kensei weapons (more at later levels), gain Agile Parry when you make an unarmed strike while wielding a kensei melee weapon, gain Kensei's Shot to add 1d4 to ranged attacks as a bonus action, and learn calligraphy or painter's supplies (Way of the Brush)."
        ),
        SubclassFeature(
            name="One with the Blade",
            level=6,
            description="Your kensei weapons count as magical for overcoming resistance, and you can spend 1 ki to deal an extra 1d4 damage on a hit with a kensei weapon (Deft Strike)."
        ),
        SubclassFeature(
            name="Sharpen the Blade",
            level=11,
            description="As a bonus action you can spend up to 3 ki points to grant a kensei weapon a +1 per ki (maximum +3) bonus to attack and damage rolls for 1 minute."
        ),
        SubclassFeature(
            name="Unerring Accuracy",
            level=17,
            description="Once on each of your turns when you miss with a monk weapon or kensei weapon attack, you can reroll the attack, ensuring your practiced strikes rarely fail."
        )
    ]
)

WAY_OF_THE_SUN_SOUL = Subclass(
    name="Way of the Sun Soul",
    class_name="Monk",
    description="Sun Soul monks project radiant ki as bolts and bursts of light, burning foes with incandescent martial arts.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Radiant Sun Bolt",
            level=3,
            description="You can hurl radiant bolts with a range of 30 feet as part of the Attack action (or as extra attacks when using Flurry of Blows). The bolts use Dexterity for attack and damage rolls and deal radiant damage."
        ),
        SubclassFeature(
            name="Searing Arc Strike",
            level=6,
            description="Immediately after taking the Attack action you can spend ki to cast Burning Hands as a bonus action, empowering the spell with additional ki to raise its level."
        ),
        SubclassFeature(
            name="Searing Sunburst",
            level=11,
            description="You can create a 20-foot radius ball of radiant light at up to 150 feet; creatures failing a Constitution save take radiant damage (you can spend ki to increase the damage)."
        ),
        SubclassFeature(
            name="Sun Shield",
            level=17,
            description="You shed bright light in a 30-foot radius and dim light for the same distance, and when a creature hits you you can use your reaction to deal radiant damage equal to 5 + your Wisdom modifier if it is within 30 feet."
        )
    ]
)

MONK_SUBCLASSES = {
    "Way of the Open Hand": WAY_OF_THE_OPEN_HAND,
    "Way of Shadow": WAY_OF_SHADOW,
    "Way of the Four Elements": WAY_OF_THE_FOUR_ELEMENTS,
    "Way of the Drunken Master": WAY_OF_THE_DRUNKEN_MASTER,
    "Way of the Kensei": WAY_OF_THE_KENSEI,
    "Way of the Sun Soul": WAY_OF_THE_SUN_SOUL,
    "Way of Mercy": WAY_OF_MERCY,
    "Way of the Astral Self": WAY_OF_THE_ASTRAL_SELF,
}

# ========== PALADIN SUBCLASSES ==========

OATH_OF_DEVOTION = Subclass(
    name="Oath of Devotion",
    class_name="Paladin",
    description="The Oath of Devotion binds a paladin to the loftiest ideals of justice, virtue, and order. Sometimes called cavaliers, white knights, or holy warriors, these paladins meet the ideal of the knight in shining armor, acting with honor in pursuit of justice and the greater good.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Oath Spells",
            level=3,
            description="You gain oath spells at the paladin levels listed.\n3rd: Protection from Evil and Good, Sanctuary\n5th: Lesser Restoration, Zone of Truth\n9th: Beacon of Hope, Dispel Magic\n13th: Freedom of Movement, Guardian of Faith\n17th: Commune, Flame Strike"
        ),
        SubclassFeature(
            name="Channel Divinity: Sacred Weapon",
            level=3,
            description="As an action, you can imbue one weapon that you are holding with positive energy, using your Channel Divinity. For 1 minute, you add your Charisma modifier to attack rolls made with that weapon (with a minimum bonus of +1). The weapon also emits bright light in a 20-foot radius and dim light 20 feet beyond that. If the weapon is not already magical, it becomes magical for the duration. You can end this effect on your turn as part of any other action. If you are no longer holding or carrying this weapon, or if you fall unconscious, this effect ends."
        ),
        SubclassFeature(
            name="Channel Divinity: Turn the Unholy",
            level=3,
            description="As an action, you present your holy symbol and speak a prayer censuring fiends and undead, using your Channel Divinity. Each fiend or undead that can see or hear you within 30 feet of you must make a Wisdom saving throw. If the creature fails its saving throw, it is turned for 1 minute or until it takes damage. A turned creature must spend its turns trying to move as far away from you as it can, and it can't willingly move to a space within 30 feet of you. It also can't take reactions. For its action, it can use only the Dash action or try to escape from an effect that prevents it from moving. If there's nowhere to move, the creature can use the Dodge action."
        ),
        SubclassFeature(
            name="Aura of Devotion",
            level=7,
            description="You and friendly creatures within 10 feet of you can't be charmed while you are conscious. At 18th level, the range of this aura increases to 30 feet."
        ),
        SubclassFeature(
            name="Purity of Spirit",
            level=15,
            description="You are always under the effects of a Protection from Evil and Good spell."
        ),
        SubclassFeature(
            name="Holy Nimbus",
            level=20,
            description="As an action, you can emanate an aura of sunlight. For 1 minute, bright light shines from you in a 30-foot radius, and dim light shines 30 feet beyond that. Whenever an enemy creature starts its turn in the bright light, the creature takes 10 radiant damage. In addition, for the duration, you have advantage on saving throws against spells cast by fiends or undead. Once you use this feature, you can't use it again until you finish a long rest."
        )
    ]
)

OATH_OF_THE_ANCIENTS = Subclass(
    name="Oath of the Ancients",
    class_name="Paladin",
    description="The Oath of the Ancients is as old as the race of elves and the rituals of the druids. Sometimes called fey knights, green knights, or horned knights, paladins who swear this oath cast their lot with the side of the light in the cosmic struggle against darkness because they love the beautiful and life-giving things of the world.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Oath Spells",
            level=3,
            description="You gain oath spells at the paladin levels listed.\n3rd: Ensnaring Strike, Speak with Animals\n5th: Moonbeam, Misty Step\n9th: Plant Growth, Protection from Energy\n13th: Ice Storm, Stoneskin\n17th: Commune with Nature, Tree Stride"
        ),
        SubclassFeature(
            name="Channel Divinity: Nature's Wrath",
            level=3,
            description="You can use your Channel Divinity to invoke primeval forces to ensnare a foe. As an action, you can cause spectral vines to spring up and reach for a creature within 10 feet of you that you can see. The creature must succeed on a Strength or Dexterity saving throw (its choice) or be restrained. While restrained by the vines, the creature repeats the saving throw at the end of each of its turns. On a success, it frees itself and the vines vanish."
        ),
        SubclassFeature(
            name="Channel Divinity: Turn the Faithless",
            level=3,
            description="You can use your Channel Divinity to utter ancient words that are painful for fey and fiends to hear. As an action, you present your holy symbol, and each fey or fiend within 30 feet of you that can hear you must make a Wisdom saving throw. On a failed save, the creature is turned for 1 minute or until it takes damage."
        ),
        SubclassFeature(
            name="Aura of Warding",
            level=7,
            description="Ancient magic lies so heavily upon you that it forms an eldritch ward. You and friendly creatures within 10 feet of you have resistance to damage from spells. At 18th level, the range of this aura increases to 30 feet."
        ),
        SubclassFeature(
            name="Undying Sentinel",
            level=15,
            description="When you are reduced to 0 hit points and are not killed outright, you can choose to drop to 1 hit point instead. Once you use this ability, you can't use it again until you finish a long rest. Additionally, you suffer none of the drawbacks of old age, and you can't be aged magically."
        ),
        SubclassFeature(
            name="Elder Champion",
            level=20,
            description="You can assume the form of an ancient force of nature, taking on an appearance you choose. For example, your skin might turn green or take on a bark-like texture, your hair might become leafy or moss-like, or you might sprout antlers or a lion-like mane. Using your action, you undergo a transformation. For 1 minute, you gain the following benefits:\n• At the start of each of your turns, you regain 10 hit points.\n• Whenever you cast a paladin spell that has a casting time of 1 action, you can cast it using a bonus action instead.\n• Enemy creatures within 10 feet of you have disadvantage on saving throws against your paladin spells and Channel Divinity options.\nOnce you use this feature, you can't use it again until you finish a long rest."
        )
    ]
)

OATH_OF_VENGEANCE = Subclass(
    name="Oath of Vengeance",
    class_name="Paladin",
    description="The Oath of Vengeance is a solemn commitment to punish those who have committed a grievous sin. When evil forces slaughter helpless villagers, when an entire people turns against the will of the gods, when a thieves' guild grows too violent and powerful, when a dragon rampages through the countryside—at times like these, paladins arise and swear an Oath of Vengeance to set right that which has gone wrong.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Oath Spells",
            level=3,
            description="You gain oath spells at the paladin levels listed.\n3rd: Bane, Hunter's Mark\n5th: Hold Person, Misty Step\n9th: Haste, Protection from Energy\n13th: Banishment, Dimension Door\n17th: Hold Monster, Scrying"
        ),
        SubclassFeature(
            name="Channel Divinity: Abjure Enemy",
            level=3,
            description="As an action, you present your holy symbol and speak a prayer of denunciation, using your Channel Divinity. Choose one creature within 60 feet of you that you can see. That creature must make a Wisdom saving throw, unless it is immune to being frightened. Fiends and undead have disadvantage on this saving throw. On a failed save, the creature is frightened for 1 minute or until it takes any damage. While frightened, the creature's speed is 0, and it can't benefit from any bonus to its speed. On a successful save, the creature's speed is halved for 1 minute or until the creature takes any damage."
        ),
        SubclassFeature(
            name="Channel Divinity: Vow of Enmity",
            level=3,
            description="As a bonus action, you can utter a vow of enmity against a creature you can see within 10 feet of you, using your Channel Divinity. You gain advantage on attack rolls against the creature for 1 minute or until it drops to 0 hit points or falls unconscious."
        ),
        SubclassFeature(
            name="Relentless Avenger",
            level=7,
            description="Your supernatural focus helps you close off a foe's retreat. When you hit a creature with an opportunity attack, you can move up to half your speed immediately after the attack and as part of the same reaction. This movement doesn't provoke opportunity attacks."
        ),
        SubclassFeature(
            name="Soul of Vengeance",
            level=15,
            description="The authority with which you speak your Vow of Enmity gives you greater power over your foe. When a creature under the effect of your Vow of Enmity makes an attack, you can use your reaction to make a melee weapon attack against that creature if it is within range."
        ),
        SubclassFeature(
            name="Avenging Angel",
            level=20,
            description="You can assume the form of an angelic avenger. Using your action, you undergo a transformation. For 1 minute, you gain the following benefits:\n• Wings sprout from your back and grant you a flying speed of 60 feet.\n• You emanate an aura of menace in a 30-foot radius. The first time any enemy creature enters the aura or starts its turn there during a battle, the creature must succeed on a Wisdom saving throw or become frightened of you for 1 minute or until it takes any damage. Attack rolls against the frightened creature have advantage.\nOnce you use this feature, you can't use it again until you finish a long rest."
        )
    ]
)

OATH_OF_CONQUEST = Subclass(
    name="Oath of Conquest",
    class_name="Paladin",
    description="Conquest paladins crush the forces of chaos, enforcing iron discipline through fear and overwhelming might.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Oath Spells",
            level=3,
            description="You gain oath spells at the paladin levels listed.\n3rd: Armor of Agathys, Command\n5th: Hold Person, Spiritual Weapon\n9th: Bestow Curse, Fear\n13th: Dominate Beast, Stoneskin\n17th: Cloudkill, Dominate Person"
        ),
        SubclassFeature(
            name="Channel Divinity: Conquering Presence",
            level=3,
            description="As an action you unleash a menacing aura that forces each creature of your choice within 30 feet to make a Wisdom save or become frightened of you for 1 minute."
        ),
        SubclassFeature(
            name="Channel Divinity: Guided Strike",
            level=3,
            description="When you make an attack roll you can add +10 to the roll after seeing the result but before knowing if it hits, representing your relentless focus."
        ),
        SubclassFeature(
            name="Aura of Conquest",
            level=7,
            description="Creatures frightened of you that start their turn within 10 feet (30 feet at 18th level) have their speed reduced to 0 and take psychic damage equal to half your paladin level."
        ),
        SubclassFeature(
            name="Scornful Rebuke",
            level=15,
            description="When a creature hits you, it takes psychic damage equal to your Charisma modifier if it is within 10 feet, reflecting your contempt for resistance."
        ),
        SubclassFeature(
            name="Invincible Conqueror",
            level=20,
            description="As a bonus action you can enter a state for 1 minute granting resistance to all damage, advantage on attack rolls, and one extra attack whenever you take the Attack action. Once per long rest."
        )
    ]
)

OATH_OF_REDEMPTION = Subclass(
    name="Oath of Redemption",
    class_name="Paladin",
    description="Redemption paladins seek peace above all, enduring harm to turn foes toward righteous paths.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Oath Spells",
            level=3,
            description="You gain oath spells at the paladin levels listed.\n3rd: Sanctuary, Sleep\n5th: Calm Emotions, Hold Person\n9th: Counterspell, Hypnotic Pattern\n13th: Otiluke's Resilient Sphere, Stoneskin\n17th: Hold Monster, Wall of Force"
        ),
        SubclassFeature(
            name="Channel Divinity: Emissary of Peace",
            level=3,
            description="As a bonus action you grant yourself +5 to Persuasion checks for 10 minutes, radiating calm authority."
        ),
        SubclassFeature(
            name="Channel Divinity: Rebuke the Violent",
            level=3,
            description="As a reaction when an attacker within 30 feet deals damage, you force it to make a Wisdom save or take radiant damage equal to the damage it just dealt."
        ),
        SubclassFeature(
            name="Aura of the Guardian",
            level=7,
            description="When a creature you can see within 10 feet (30 feet at 18th level) takes damage, you can use your reaction to take that damage instead, reducing it on the ally to zero."
        ),
        SubclassFeature(
            name="Protective Spirit",
            level=15,
            description="During each of your turns while below half hit points, you regain 1d6 + half your paladin level hit points, reflecting your inner resolve."
        ),
        SubclassFeature(
            name="Emissary of Redemption",
            level=20,
            description="You gain resistance to all damage from creatures that hit you (unless they deal psychic damage or you attack them), and when such a creature hits you it takes radiant damage equal to the damage you take. The aura ends for a creature if you attack it or force it to make a save."
        )
    ]
)

PALADIN_SUBCLASSES = {
    "Oath of Devotion": OATH_OF_DEVOTION,
    "Oath of the Ancients": OATH_OF_THE_ANCIENTS,
    "Oath of Vengeance": OATH_OF_VENGEANCE,
    "Oath of Conquest": OATH_OF_CONQUEST,
    "Oath of Redemption": OATH_OF_REDEMPTION,
    "Oath of Glory": OATH_OF_GLORY,
    "Oath of the Watchers": OATH_OF_THE_WATCHERS,
}

# ========== RANGER SUBCLASSES ==========

HUNTER = Subclass(
    name="Hunter",
    class_name="Ranger",
    description="Emulating the Hunter archetype means accepting your place as a bulwark between civilization and the terrors of the wilderness. As you walk the Hunter's path, you learn specialized techniques for fighting the threats you face.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Hunter's Prey",
            level=3,
            description="You gain one of the following features of your choice.\nColossus Slayer: Your tenacity can wear down the most potent foes. When you hit a creature with a weapon attack, the creature takes an extra 1d8 damage if it's below its hit point maximum. You can deal this extra damage only once per turn.\nGiant Killer: When a Large or larger creature within 5 feet of you hits or misses you with an attack, you can use your reaction to attack that creature immediately after its attack, provided that you can see the creature.\nHorde Breaker: Once on each of your turns when you make a weapon attack, you can make another attack with the same weapon against a different creature that is within 5 feet of the original target and within range of your weapon."
        ),
        SubclassFeature(
            name="Defensive Tactics",
            level=7,
            description="You gain one of the following features of your choice.\nEscape the Horde: Opportunity attacks against you are made with disadvantage.\nMultiattack Defense: When a creature hits you with an attack, you gain a +4 bonus to AC against all subsequent attacks made by that creature for the rest of the turn.\nSteel Will: You have advantage on saving throws against being frightened."
        ),
        SubclassFeature(
            name="Multiattack",
            level=11,
            description="You gain one of the following features of your choice.\nVolley: You can use your action to make a ranged attack against any number of creatures within 10 feet of a point you can see within your weapon's range. You must have ammunition for each target, as normal, and you make a separate attack roll for each target.\nWhirlwind Attack: You can use your action to make a melee attack against any number of creatures within 5 feet of you, with a separate attack roll for each target."
        ),
        SubclassFeature(
            name="Superior Hunter's Defense",
            level=15,
            description="You gain one of the following features of your choice.\nEvasion: When you are subjected to an effect, such as a red dragon's fiery breath or a Lightning Bolt spell, that allows you to make a Dexterity saving throw to take only half damage, you instead take no damage if you succeed on the saving throw, and only half damage if you fail.\nStand Against the Tide: When a hostile creature misses you with a melee attack, you can use your reaction to force that creature to repeat the same attack against another creature (other than itself) of your choice.\nUncanny Dodge: When an attacker that you can see hits you with an attack, you can use your reaction to halve the attack's damage against you."
        )
    ]
)

BEAST_MASTER = Subclass(
    name="Beast Master",
    class_name="Ranger",
    description="The Beast Master archetype embodies a friendship between the civilized races and the beasts of the world. United in focus, beast and ranger work as one to fight the monstrous foes that threaten civilization and the wilderness alike.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Ranger's Companion",
            level=3,
            description="You gain a beast companion that accompanies you on your adventures and is trained to fight alongside you. Choose a beast that is no larger than Medium and that has a challenge rating of 1/4 or lower. Add your proficiency bonus to the beast's AC, attack rolls, and damage rolls, as well as to any saving throws and skills it is proficient in. Its hit point maximum equals its normal maximum or four times your ranger level, whichever is higher. Like any creature, the beast can spend Hit Dice during a short rest. The beast obeys your commands as best as it can. It takes its turn on your initiative. On your turn, you can verbally command the beast where to move (no action required by you). You can use your action to verbally command it to take the Attack, Dash, Disengage, or Help action. If you don't issue a command, the beast takes the Dodge action."
        ),
        SubclassFeature(
            name="Exceptional Training",
            level=7,
            description="On any of your turns when your beast companion doesn't attack, you can use a bonus action to command the beast to take the Dash, Disengage, or Help action on its turn. In addition, the beast's attacks now count as magical for the purpose of overcoming resistance and immunity to nonmagical attacks and damage."
        ),
        SubclassFeature(
            name="Bestial Fury",
            level=11,
            description="When you command your beast companion to take the Attack action, the beast can make two attacks, or it can take the Multiattack action if it has that action."
        ),
        SubclassFeature(
            name="Share Spells",
            level=15,
            description="When you cast a spell targeting yourself, you can also affect your beast companion with the spell if the beast is within 30 feet of you."
        )
    ]
)

GLOOM_STALKER = Subclass(
    name="Gloom Stalker",
    class_name="Ranger",
    description="Gloom Stalkers ambush foes from oppressive darkness, striking swiftly before vanishing back into the shadows.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Gloom Stalker Magic",
            level=3,
            description="You gain additional spells that reflect subterranean stealth, such as Disguise Self, Rope Trick, Fear, Greater Invisibility, and Seeming; they count as ranger spells for you."
        ),
        SubclassFeature(
            name="Dread Ambusher",
            level=3,
            description="You gain +10 walking speed, add Wisdom modifier to initiative, and on the first turn of combat you can make an extra attack that deals an additional 1d8 damage on a hit."
        ),
        SubclassFeature(
            name="Umbral Sight",
            level=3,
            description="You gain darkvision or extend it by 30 feet, and creatures relying on darkvision can't see you while you're in darkness."
        ),
        SubclassFeature(
            name="Iron Mind",
            level=7,
            description="You gain proficiency in Wisdom saving throws; if you already have it, choose Intelligence or Charisma saves instead."
        ),
        SubclassFeature(
            name="Stalker's Flurry",
            level=11,
            description="Once per turn when you miss with a weapon attack, you can make another attack as part of the same action."
        ),
        SubclassFeature(
            name="Shadowy Dodge",
            level=15,
            description="When a creature makes an attack roll against you and doesn't have advantage, you can use your reaction to impose disadvantage as you blur into darkness."
        )
    ]
)

HORIZON_WALKER = Subclass(
    name="Horizon Walker",
    class_name="Ranger",
    description="Horizon Walkers guard planar pathways, teleporting across the battlefield and channeling planar energies into their strikes.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Horizon Walker Magic",
            level=3,
            description="You gain additional spells tied to planar travel, such as Protection from Evil and Good, Misty Step, Haste, Banishment, and Teleportation Circle."
        ),
        SubclassFeature(
            name="Detect Portal",
            level=3,
            description="As an action you can sense any planar portal within 1 mile of you, learning its direction and distance; you can use this feature a number of times equal to your Wisdom modifier per long rest."
        ),
        SubclassFeature(
            name="Planar Warrior",
            level=3,
            description="As a bonus action you can focus on a creature, turning one of your attacks that turn into force damage and adding 1d8 force damage (2d8 at 11th level) while ignoring resistance."
        ),
        SubclassFeature(
            name="Ethereal Step",
            level=7,
            description="You can cast Etherealness without components once per short or long rest, stepping briefly into the Ethereal Plane."
        ),
        SubclassFeature(
            name="Distant Strike",
            level=11,
            description="When you take the Attack action you can teleport up to 10 feet before each attack. If you attack at least two different creatures, you can make one additional attack."
        ),
        SubclassFeature(
            name="Spectral Defense",
            level=15,
            description="When you take damage from an attack you can use your reaction to halve the damage as your form flickers between planes."
        )
    ]
)

MONSTER_SLAYER = Subclass(
    name="Monster Slayer",
    class_name="Ranger",
    description="Monster Slayers hunt supernatural threats with specialized techniques to disrupt magic and finish resilient foes.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Monster Slayer Magic",
            level=3,
            description="You gain additional spells such as Protection from Evil and Good, Zone of Truth, Magic Circle, Banishment, and Hold Monster that aid in battling extraplanar foes."
        ),
        SubclassFeature(
            name="Hunter's Sense",
            level=3,
            description="As an action you can learn a creature's damage immunities, resistances, and vulnerabilities a number of times per long rest equal to your Wisdom modifier."
        ),
        SubclassFeature(
            name="Slayer's Prey",
            level=3,
            description="As a bonus action you designate a target to deal an extra 1d6 damage once per turn when you hit it with a weapon attack; this lasts until you finish a short or long rest."
        ),
        SubclassFeature(
            name="Supernatural Defense",
            level=7,
            description="When the target of your Slayer's Prey forces you to make a saving throw or you suffer an effect requiring an ability check, you add 1d6 to the roll."
        ),
        SubclassFeature(
            name="Magic-User's Nemesis",
            level=11,
            description="When a creature you can see casts a spell or teleports, you can use your reaction to force it to make a Wisdom save; on a failure the spell fails or the teleport is wasted."
        ),
        SubclassFeature(
            name="Slayer's Counter",
            level=15,
            description="When the target of your Slayer's Prey forces you to make a saving throw, you can use your reaction to make one weapon attack against it. On a hit, the save automatically succeeds, reflecting your ability to disrupt its magic."
        )
    ]
)

RANGER_SUBCLASSES = {
    "Hunter": HUNTER,
    "Beast Master": BEAST_MASTER,
    "Gloom Stalker": GLOOM_STALKER,
    "Horizon Walker": HORIZON_WALKER,
    "Monster Slayer": MONSTER_SLAYER,
    "Fey Wanderer": FEY_WANDERER,
    "Swarmkeeper": SWARMKEEPER,
}

# ========== ROGUE SUBCLASSES ==========

THIEF = Subclass(
    name="Thief",
    class_name="Rogue",
    description="You hone your skills in the larcenous arts. Burglars, bandits, cutpurses, and other criminals typically follow this archetype, but so do rogues who prefer to think of themselves as professional treasure seekers, explorers, delvers, and investigators.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Fast Hands",
            level=3,
            description="You can use the bonus action granted by your Cunning Action to make a Dexterity (Sleight of Hand) check, use your thieves' tools to disarm a trap or open a lock, or take the Use an Object action."
        ),
        SubclassFeature(
            name="Second-Story Work",
            level=3,
            description="You gain the ability to climb faster than normal; climbing no longer costs you extra movement. In addition, when you make a running jump, the distance you cover increases by a number of feet equal to your Dexterity modifier."
        ),
        SubclassFeature(
            name="Supreme Sneak",
            level=9,
            description="You have advantage on a Dexterity (Stealth) check if you move no more than half your speed on the same turn."
        ),
        SubclassFeature(
            name="Use Magic Device",
            level=13,
            description="You have learned enough about the workings of magic that you can improvise the use of items even when they are not intended for you. You ignore all class, race, and level requirements on the use of magic items."
        ),
        SubclassFeature(
            name="Thief's Reflexes",
            level=17,
            description="You have become adept at laying ambushes and quickly escaping danger. You can take two turns during the first round of any combat. You take your first turn at your normal initiative and your second turn at your initiative minus 10. You can't use this feature when you are surprised."
        )
    ]
)

ASSASSIN = Subclass(
    name="Assassin",
    class_name="Rogue",
    description="You focus your training on the grim art of death. Those who adhere to this archetype are diverse: hired killers, spies, bounty hunters, and even specially anointed priests trained to exterminate the enemies of their deity.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Bonus Proficiencies",
            level=3,
            description="You gain proficiency with the disguise kit and the poisoner's kit."
        ),
        SubclassFeature(
            name="Assassinate",
            level=3,
            description="You are at your deadliest when you get the drop on your enemies. You have advantage on attack rolls against any creature that hasn't taken a turn in the combat yet. In addition, any hit you score against a creature that is surprised is a critical hit."
        ),
        SubclassFeature(
            name="Infiltration Expertise",
            level=9,
            description="You can unfailingly create false identities for yourself. You must spend seven days and 25 gp to establish the history, profession, and affiliations for an identity. You can't establish an identity that belongs to someone else. Thereafter, if you adopt the new identity as a disguise, other creatures believe you to be that person until given an obvious reason not to."
        ),
        SubclassFeature(
            name="Impostor",
            level=13,
            description="You gain the ability to unerringly mimic another person's speech, writing, and behavior. You must spend at least three hours studying these three components of the person's behavior, listening to speech, examining handwriting, and observing mannerisms. Your ruse is indiscernible to the casual observer. If a wary creature suspects something is amiss, you have advantage on any Charisma (Deception) check you make to avoid detection."
        ),
        SubclassFeature(
            name="Death Strike",
            level=17,
            description="You become a master of instant death. When you attack and hit a creature that is surprised, it must make a Constitution saving throw (DC 8 + your Dexterity modifier + your proficiency bonus). On a failed save, double the damage of your attack against the creature."
        )
    ]
)

ARCANE_TRICKSTER = Subclass(
    name="Arcane Trickster",
    class_name="Rogue",
    description="Some rogues enhance their fine-honed skills of stealth and agility with magic, learning tricks of enchantment and illusion. These rogues include pickpockets and burglars, but also pranksters, mischief-makers, and a significant number of adventurers.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Spellcasting",
            level=3,
            description="You augment your martial prowess with the ability to cast spells. You learn three cantrips: Mage Hand and two other cantrips of your choice from the wizard spell list. You learn another wizard cantrip of your choice at 10th level. When you cast Mage Hand, you can make the spectral hand invisible, and you can perform additional tasks with it (stow/retrieve objects, pick locks, disarm traps, use objects)."
        ),
        SubclassFeature(
            name="Mage Hand Legerdemain",
            level=3,
            description="When you cast Mage Hand, you can make the spectral hand invisible, and you can perform the following additional tasks with it:\n• You can stow one object the hand is holding in a container worn or carried by another creature.\n• You can retrieve an object in a container worn or carried by another creature.\n• You can use thieves' tools to pick locks and disarm traps at range.\nYou can perform one of these tasks without being noticed by a creature if you succeed on a Dexterity (Sleight of Hand) check contested by the creature's Wisdom (Perception) check. In addition, you can use the bonus action granted by your Cunning Action to control the hand."
        ),
        SubclassFeature(
            name="Magical Ambush",
            level=9,
            description="If you are hidden from a creature when you cast a spell on it, the creature has disadvantage on any saving throw it makes against the spell this turn."
        ),
        SubclassFeature(
            name="Versatile Trickster",
            level=13,
            description="You gain the ability to distract targets with your Mage Hand. As a bonus action on your turn, you can designate a creature within 5 feet of the spectral hand created by the spell. Doing so gives you advantage on attack rolls against that creature until the end of the turn."
        ),
        SubclassFeature(
            name="Spell Thief",
            level=17,
            description="You gain the ability to magically steal the knowledge of how to cast a spell from another spellcaster. Immediately after a creature casts a spell that targets you or includes you in its area of effect, you can use your reaction to force the creature to make a saving throw with its spellcasting ability modifier. The DC equals your spell save DC. On a failed save, you negate the spell's effect against you, and you steal the knowledge of the spell if it is at least 1st level and of a level you can cast (it doesn't need to be a wizard spell). For the next 8 hours, you know the spell and can cast it using your spell slots. The creature can't cast that spell until the 8 hours have passed. Once you use this feature, you can't use it again until you finish a long rest."
        )
    ]
)

INQUISITIVE = Subclass(
    name="Inquisitive",
    class_name="Rogue",
    description="Inquisitive rogues excel at rooting out secrets, reading foes, and exploiting every hint of deception.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Ear for Deceit",
            level=3,
            description="Whenever you make an Insight check to determine if a creature is lying, treat a rolled 7 or lower on the d20 as an 8."
        ),
        SubclassFeature(
            name="Eye for Detail",
            level=3,
            description="You can use a bonus action to make a Perception check to spot hidden creatures or an Investigation check to uncover or decipher clues."
        ),
        SubclassFeature(
            name="Insightful Fighting",
            level=3,
            description="As a bonus action you can make an Insight check contested by a creature's Deception. On a success you can use Sneak Attack against it even without advantage (unless you have disadvantage) for 1 minute or until you target another creature."
        ),
        SubclassFeature(
            name="Steady Eye",
            level=9,
            description="If you move no more than half your speed on your turn, you have advantage on any Perception or Investigation check you make that turn."
        ),
        SubclassFeature(
            name="Unerring Eye",
            level=13,
            description="As an action you can detect illusions, shapechangers, and magic disguises within 30 feet unless they succeed on a Charisma save; usable a number of times equal to your Wisdom modifier per long rest."
        ),
        SubclassFeature(
            name="Eye for Weakness",
            level=17,
            description="When Insightful Fighting is active on a target, you deal an extra 3d6 damage the first time you hit that creature with Sneak Attack each turn."
        )
    ]
)

MASTERMIND = Subclass(
    name="Mastermind",
    class_name="Rogue",
    description="Masterminds weave intrigue, mimicry, and battlefield tactics to turn every ally into an extension of their schemes.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Master of Intrigue",
            level=3,
            description="You gain proficiency with the disguise kit, forgery kit, and one gaming set; you learn two languages and can mimic speech and writing you've observed for 1 minute, fooling listeners with an Insight check contested by your Deception."
        ),
        SubclassFeature(
            name="Master of Tactics",
            level=3,
            description="You can use the Help action as a bonus action, and when you help an ally attack a creature, the target can be within 30 feet of you if it can see or hear you."
        ),
        SubclassFeature(
            name="Insightful Manipulator",
            level=9,
            description="After observing a creature for 1 minute outside combat, you can learn whether it is equal, superior, or inferior to you in Intelligence, Wisdom, Charisma, and class levels."
        ),
        SubclassFeature(
            name="Misdirection",
            level=13,
            description="When a creature targets you with an attack while another creature is within 5 feet of you, you can use your reaction to cause the attack to target that other creature."
        ),
        SubclassFeature(
            name="Soul of Deceit",
            level=17,
            description="Your thoughts can't be read unless you allow it; magic that would determine if you are lying indicates you are telling the truth, and you can present false thoughts when targeted by telepathy."
        )
    ]
)

SCOUT = Subclass(
    name="Scout",
    class_name="Rogue",
    description="Scouts range ahead of companions, striking from the wilds with unmatched mobility and knowledge of the natural world.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Skirmisher",
            level=3,
            description="When a creature ends its turn within 5 feet of you, you can use your reaction to move up to half your speed without provoking opportunity attacks."
        ),
        SubclassFeature(
            name="Survivalist",
            level=3,
            description="You gain proficiency in Nature and Survival, and your proficiency bonus is doubled for checks using those skills."
        ),
        SubclassFeature(
            name="Superior Mobility",
            level=9,
            description="Your walking speed increases by 10 feet, and you gain climbing and swimming speeds equal to your walking speed."
        ),
        SubclassFeature(
            name="Ambush Master",
            level=13,
            description="You have advantage on initiative rolls, and the first creature you hit in the first round of combat grants advantage on attacks against it until the start of your next turn."
        ),
        SubclassFeature(
            name="Sudden Strike",
            level=17,
            description="Once on each of your turns you can make one extra weapon attack as part of the Attack action, and if it hits you can apply Sneak Attack even if you've already used it this turn."
        )
    ]
)

SWASHBUCKLER = Subclass(
    name="Swashbuckler",
    class_name="Rogue",
    description="Swashbucklers dance through combat with panache, striking boldly and darting away before reprisals can land.",
    selection_level=3,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Fancy Footwork",
            level=3,
            description="When you make a melee attack against a creature, that creature can't make opportunity attacks against you for the rest of your turn, whether or not you hit."
        ),
        SubclassFeature(
            name="Rakish Audacity",
            level=3,
            description="You add your Charisma modifier to initiative, and you can use Sneak Attack against a creature if you are within 5 feet of it, no other creatures are within 5 feet of you, and you don't have disadvantage."
        ),
        SubclassFeature(
            name="Panache",
            level=9,
            description="As an action you can make a Persuasion check contested by a creature's Insight to charm it (if friendly) or goad it into focusing on you (if hostile), imposing disadvantage on attacks against others."
        ),
        SubclassFeature(
            name="Elegant Maneuver",
            level=13,
            description="As a bonus action you can gain advantage on the next Acrobatics or Athletics check you make during the same turn."
        ),
        SubclassFeature(
            name="Master Duelist",
            level=17,
            description="When you miss with an attack, you can reroll it with advantage. Once you do so, you can't use this feature again until you finish a short or long rest."
        )
    ]
)

ROGUE_SUBCLASSES = {
    "Thief": THIEF,
    "Assassin": ASSASSIN,
    "Arcane Trickster": ARCANE_TRICKSTER,
    "Inquisitive": INQUISITIVE,
    "Mastermind": MASTERMIND,
    "Scout": SCOUT,
    "Swashbuckler": SWASHBUCKLER,
    "Phantom": PHANTOM,
    "Soulknife": SOULKNIFE,
}

# ========== SORCERER SUBCLASSES ==========

DRACONIC_BLOODLINE = Subclass(
    name="Draconic Bloodline",
    class_name="Sorcerer",
    description="Your innate magic comes from draconic magic that was mingled with your blood or that of your ancestors. Most often, sorcerers with this origin trace their descent back to a mighty sorcerer of ancient times who made a bargain with a dragon or who might even have claimed a dragon parent.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Dragon Ancestor",
            level=1,
            description="You choose one type of dragon as your ancestor. The damage type associated with each dragon is used by features you gain later. You can speak, read, and write Draconic. Additionally, whenever you make a Charisma check when interacting with dragons, your proficiency bonus is doubled if it applies to the check."
        ),
        SubclassFeature(
            name="Draconic Resilience",
            level=1,
            description="As magic flows through your body, it causes physical traits of your dragon ancestors to emerge. At 1st level, your hit point maximum increases by 1 and increases by 1 again whenever you gain a level in this class. Additionally, parts of your skin are covered by a thin sheen of dragon-like scales. When you aren't wearing armor, your AC equals 13 + your Dexterity modifier."
        ),
        SubclassFeature(
            name="Elemental Affinity",
            level=6,
            description="When you cast a spell that deals damage of the type associated with your draconic ancestry, you can add your Charisma modifier to one damage roll of that spell. At the same time, you can spend 1 sorcery point to gain resistance to that damage type for 1 hour."
        ),
        SubclassFeature(
            name="Dragon Wings",
            level=14,
            description="You gain the ability to sprout a pair of dragon wings from your back, gaining a flying speed equal to your current speed. You can create these wings as a bonus action on your turn. They last until you dismiss them as a bonus action on your turn. You can't manifest your wings while wearing armor unless the armor is made to accommodate them, and clothing not made to accommodate your wings might be destroyed when you manifest them."
        ),
        SubclassFeature(
            name="Draconic Presence",
            level=18,
            description="You can channel the dread presence of your dragon ancestor, causing those around you to become awestruck or frightened. As an action, you can spend 5 sorcery points to draw on this power and exude an aura of awe or fear (your choice) to a distance of 60 feet. For 1 minute or until you lose your concentration, each hostile creature that starts its turn in this aura must succeed on a Wisdom saving throw or be charmed (if you chose awe) or frightened (if you chose fear) until the aura ends. A creature that succeeds on this saving throw is immune to your aura for 24 hours."
        )
    ]
)

WILD_MAGIC = Subclass(
    name="Wild Magic",
    class_name="Sorcerer",
    description="Your innate magic comes from the wild forces of chaos that underlie the order of creation. You might have endured exposure to some form of raw magic, perhaps through a planar portal leading to Limbo, the Elemental Planes, or the Far Realm.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Wild Magic Surge",
            level=1,
            description="Your spellcasting can unleash surges of untamed magic. Immediately after you cast a sorcerer spell of 1st level or higher, the DM can have you roll a d20. If you roll a 1, roll on the Wild Magic Surge table to create a random magical effect."
        ),
        SubclassFeature(
            name="Tides of Chaos",
            level=1,
            description="You can manipulate the forces of chance and chaos to gain advantage on one attack roll, ability check, or saving throw. Once you do so, you must finish a long rest before you can use this feature again. Any time before you regain the use of this feature, the DM can have you roll on the Wild Magic Surge table immediately after you cast a sorcerer spell of 1st level or higher. You then regain the use of this feature."
        ),
        SubclassFeature(
            name="Bend Luck",
            level=6,
            description="You have the ability to twist fate using your wild magic. When another creature you can see makes an attack roll, an ability check, or a saving throw, you can use your reaction and spend 2 sorcery points to roll 1d4 and apply the number rolled as a bonus or penalty (your choice) to the creature's roll. You can do so after the creature rolls but before any effects of the roll occur."
        ),
        SubclassFeature(
            name="Controlled Chaos",
            level=14,
            description="You gain a modicum of control over the surges of your wild magic. Whenever you roll on the Wild Magic Surge table, you can roll twice and use either number."
        ),
        SubclassFeature(
            name="Spell Bombardment",
            level=18,
            description="The harmful energy of your spells intensifies. When you roll damage for a spell and roll the highest number possible on any of the dice, choose one of those dice, roll it again and add that roll to the damage. You can use the feature only once per turn."
        )
    ]
)

DIVINE_SOUL = Subclass(
    name="Divine Soul",
    class_name="Sorcerer",
    description="Divine Soul sorcerers are touched by the gods, blending arcane talent with clerical miracles and radiant resilience.",
    selection_level=1,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Divine Magic",
            level=1,
            description="You learn additional spells from the cleric list based on an alignment affinity (Good, Evil, Law, Chaos, Neutral) and can replace them when you gain a sorcerer level."
        ),
        SubclassFeature(
            name="Favored by the Gods",
            level=1,
            description="If you fail a saving throw or miss with an attack roll, you can add 2d4 to the roll once per short or long rest."
        ),
        SubclassFeature(
            name="Empowered Healing",
            level=6,
            description="When you or an ally within 5 feet roll dice to restore hit points, you can spend 1 sorcery point to reroll any number of those dice."
        ),
        SubclassFeature(
            name="Otherworldly Wings",
            level=14,
            description="As a bonus action you can manifest angelic or fiendish wings granting a flying speed equal to your walking speed until you dismiss them."
        ),
        SubclassFeature(
            name="Unearthly Recovery",
            level=18,
            description="As a bonus action you can regain hit points equal to half your hit point maximum once per long rest."
        )
    ]
)

SHADOW_MAGIC = Subclass(
    name="Shadow Magic",
    class_name="Sorcerer",
    description="Shadow Magic sorcerers draw power from the Shadowfell, wielding darkness and undead vigor to sap foes.",
    selection_level=1,
    source=SOURCE_XANATHARS,
    features=[
        SubclassFeature(
            name="Eyes of the Dark",
            level=1,
            description="You gain darkvision (or extend it) to 120 feet and can spend 2 sorcery points to cast Darkness, seeing through it."
        ),
        SubclassFeature(
            name="Strength of the Grave",
            level=1,
            description="When damage reduces you to 0 hit points, you can make a Charisma save to drop to 1 hit point instead, once per long rest."
        ),
        SubclassFeature(
            name="Hound of Ill Omen",
            level=6,
            description="As a bonus action you can spend 3 sorcery points to summon a spectral hound that hunts a creature you can see, imposing disadvantage on saves against your spells."
        ),
        SubclassFeature(
            name="Shadow Walk",
            level=14,
            description="As a bonus action you can teleport from one area of dim light or darkness to another within 120 feet."
        ),
        SubclassFeature(
            name="Umbral Form",
            level=18,
            description="As a bonus action you can spend 6 sorcery points to gain resistance to all damage except force and radiant, and move through objects for 1 minute while in a shadowy form."
        )
    ]
)

SORCERER_SUBCLASSES = {
    "Draconic Bloodline": DRACONIC_BLOODLINE,
    "Wild Magic": WILD_MAGIC,
    "Divine Soul": DIVINE_SOUL,
    "Shadow Magic": SHADOW_MAGIC,
    "Aberrant Mind": ABERRANT_MIND,
    "Clockwork Soul": CLOCKWORK_SOUL,
}

# ========== WARLOCK SUBCLASSES ==========

THE_ARCHFEY = Subclass(
    name="The Archfey",
    class_name="Warlock",
    description="Your patron is a lord or lady of the fey, a creature of legend who holds secrets that were forgotten before the mortal races were born. This being's motivations are often inscrutable, and sometimes whimsical, and might involve a striving for greater magical power or the settling of age-old grudges.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Expanded Spell List",
            level=1,
            description="The Archfey lets you choose from an expanded list of spells when you learn a warlock spell. The following spells are added to the warlock spell list for you.\n1st: Faerie Fire, Sleep\n2nd: Calm Emotions, Phantasmal Force\n3rd: Blink, Plant Growth\n4th: Dominate Beast, Greater Invisibility\n5th: Dominate Person, Seeming"
        ),
        SubclassFeature(
            name="Fey Presence",
            level=1,
            description="Your patron bestows upon you the ability to project the beguiling and fearsome presence of the fey. As an action, you can cause each creature in a 10-foot cube originating from you to make a Wisdom saving throw against your warlock spell save DC. The creatures that fail their saving throws are all charmed or frightened by you (your choice) until the end of your next turn. Once you use this feature, you can't use it again until you finish a short or long rest."
        ),
        SubclassFeature(
            name="Misty Escape",
            level=6,
            description="You can vanish in a puff of mist in response to harm. When you take damage, you can use your reaction to turn invisible and teleport up to 60 feet to an unoccupied space you can see. You remain invisible until the start of your next turn or until you attack or cast a spell. Once you use this feature, you can't use it again until you finish a short or long rest."
        ),
        SubclassFeature(
            name="Beguiling Defenses",
            level=10,
            description="Your patron teaches you how to turn the mind-affecting magic of your enemies against them. You are immune to being charmed, and when another creature attempts to charm you, you can use your reaction to attempt to turn the charm back on that creature. The creature must succeed on a Wisdom saving throw against your warlock spell save DC or be charmed by you for 1 minute or until the creature takes any damage."
        ),
        SubclassFeature(
            name="Dark Delirium",
            level=14,
            description="You can plunge a creature into an illusory realm. As an action, choose a creature that you can see within 60 feet of you. It must make a Wisdom saving throw against your warlock spell save DC. On a failed save, it is charmed or frightened by you (your choice) for 1 minute or until your concentration is broken. This effect ends early if the creature takes any damage. Until this illusion ends, the creature thinks it is lost in a misty realm, the appearance of which you choose. The creature can see and hear only itself, you, and the illusion. You must finish a short or long rest before you can use this feature again."
        )
    ]
)

THE_FIEND = Subclass(
    name="The Fiend",
    class_name="Warlock",
    description="You have made a pact with a fiend from the lower planes of existence, a being whose aims are evil, even if you strive against those aims. Such beings desire the corruption or destruction of all things, ultimately including you.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Expanded Spell List",
            level=1,
            description="The Fiend lets you choose from an expanded list of spells when you learn a warlock spell. The following spells are added to the warlock spell list for you.\n1st: Burning Hands, Command\n2nd: Blindness/Deafness, Scorching Ray\n3rd: Fireball, Stinking Cloud\n4th: Fire Shield, Wall of Fire\n5th: Flame Strike, Hallow"
        ),
        SubclassFeature(
            name="Dark One's Blessing",
            level=1,
            description="When you reduce a hostile creature to 0 hit points, you gain temporary hit points equal to your Charisma modifier + your warlock level (minimum of 1)."
        ),
        SubclassFeature(
            name="Dark One's Own Luck",
            level=6,
            description="You can call on your patron to alter fate in your favor. When you make an ability check or a saving throw, you can use this feature to add a d10 to your roll. You can do so after seeing the initial roll but before any of the roll's effects occur. Once you use this feature, you can't use it again until you finish a short or long rest."
        ),
        SubclassFeature(
            name="Fiendish Resilience",
            level=10,
            description="You can choose one damage type when you finish a short or long rest. You gain resistance to that damage type until you choose a different one with this feature. Damage from magical weapons or silver weapons ignores this resistance."
        ),
        SubclassFeature(
            name="Hurl Through Hell",
            level=14,
            description="When you hit a creature with an attack, you can use this feature to instantly transport the target through the lower planes. The creature disappears and hurtles through a nightmare landscape. At the end of your next turn, the target returns to the space it previously occupied, or the nearest unoccupied space. If the target is not a fiend, it takes 10d10 psychic damage as it reels from its horrific experience. Once you use this feature, you can't use it again until you finish a long rest."
        )
    ]
)

THE_GREAT_OLD_ONE = Subclass(
    name="The Great Old One",
    class_name="Warlock",
    description="Your patron is a mysterious entity whose nature is utterly foreign to the fabric of reality. It might come from the Far Realm, the space beyond reality, or it could be one of the elder gods known only in legends.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Expanded Spell List",
            level=1,
            description="The Great Old One lets you choose from an expanded list of spells when you learn a warlock spell. The following spells are added to the warlock spell list for you.\n1st: Dissonant Whispers, Tasha's Hideous Laughter\n2nd: Detect Thoughts, Phantasmal Force\n3rd: Clairvoyance, Sending\n4th: Dominate Beast, Evard's Black Tentacles\n5th: Dominate Person, Telekinesis"
        ),
        SubclassFeature(
            name="Awakened Mind",
            level=1,
            description="Your alien knowledge gives you the ability to touch the minds of other creatures. You can communicate telepathically with any creature you can see within 30 feet of you. You don't need to share a language with the creature for it to understand your telepathic utterances, but the creature must be able to understand at least one language."
        ),
        SubclassFeature(
            name="Entropic Ward",
            level=6,
            description="You learn to magically ward yourself against attack and to turn an enemy's failed strike into good luck for yourself. When a creature makes an attack roll against you, you can use your reaction to impose disadvantage on that roll. If the attack misses you, your next attack roll against the creature has advantage if you make it before the end of your next turn. Once you use this feature, you can't use it again until you finish a short or long rest."
        ),
        SubclassFeature(
            name="Thought Shield",
            level=10,
            description="Your thoughts can't be read by telepathy or other means unless you allow it. You also have resistance to psychic damage, and whenever a creature deals psychic damage to you, that creature takes the same amount of damage that you do."
        ),
        SubclassFeature(
            name="Create Thrall",
            level=14,
            description="You gain the ability to infect a humanoid's mind with the alien magic of your patron. You can use your action to touch an incapacitated humanoid. That creature is then charmed by you until a Remove Curse spell is cast on it, the charmed condition is removed from it, or you use this feature again. You can communicate telepathically with the charmed creature as long as the two of you are on the same plane of existence."
        )
    ]
)

WARLOCK_SUBCLASSES = {
    "The Archfey": THE_ARCHFEY,
    "The Fiend": THE_FIEND,
    "The Great Old One": THE_GREAT_OLD_ONE,
    "The Hexblade": THE_HEXBLADE,
    "The Celestial": THE_CELESTIAL,
    "The Fathomless": THE_FATHOMLESS,
    "The Genie": THE_GENIE,
}

# ========== WIZARD SUBCLASSES ==========

BLADESINGING = Subclass(
    name="Bladesinging",
    class_name="Wizard",
    description="Bladesingers fuse swordplay with arcane artistry, weaving defensive magic into every strike.",
    selection_level=2,
    source=SOURCE_TASHAS,
    features=[
        SubclassFeature(
            name="Training in War and Song",
            level=2,
            description="You gain proficiency with light armor and one one-handed melee weapon of your choice, and you gain proficiency in Performance if you don't already have it."
        ),
        SubclassFeature(
            name="Bladesong",
            level=2,
            description="You can use a bonus action to start the Bladesong for 1 minute, gaining bonuses to AC, movement speed, Acrobatics checks, and concentration saves equal to your Intelligence modifier (uses equal to proficiency bonus)."
        ),
        SubclassFeature(
            name="Extra Attack",
            level=6,
            description="You can attack twice, instead of once, whenever you take the Attack action on your turn, and you can replace one of the attacks with casting a cantrip."
        ),
        SubclassFeature(
            name="Song of Defense",
            level=10,
            description="While your Bladesong is active, you can use your reaction to expend a spell slot and reduce damage you take by 5 × the slot's level."
        ),
        SubclassFeature(
            name="Song of Victory",
            level=14,
            description="While Bladesong is active, you add your Intelligence modifier to the damage of your melee weapon attacks."
        )
    ]
)

SCHOOL_OF_ABJURATION = Subclass(
    name="School of Abjuration",
    class_name="Wizard",
    description="The School of Abjuration emphasizes magic that blocks, banishes, or protects. Detractors of this school say that its tradition is about denial, negation rather than positive assertion. You understand, however, that ending harmful effects, protecting the weak, and banishing evil influences is anything but a philosophical void.",
    selection_level=2,
    features=[
        SubclassFeature(
            name="Abjuration Savant",
            level=2,
            description="The gold and time you must spend to copy an abjuration spell into your spellbook is halved."
        ),
        SubclassFeature(
            name="Arcane Ward",
            level=2,
            description="You can weave magic around yourself for protection. When you cast an abjuration spell of 1st level or higher, you can simultaneously use a strand of the spell's magic to create a magical ward on yourself that lasts until you finish a long rest. The ward has hit points equal to twice your wizard level + your Intelligence modifier. Whenever you take damage, the ward takes the damage instead. If this damage reduces the ward to 0 hit points, you take any remaining damage. While the ward has 0 hit points, it can't absorb damage, but its magic remains. Whenever you cast an abjuration spell of 1st level or higher, the ward regains a number of hit points equal to twice the level of the spell."
        ),
        SubclassFeature(
            name="Projected Ward",
            level=6,
            description="When a creature that you can see within 30 feet of you takes damage, you can use your reaction to cause your Arcane Ward to absorb that damage. If this damage reduces the ward to 0 hit points, the warded creature takes any remaining damage."
        ),
        SubclassFeature(
            name="Improved Abjuration",
            level=10,
            description="When you cast an abjuration spell that requires you to make an ability check as a part of casting that spell (as in Counterspell and Dispel Magic), you add your proficiency bonus to that ability check."
        ),
        SubclassFeature(
            name="Spell Resistance",
            level=14,
            description="You have advantage on saving throws against spells. Furthermore, you have resistance against the damage of spells."
        )
    ]
)

SCHOOL_OF_CONJURATION = Subclass(
    name="School of Conjuration",
    class_name="Wizard",
    description="As a conjurer, you favor spells that produce objects and creatures out of thin air. You can conjure billowing clouds of killing fog or summon creatures from elsewhere to fight on your behalf.",
    selection_level=2,
    features=[
        SubclassFeature(
            name="Conjuration Savant",
            level=2,
            description="The gold and time you must spend to copy a conjuration spell into your spellbook is halved."
        ),
        SubclassFeature(
            name="Minor Conjuration",
            level=2,
            description="You can use your action to conjure up an inanimate object in your hand or on the ground within 10 feet of you. This object can be no larger than 3 feet on a side and weigh no more than 10 pounds, and its form must be that of a nonmagical object that you have seen. The object disappears after 1 hour, when you use this feature again, or if it takes or deals any damage."
        ),
        SubclassFeature(
            name="Benign Transposition",
            level=6,
            description="As an action, you can teleport up to 30 feet to an unoccupied space you can see. Alternatively, you can choose a space within range that is occupied by a Small or Medium creature. If that creature is willing, you both teleport, swapping places. Once you use this feature, you can't use it again until you finish a long rest or you cast a conjuration spell of 1st level or higher."
        ),
        SubclassFeature(
            name="Focused Conjuration",
            level=10,
            description="While you are concentrating on a conjuration spell, your concentration can't be broken as a result of taking damage."
        ),
        SubclassFeature(
            name="Durable Summons",
            level=14,
            description="Any creature that you summon or create with a conjuration spell has 30 temporary hit points."
        )
    ]
)

SCHOOL_OF_DIVINATION = Subclass(
    name="School of Divination",
    class_name="Wizard",
    description="The counsel of diviners is sought by royalty and commoners alike, for all seek a clearer understanding of the past, present, and future.",
    selection_level=2,
    features=[
        SubclassFeature(
            name="Divination Savant",
            level=2,
            description="The gold and time you must spend to copy a divination spell into your spellbook is halved."
        ),
        SubclassFeature(
            name="Portent",
            level=2,
            description="Glimpses of the future begin to press in on your awareness. When you finish a long rest, roll two d20s and record the numbers rolled. You can replace any attack roll, saving throw, or ability check made by you or a creature you can see with one of these foretelling rolls."
        ),
        SubclassFeature(
            name="Expert Divination",
            level=6,
            description="Casting divination spells comes so easily to you that it expends only a fraction of your spellcasting efforts. When you cast a divination spell of 2nd level or higher using a spell slot, you regain one expended spell slot. The slot you regain must be of a lower level than the spell you cast and can't be higher than 5th level."
        ),
        SubclassFeature(
            name="The Third Eye",
            level=10,
            description="You can use your action to increase your powers of perception. When you do so, choose one benefit that lasts until you are incapacitated or you take a short or long rest: Darkvision, Ethereal Sight, Greater Comprehension, or See Invisibility."
        ),
        SubclassFeature(
            name="Greater Portent",
            level=14,
            description="You can see even further into time's endless tapestry; you roll three d20s for your Portent feature, rather than two."
        )
    ]
)

SCHOOL_OF_ENCHANTMENT = Subclass(
    name="School of Enchantment",
    class_name="Wizard",
    description="As a member of the School of Enchantment, you have honed your ability to magically entrance and beguile other creatures.",
    selection_level=2,
    features=[
        SubclassFeature(
            name="Enchantment Savant",
            level=2,
            description="The gold and time you must spend to copy an enchantment spell into your spellbook is halved."
        ),
        SubclassFeature(
            name="Hypnotic Gaze",
            level=2,
            description="As an action, choose one creature you can see within 5 feet of you. If the target can see or hear you, it must succeed on a Wisdom saving throw against your wizard spell save DC or be charmed until the end of your next turn. The charmed creature's speed becomes 0, and the creature is incapacitated and visibly dazed."
        ),
        SubclassFeature(
            name="Instinctive Charm",
            level=6,
            description="When a creature you can see within 30 feet of you makes an attack roll against you, you can use your reaction to divert the attack, provided another creature is within the attack's range. The attacker must make a Wisdom saving throw; on a failed save, the attacker must target the creature that is closest to it, not including you or itself."
        ),
        SubclassFeature(
            name="Split Enchantment",
            level=10,
            description="When you cast an enchantment spell of 1st level or higher that targets only one creature, you can have it target a second creature."
        ),
        SubclassFeature(
            name="Alter Memories",
            level=14,
            description="You gain the ability to make a creature unaware of your magical influence on it. When you cast an enchantment spell to charm one or more creatures, you can alter one of the creature's understanding so that the charm is not remembered."
        )
    ]
)

SCHOOL_OF_EVOCATION = Subclass(
    name="School of Evocation",
    class_name="Wizard",
    description="You focus your study on magic that creates powerful elemental effects such as bitter cold, searing flame, rolling thunder, crackling lightning, and burning acid. Some evokers find employment in military forces, serving as artillery to blast enemy armies from afar.",
    selection_level=2,
    features=[
        SubclassFeature(
            name="Evocation Savant",
            level=2,
            description="The gold and time you must spend to copy an evocation spell into your spellbook is halved."
        ),
        SubclassFeature(
            name="Sculpt Spells",
            level=2,
            description="You can create pockets of relative safety within the effects of your evocation spells. When you cast an evocation spell that affects other creatures that you can see, you can choose a number of them equal to 1 + the spell's level. The chosen creatures automatically succeed on their saving throws against the spell, and they take no damage if they would normally take half damage on a successful save."
        ),
        SubclassFeature(
            name="Potent Cantrip",
            level=6,
            description="Your damaging cantrips affect even creatures that avoid the brunt of the effect. When a creature succeeds on a saving throw against your cantrip, the creature takes half the cantrip's damage (if any) but suffers no additional effect from the cantrip."
        ),
        SubclassFeature(
            name="Empowered Evocation",
            level=10,
            description="You can add your Intelligence modifier to one damage roll of any wizard evocation spell you cast."
        ),
        SubclassFeature(
            name="Overchannel",
            level=14,
            description="You can increase the power of your simpler spells. When you cast a wizard spell of 1st through 5th level that deals damage, you can deal maximum damage with that spell. The first time you do so, you suffer no adverse effect. If you use this feature again before you finish a long rest, you take 2d12 necrotic damage for each level of the spell, immediately after you cast it. Each time you use this feature again before finishing a long rest, the necrotic damage per spell level increases by 1d12. This damage ignores resistance and immunity."
        )
    ]
)

SCHOOL_OF_ILLUSION = Subclass(
    name="School of Illusion",
    class_name="Wizard",
    description="You focus on magic that dazzles the senses, befuddles the mind, and tricks even the wisest folk.",
    selection_level=2,
    features=[
        SubclassFeature(
            name="Illusion Savant",
            level=2,
            description="The gold and time you must spend to copy an illusion spell into your spellbook is halved."
        ),
        SubclassFeature(
            name="Improved Minor Illusion",
            level=2,
            description="You learn the Minor Illusion cantrip if you don't already know it. When you cast it, you can create both a sound and an image with a single casting of the spell."
        ),
        SubclassFeature(
            name="Malleable Illusions",
            level=6,
            description="When you cast an illusion spell that has a duration of 1 minute or longer, you can use your action to change the nature of that illusion (using the spell's normal parameters for the illusion), provided that you can see the illusion."
        ),
        SubclassFeature(
            name="Illusory Self",
            level=10,
            description="You can create an illusory duplicate of yourself as an instant, almost instinctual reaction to danger. When a creature makes an attack roll against you, you can use your reaction to interpose the illusory duplicate between the attacker and yourself, causing the attack to automatically miss you."
        ),
        SubclassFeature(
            name="Illusory Reality",
            level=14,
            description="You have learned the secret of weaving shadow magic into your illusions to give them a semi-reality. When you cast an illusion spell of 1st level or higher, you can choose one inanimate, nonmagical object that is part of the illusion and make that object real."
        )
    ]
)

SCHOOL_OF_NECROMANCY = Subclass(
    name="School of Necromancy",
    class_name="Wizard",
    description="The School of Necromancy explores the cosmic forces of life, death, and undeath. As you focus your studies in this tradition, you learn to manipulate the energy that animates all living things.",
    selection_level=2,
    features=[
        SubclassFeature(
            name="Necromancy Savant",
            level=2,
            description="The gold and time you must spend to copy a necromancy spell into your spellbook is halved."
        ),
        SubclassFeature(
            name="Grim Harvest",
            level=2,
            description="Once per turn when you kill one or more creatures with a spell of 1st level or higher, you regain hit points equal to twice the spell's level, or three times its level if the spell belongs to the school of necromancy."
        ),
        SubclassFeature(
            name="Undead Thralls",
            level=6,
            description="You add the Animate Dead spell to your spellbook if it is not there already. When you cast Animate Dead, you can create one additional undead creature. Additionally, undead you raise or create with a necromancy spell gain additional hit points equal to your wizard level, and they add your proficiency bonus to their damage rolls."
        ),
        SubclassFeature(
            name="Inured to Undeath",
            level=10,
            description="You have resistance to necrotic damage, and your hit point maximum can't be reduced."
        ),
        SubclassFeature(
            name="Command Undead",
            level=14,
            description="You can use magic to bring undead under your control, even those created by other wizards. As an action, you can choose one undead that you can see within 60 feet of you. That creature must make a Charisma saving throw against your wizard spell save DC. If it succeeds, you can't use this feature on it again. If it fails, it becomes friendly to you and obeys your commands until you use this feature again."
        )
    ]
)

SCHOOL_OF_TRANSMUTATION = Subclass(
    name="School of Transmutation",
    class_name="Wizard",
    description="You are a student of spells that modify energy and matter. To you, the world is not a fixed thing but eminently mutable, and you delight in bending reality to your will.",
    selection_level=2,
    features=[
        SubclassFeature(
            name="Transmutation Savant",
            level=2,
            description="The gold and time you must spend to copy a transmutation spell into your spellbook is halved."
        ),
        SubclassFeature(
            name="Minor Alchemy",
            level=2,
            description="You can temporarily alter the physical properties of one nonmagical object, changing it from one substance into another. You perform a special alchemical procedure on an object composed entirely of wood, stone, iron, copper, or silver, transforming it into a different one of those materials."
        ),
        SubclassFeature(
            name="Transmuter's Stone",
            level=6,
            description="You can spend 8 hours creating a transmuter's stone that stores transmutation magic. While carrying the stone, you can benefit from one effect of your choice: darkvision, an increase to speed, proficiency in Constitution saving throws, or resistance to a damage type."
        ),
        SubclassFeature(
            name="Shapechanger",
            level=10,
            description="You add the Polymorph spell to your spellbook if it is not there already. You can cast Polymorph without expending a spell slot, targeting only yourself, and you regain the ability to do so when you finish a short or long rest."
        ),
        SubclassFeature(
            name="Master Transmuter",
            level=14,
            description="You can use your action to consume the reserves of transmutation magic stored within your transmuter's stone in a single burst. When you do so, you choose one of several powerful transformations: Major Transformation, Panacea, Restore Life, or Restore Youth."
        )
    ]
)

WIZARD_SUBCLASSES = {
    "School of Abjuration": SCHOOL_OF_ABJURATION,
    "School of Conjuration": SCHOOL_OF_CONJURATION,
    "School of Divination": SCHOOL_OF_DIVINATION,
    "School of Enchantment": SCHOOL_OF_ENCHANTMENT,
    "School of Evocation": SCHOOL_OF_EVOCATION,
    "School of Illusion": SCHOOL_OF_ILLUSION,
    "School of Necromancy": SCHOOL_OF_NECROMANCY,
    "School of Transmutation": SCHOOL_OF_TRANSMUTATION,
    "Bladesinging": BLADESINGING,
    "School of War Magic": SCHOOL_OF_WAR_MAGIC,
    "School of Scribes": SCHOOL_OF_SCRIBES,
}

# Dicionário mestre de todas as subclasses
ALL_SUBCLASSES = {
    "Barbarian": BARBARIAN_SUBCLASSES,
    "Bard": BARD_SUBCLASSES,
    "Cleric": CLERIC_SUBCLASSES,
    "Druid": DRUID_SUBCLASSES,
    "Fighter": FIGHTER_SUBCLASSES,
    "Monk": MONK_SUBCLASSES,
    "Paladin": PALADIN_SUBCLASSES,
    "Ranger": RANGER_SUBCLASSES,
    "Rogue": ROGUE_SUBCLASSES,
    "Sorcerer": SORCERER_SUBCLASSES,
    "Warlock": WARLOCK_SUBCLASSES,
    "Wizard": WIZARD_SUBCLASSES
}


class SubclassDatabase:
    """Database de subclasses"""
    
    @staticmethod
    def get_subclasses_for_class(class_name: str) -> Dict[str, Subclass]:
        """Retorna todas as subclasses disponíveis para uma classe"""
        subclasses = ALL_SUBCLASSES.get(class_name, {})
        filtered: Dict[str, Subclass] = {}
        for name, subclass in subclasses.items():
            if SubclassDatabase._is_source_enabled(subclass):
                filtered[name] = subclass
        return filtered
    
    @staticmethod
    def get_subclass(class_name: str, subclass_name: str) -> Subclass:
        """Retorna uma subclasse específica"""
        subclasses = ALL_SUBCLASSES.get(class_name, {})
        return subclasses.get(subclass_name)
    
    @staticmethod
    def get_selection_level(class_name: str) -> int:
        """Retorna o nível em que a classe escolhe sua subclasse"""
        # A maioria das classes escolhe no nível 3
        # Cleric e Warlock escolhem no nível 1
        # Sorcerer e Wizard escolhem no nível 1 (origem/escola)
        special_levels = {
            "Cleric": 1,
            "Warlock": 1,
            "Sorcerer": 1,
            "Wizard": 2
        }
        return special_levels.get(class_name, 3)

    @staticmethod
    def get_source_label(subclass: Optional[Subclass]) -> str:
        if not subclass:
            return ""
        return SOURCE_LABELS.get(subclass.source, SOURCE_LABELS[SOURCE_CORE])

    @staticmethod
    def is_optional_source(subclass: Optional[Subclass]) -> bool:
        if not subclass:
            return False
        return subclass.source in OPTIONAL_SOURCE_FLAGS

    @staticmethod
    def _is_source_enabled(subclass: Subclass) -> bool:
        flag_key = OPTIONAL_SOURCE_FLAGS.get(subclass.source)
        if not flag_key:
            return True
        return AppSettings.get_optional_content_flag(flag_key)
