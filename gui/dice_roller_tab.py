from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QPushButton, QLabel, QLineEdit, QGroupBox, 
                             QTextEdit, QComboBox, QSpinBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from models import Character, DiceRoller

class DiceRollerTab(QWidget):
    def __init__(self, character: Character):
        super().__init__()
        self.character = character
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        custom_group = QGroupBox("Rolagem Personalizada")
        custom_layout = QVBoxLayout()
        
        dice_input_layout = QHBoxLayout()
        dice_input_layout.addWidget(QLabel("Notação:"))
        
        self.dice_input = QLineEdit()
        self.dice_input.setPlaceholderText("Ex: 2d6+3, 1d20, 4d6kh3")
        dice_input_layout.addWidget(self.dice_input)
        
        self.roll_custom_btn = QPushButton("Rolar")
        self.roll_custom_btn.clicked.connect(self.roll_custom_dice)
        dice_input_layout.addWidget(self.roll_custom_btn)
        
        custom_layout.addLayout(dice_input_layout)
        
        quick_roll_layout = QHBoxLayout()
        quick_roll_layout.addWidget(QLabel("Rolagens Rápidas:"))
        
        for dice in ["1d4", "1d6", "1d8", "1d10", "1d12", "1d20", "1d100"]:
            btn = QPushButton(dice)
            btn.clicked.connect(lambda checked, d=dice: self.quick_roll(d))
            quick_roll_layout.addWidget(btn)
        
        custom_layout.addLayout(quick_roll_layout)
        custom_group.setLayout(custom_layout)
        layout.addWidget(custom_group)
        
        character_group = QGroupBox("Rolagens de Personagem")
        character_layout = QVBoxLayout()
        
        initiative_layout = QHBoxLayout()
        initiative_layout.addWidget(QLabel("Iniciativa:"))
        self.initiative_btn = QPushButton("Rolar Iniciativa")
        self.initiative_btn.clicked.connect(self.roll_initiative)
        initiative_layout.addWidget(self.initiative_btn)
        initiative_layout.addStretch()
        character_layout.addLayout(initiative_layout)
        
        save_layout = QHBoxLayout()
        save_layout.addWidget(QLabel("Teste de Resistência:"))
        
        self.save_combo = QComboBox()
        self.save_combo.addItems(['Força', 'Destreza', 'Constituição', 'Inteligência', 'Sabedoria', 'Carisma'])
        save_layout.addWidget(self.save_combo)
        
        self.save_btn = QPushButton("Rolar")
        self.save_btn.clicked.connect(self.roll_saving_throw)
        save_layout.addWidget(self.save_btn)
        save_layout.addStretch()
        
        character_layout.addLayout(save_layout)
        
        skill_layout = QHBoxLayout()
        skill_layout.addWidget(QLabel("Teste de Perícia:"))
        
        self.skill_combo = QComboBox()
        skills = [
            ('Acrobacia', 'Acrobatics', 'dexterity'),
            ('Lidar com Animais', 'Animal Handling', 'wisdom'),
            ('Arcanismo', 'Arcana', 'intelligence'),
            ('Atletismo', 'Athletics', 'strength'),
            ('Enganação', 'Deception', 'charisma'),
            ('História', 'History', 'intelligence'),
            ('Intuição', 'Insight', 'wisdom'),
            ('Intimidação', 'Intimidation', 'charisma'),
            ('Investigação', 'Investigation', 'intelligence'),
            ('Medicina', 'Medicine', 'wisdom'),
            ('Natureza', 'Nature', 'intelligence'),
            ('Percepção', 'Perception', 'wisdom'),
            ('Performance', 'Performance', 'charisma'),
            ('Persuasão', 'Persuasion', 'charisma'),
            ('Religião', 'Religion', 'intelligence'),
            ('Prestidigitação', 'Sleight of Hand', 'dexterity'),
            ('Furtividade', 'Stealth', 'dexterity'),
            ('Sobrevivência', 'Survival', 'wisdom'),
        ]
        
        self.skill_data = {pt_name: (en_name, ability) for pt_name, en_name, ability in skills}
        self.skill_combo.addItems([pt_name for pt_name, _, _ in skills])
        skill_layout.addWidget(self.skill_combo)
        
        self.skill_btn = QPushButton("Rolar")
        self.skill_btn.clicked.connect(self.roll_skill_check)
        skill_layout.addWidget(self.skill_btn)
        skill_layout.addStretch()
        
        character_layout.addLayout(skill_layout)
        
        attack_layout = QHBoxLayout()
        attack_layout.addWidget(QLabel("Ataque:"))
        
        self.attack_ability_combo = QComboBox()
        self.attack_ability_combo.addItems(['Força', 'Destreza'])
        attack_layout.addWidget(self.attack_ability_combo)
        
        self.attack_btn = QPushButton("Rolar Ataque")
        self.attack_btn.clicked.connect(self.roll_attack)
        attack_layout.addWidget(self.attack_btn)
        attack_layout.addStretch()
        
        character_layout.addLayout(attack_layout)
        
        character_group.setLayout(character_layout)
        layout.addWidget(character_group)
        
        result_group = QGroupBox("Histórico de Rolagens")
        result_layout = QVBoxLayout()
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMaximumHeight(300)
        result_layout.addWidget(self.result_text)
        
        clear_btn = QPushButton("Limpar Histórico")
        clear_btn.clicked.connect(self.clear_history)
        result_layout.addWidget(clear_btn)
        
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        layout.addStretch()
    
    def add_result(self, text: str):
        current = self.result_text.toPlainText()
        self.result_text.setPlainText(f"{text}\n{'-' * 50}\n{current}")
    
    def roll_custom_dice(self):
        notation = self.dice_input.text().strip()
        if not notation:
            return
        
        try:
            total, rolls = DiceRoller.roll(notation)
            result = f"🎲 Rolagem: {notation}\n"
            result += f"Resultados individuais: {rolls}\n"
            result += f"TOTAL: {total}"
            self.add_result(result)
        except Exception as e:
            self.add_result(f"❌ Erro ao rolar {notation}: {str(e)}")
    
    def quick_roll(self, dice: str):
        try:
            total, rolls = DiceRoller.roll(dice)
            result = f"🎲 Rolagem Rápida: {dice}\n"
            result += f"Resultado: {rolls[0] if len(rolls) == 1 else rolls}\n"
            result += f"TOTAL: {total}"
            self.add_result(result)
        except Exception as e:
            self.add_result(f"❌ Erro ao rolar {dice}: {str(e)}")
    
    def roll_initiative(self):
        total, d20 = self.character.roll_initiative()
        result = f"⚔️ INICIATIVA\n"
        result += f"d20: {d20}\n"
        result += f"Modificador: {self.character.initiative:+d}\n"
        result += f"TOTAL: {total}"
        
        if d20 == 20:
            result += " 🎉 CRÍTICO!"
        elif d20 == 1:
            result += " 💀 FALHA CRÍTICA!"
        
        self.add_result(result)
    
    def roll_saving_throw(self):
        ability_map = {
            'Força': 'strength',
            'Destreza': 'dexterity',
            'Constituição': 'constitution',
            'Inteligência': 'intelligence',
            'Sabedoria': 'wisdom',
            'Carisma': 'charisma'
        }
        
        pt_ability = self.save_combo.currentText()
        ability = ability_map[pt_ability]
        
        total, d20 = self.character.roll_saving_throw(ability)
        modifier = self.character.stats.get_modifier(ability)
        
        if ability in self.character.saving_throw_proficiencies:
            modifier += self.character.proficiency_bonus
        
        result = f"🛡️ TESTE DE RESISTÊNCIA - {pt_ability.upper()}\n"
        result += f"d20: {d20}\n"
        result += f"Modificador: {modifier:+d}\n"
        result += f"TOTAL: {total}"
        
        if d20 == 20:
            result += " 🎉 CRÍTICO!"
        elif d20 == 1:
            result += " 💀 FALHA CRÍTICA!"
        
        self.add_result(result)
    
    def roll_skill_check(self):
        pt_skill = self.skill_combo.currentText()
        en_skill, ability = self.skill_data[pt_skill]
        
        total, d20 = self.character.roll_skill_check(en_skill, ability)
        modifier = self.character.stats.get_modifier(ability)
        
        if en_skill in self.character.skill_proficiencies:
            modifier += self.character.proficiency_bonus
        
        result = f"🎯 TESTE DE PERÍCIA - {pt_skill.upper()}\n"
        result += f"d20: {d20}\n"
        result += f"Modificador: {modifier:+d}\n"
        result += f"TOTAL: {total}"
        
        if d20 == 20:
            result += " 🎉 CRÍTICO!"
        elif d20 == 1:
            result += " 💀 FALHA CRÍTICA!"
        
        self.add_result(result)
    
    def roll_attack(self):
        ability_map = {
            'Força': 'strength',
            'Destreza': 'dexterity'
        }
        
        pt_ability = self.attack_ability_combo.currentText()
        ability = ability_map[pt_ability]
        
        total, d20 = self.character.roll_attack(ability, weapon_proficient=True)
        modifier = self.character.stats.get_modifier(ability) + self.character.proficiency_bonus
        
        result = f"⚔️ ROLAGEM DE ATAQUE - {pt_ability.upper()}\n"
        result += f"d20: {d20}\n"
        result += f"Modificador: {modifier:+d}\n"
        result += f"TOTAL: {total}"
        
        if d20 == 20:
            result += " 🎉 ACERTO CRÍTICO!"
        elif d20 == 1:
            result += " 💀 ERRO CRÍTICO!"
        
        self.add_result(result)
    
    def clear_history(self):
        self.result_text.clear()
    
    def update_character(self, character: Character):
        self.character = character
