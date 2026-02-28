from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLabel, QGroupBox, QScrollArea, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from models import Character

class CharacterSheetTab(QWidget):
    def __init__(self, character: Character):
        super().__init__()
        self.character = character
        self.init_ui()
    
    def init_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll.setWidget(scroll_widget)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        
        layout = QVBoxLayout(scroll_widget)
        
        header_layout = QVBoxLayout()
        self.name_label = QLabel("Nome do Personagem")
        name_font = QFont()
        name_font.setPointSize(16)
        name_font.setBold(True)
        self.name_label.setFont(name_font)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.name_label)
        
        self.info_label = QLabel("Raça | Subraça | Classe | Nível")
        info_font = QFont()
        info_font.setPointSize(10)
        self.info_label.setFont(info_font)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.info_label)
        
        layout.addLayout(header_layout)
        
        top_row = QHBoxLayout()
        
        combat_group = QGroupBox("Estatísticas de Combate")
        combat_layout = QFormLayout()
        
        self.ac_label = QLabel("10")
        self.ac_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        combat_layout.addRow("Classe de Armadura:", self.ac_label)
        
        self.initiative_label = QLabel("+0")
        self.initiative_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        combat_layout.addRow("Iniciativa:", self.initiative_label)
        
        self.speed_label = QLabel("30 ft")
        self.speed_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        combat_layout.addRow("Deslocamento:", self.speed_label)
        
        self.hp_label = QLabel("0/0")
        self.hp_label.setStyleSheet("font-size: 18px; font-weight: bold; color: red;")
        combat_layout.addRow("Pontos de Vida:", self.hp_label)
        
        self.prof_bonus_label = QLabel("+2")
        self.prof_bonus_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        combat_layout.addRow("Bônus de Proficiência:", self.prof_bonus_label)
        
        combat_group.setLayout(combat_layout)
        top_row.addWidget(combat_group)
        
        stats_group = QGroupBox("Atributos")
        stats_layout = QGridLayout()
        
        self.stat_labels = {}
        stat_names = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']
        stat_abbr = ['FOR', 'DES', 'CON', 'INT', 'SAB', 'CAR']
        
        for idx, (stat_name, abbr) in enumerate(zip(stat_names, stat_abbr)):
            row = idx // 2
            col = (idx % 2) * 3
            
            abbr_label = QLabel(abbr)
            abbr_label.setStyleSheet("font-weight: bold;")
            stats_layout.addWidget(abbr_label, row, col)
            
            score_label = QLabel("10")
            score_label.setStyleSheet("font-size: 16px; font-weight: bold;")
            stats_layout.addWidget(score_label, row, col + 1)
            
            mod_label = QLabel("(+0)")
            mod_label.setStyleSheet("font-size: 14px;")
            stats_layout.addWidget(mod_label, row, col + 2)
            
            self.stat_labels[stat_name] = {
                'score': score_label,
                'modifier': mod_label
            }
        
        stats_group.setLayout(stats_layout)
        top_row.addWidget(stats_group)
        
        layout.addLayout(top_row)
        
        middle_row = QHBoxLayout()
        
        saves_group = QGroupBox("Testes de Resistência")
        saves_layout = QVBoxLayout()
        
        self.saves_labels = {}
        for stat_name, abbr in zip(stat_names, stat_abbr):
            save_layout = QHBoxLayout()
            
            prof_label = QLabel("○")
            prof_label.setStyleSheet("font-size: 14px;")
            save_layout.addWidget(prof_label)
            
            name_label = QLabel(abbr)
            save_layout.addWidget(name_label)
            
            save_layout.addStretch()
            
            bonus_label = QLabel("+0")
            bonus_label.setStyleSheet("font-weight: bold;")
            save_layout.addWidget(bonus_label)
            
            saves_layout.addLayout(save_layout)
            
            self.saves_labels[stat_name] = {
                'prof': prof_label,
                'bonus': bonus_label
            }
        
        saves_group.setLayout(saves_layout)
        middle_row.addWidget(saves_group)
        
        skills_group = QGroupBox("Perícias")
        skills_layout = QVBoxLayout()
        
        self.skills_labels = {}
        skills_list = [
            ('Acrobatics', 'dexterity', 'Acrobacia'),
            ('Animal Handling', 'wisdom', 'Lidar com Animais'),
            ('Arcana', 'intelligence', 'Arcanismo'),
            ('Athletics', 'strength', 'Atletismo'),
            ('Deception', 'charisma', 'Enganação'),
            ('History', 'intelligence', 'História'),
            ('Insight', 'wisdom', 'Intuição'),
            ('Intimidation', 'charisma', 'Intimidação'),
            ('Investigation', 'intelligence', 'Investigação'),
            ('Medicine', 'wisdom', 'Medicina'),
            ('Nature', 'intelligence', 'Natureza'),
            ('Perception', 'wisdom', 'Percepção'),
            ('Performance', 'charisma', 'Performance'),
            ('Persuasion', 'charisma', 'Persuasão'),
            ('Religion', 'intelligence', 'Religião'),
            ('Sleight of Hand', 'dexterity', 'Prestidigitação'),
            ('Stealth', 'dexterity', 'Furtividade'),
            ('Survival', 'wisdom', 'Sobrevivência'),
        ]
        
        for skill_name, ability, pt_name in skills_list:
            skill_layout = QHBoxLayout()
            
            prof_label = QLabel("○")
            prof_label.setStyleSheet("font-size: 14px;")
            skill_layout.addWidget(prof_label)
            
            name_label = QLabel(pt_name)
            skill_layout.addWidget(name_label)
            
            skill_layout.addStretch()
            
            bonus_label = QLabel("+0")
            bonus_label.setStyleSheet("font-weight: bold;")
            skill_layout.addWidget(bonus_label)
            
            skills_layout.addLayout(skill_layout)
            
            self.skills_labels[skill_name] = {
                'prof': prof_label,
                'bonus': bonus_label,
                'ability': ability
            }
        
        skills_group.setLayout(skills_layout)
        middle_row.addWidget(skills_group)
        
        layout.addLayout(middle_row)
        
        bottom_row = QHBoxLayout()
        
        traits_group = QGroupBox("Traços e Características")
        traits_layout = QVBoxLayout()
        self.traits_label = QLabel("Nenhum traço")
        self.traits_label.setWordWrap(True)
        traits_layout.addWidget(self.traits_label)
        traits_group.setLayout(traits_layout)
        bottom_row.addWidget(traits_group)
        
        languages_group = QGroupBox("Idiomas")
        languages_layout = QVBoxLayout()
        self.languages_label = QLabel("Nenhum idioma")
        self.languages_label.setWordWrap(True)
        languages_layout.addWidget(self.languages_label)
        languages_group.setLayout(languages_layout)
        bottom_row.addWidget(languages_group)
        
        layout.addLayout(bottom_row)
        
        layout.addStretch()
        
        self.update_display()
    
    def update_display(self):
        if self.character.name:
            self.name_label.setText(self.character.name)
        else:
            self.name_label.setText("Nome do Personagem")
        
        race_name = self.character.race.name if self.character.race else "Raça"
        subrace_name = self.character.subrace.name if self.character.subrace else "Subraça"
        class_name = self.character.character_class.name if self.character.character_class else "Classe"
        self.info_label.setText(f"{race_name} | {subrace_name} | {class_name} | Nível {self.character.level}")
        
        self.ac_label.setText(str(self.character.armor_class))
        
        init_sign = '+' if self.character.initiative >= 0 else ''
        self.initiative_label.setText(f"{init_sign}{self.character.initiative}")
        
        self.speed_label.setText(f"{self.character.speed} ft")
        
        self.hp_label.setText(f"{self.character.current_hit_points}/{self.character.max_hit_points}")
        
        self.prof_bonus_label.setText(f"+{self.character.proficiency_bonus}")
        
        for stat_name, labels in self.stat_labels.items():
            score = getattr(self.character.stats, stat_name)
            modifier = self.character.stats.get_modifier(stat_name)
            
            labels['score'].setText(str(score))
            sign = '+' if modifier >= 0 else ''
            labels['modifier'].setText(f"({sign}{modifier})")
        
        for stat_name, labels in self.saves_labels.items():
            modifier = self.character.stats.get_modifier(stat_name)
            if stat_name in self.character.saving_throw_proficiencies:
                modifier += self.character.proficiency_bonus
                labels['prof'].setText("●")
                labels['prof'].setStyleSheet("font-size: 14px; color: green;")
            else:
                labels['prof'].setText("○")
                labels['prof'].setStyleSheet("font-size: 14px;")
            
            sign = '+' if modifier >= 0 else ''
            labels['bonus'].setText(f"{sign}{modifier}")
        
        for skill_name, labels in self.skills_labels.items():
            ability = labels['ability']
            modifier = self.character.stats.get_modifier(ability)
            
            if skill_name in self.character.skill_proficiencies:
                modifier += self.character.proficiency_bonus
                labels['prof'].setText("●")
                labels['prof'].setStyleSheet("font-size: 14px; color: green;")
            else:
                labels['prof'].setText("○")
                labels['prof'].setStyleSheet("font-size: 14px;")
            
            sign = '+' if modifier >= 0 else ''
            labels['bonus'].setText(f"{sign}{modifier}")
        
        if self.character.traits:
            self.traits_label.setText("\n".join(f"• {trait}" for trait in self.character.traits))
        else:
            self.traits_label.setText("Nenhum traço")
        
        if self.character.languages:
            self.languages_label.setText(", ".join(self.character.languages))
        else:
            self.languages_label.setText("Nenhum idioma")
    
    def set_character(self, character: Character):
        self.character = character
        self.update_display()
