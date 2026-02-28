from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QComboBox, QSpinBox, QPushButton, 
                             QGroupBox, QLabel, QListWidget, QMessageBox, QScrollArea)
from PyQt6.QtCore import pyqtSignal
from models import Character, RaceDatabase, SubraceDatabase, ClassDatabase, DiceRoller

class CharacterCreationTab(QWidget):
    character_updated = pyqtSignal()
    
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
        
        basic_group = QGroupBox("Informações Básicas")
        basic_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.textChanged.connect(self.update_character)
        basic_layout.addRow("Nome:", self.name_input)
        
        self.race_combo = QComboBox()
        races = list(RaceDatabase.get_all_races().keys())
        self.race_combo.addItems(races)
        self.race_combo.currentTextChanged.connect(self.on_race_changed)
        basic_layout.addRow("Raça:", self.race_combo)
        
        self.subrace_combo = QComboBox()
        # NÃO adicione itens aqui - será preenchido dinamicamente
        self.subrace_combo.currentTextChanged.connect(self.on_subrace_changed)
        basic_layout.addRow("Subraça:", self.subrace_combo)

        self.class_combo = QComboBox()
        classes = list(ClassDatabase.get_all_classes().keys())
        self.class_combo.addItems(classes)
        self.class_combo.currentTextChanged.connect(self.on_class_changed)
        basic_layout.addRow("Classe:", self.class_combo)
        
        self.level_spin = QSpinBox()
        self.level_spin.setMinimum(1)
        self.level_spin.setMaximum(20)
        self.level_spin.setValue(1)
        self.level_spin.valueChanged.connect(self.update_character)
        basic_layout.addRow("Nível:", self.level_spin)
        
        self.background_input = QLineEdit()
        self.background_input.textChanged.connect(self.update_character)
        basic_layout.addRow("Antecedente:", self.background_input)
        
        self.alignment_combo = QComboBox()
        alignments = ["Lawful Good", "Neutral Good", "Chaotic Good",
                     "Lawful Neutral", "Neutral", "Chaotic Neutral",
                     "Lawful Evil", "Neutral Evil", "Chaotic Evil"]
        self.alignment_combo.addItems(alignments)
        self.alignment_combo.currentTextChanged.connect(self.update_character)
        basic_layout.addRow("Alinhamento:", self.alignment_combo)
        
        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)
        
        stats_group = QGroupBox("Atributos")
        stats_layout = QVBoxLayout()
        
        roll_btn_layout = QHBoxLayout()
        self.roll_stats_btn = QPushButton("Rolar Atributos (4d6 manter 3 maiores)")
        self.roll_stats_btn.clicked.connect(self.roll_all_stats)
        roll_btn_layout.addWidget(self.roll_stats_btn)
        stats_layout.addLayout(roll_btn_layout)
        
        stats_form = QFormLayout()
        
        self.stat_inputs = {}
        stat_names = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']
        stat_labels = ['Força (STR)', 'Destreza (DEX)', 'Constituição (CON)', 
                      'Inteligência (INT)', 'Sabedoria (WIS)', 'Carisma (CHA)']
        
        for stat_name, label in zip(stat_names, stat_labels):
            stat_widget = QWidget()
            stat_layout = QHBoxLayout(stat_widget)
            stat_layout.setContentsMargins(0, 0, 0, 0)
            
            spin = QSpinBox()
            spin.setMinimum(1)
            spin.setMaximum(20)
            spin.setValue(10)
            spin.valueChanged.connect(self.update_character)
            stat_layout.addWidget(spin)
            
            roll_btn = QPushButton("🎲")
            roll_btn.setMaximumWidth(40)
            roll_btn.clicked.connect(lambda checked, s=stat_name: self.roll_single_stat(s))
            stat_layout.addWidget(roll_btn)
            
            modifier_label = QLabel("(+0)")
            modifier_label.setMinimumWidth(50)
            stat_layout.addWidget(modifier_label)
            
            self.stat_inputs[stat_name] = {
                'spin': spin,
                'modifier': modifier_label
            }
            
            stats_form.addRow(label, stat_widget)
        
        stats_layout.addLayout(stats_form)
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        skills_group = QGroupBox("Proficiências em Perícias")
        skills_layout = QVBoxLayout()
        
        self.available_skills_label = QLabel("Selecione suas perícias:")
        skills_layout.addWidget(self.available_skills_label)
        
        self.skills_list = QListWidget()
        self.skills_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.skills_list.itemSelectionChanged.connect(self.update_character)
        skills_layout.addWidget(self.skills_list)
        
        self.subrace_skills_label = QLabel("Perícias da Subraça:")
        self.subrace_skills_label.setVisible(False)
        skills_layout.addWidget(self.subrace_skills_label)
        
        self.subrace_skills_list = QListWidget()
        self.subrace_skills_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.subrace_skills_list.setVisible(False)
        self.subrace_skills_list.itemSelectionChanged.connect(self.update_character)
        skills_layout.addWidget(self.subrace_skills_list)
        
        skills_group.setLayout(skills_layout)
        layout.addWidget(skills_group)
        
        layout.addStretch()
    
    def roll_single_stat(self, stat_name: str):
        total, rolls = DiceRoller.roll_ability_score()
        self.stat_inputs[stat_name]['spin'].setValue(total)
        setattr(self.character.base_stats, stat_name, total)
        self.character.recalculate_stats()
        self.update_stats_display()
        QMessageBox.information(
            self, 
            "Rolagem de Atributo",
            f"Rolou 4d6 (manteve os 3 maiores)\nResultados: {rolls}\nTotal: {total}"
        )
    
    def roll_all_stats(self):
        results = []
        for stat_name in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']:
            total, rolls = DiceRoller.roll_ability_score()
            self.stat_inputs[stat_name]['spin'].setValue(total)
            setattr(self.character.base_stats, stat_name, total)
            results.append(f"{stat_name.capitalize()}: {total} (rolagens: {rolls})")
        
        self.character.recalculate_stats()
        self.update_stats_display()
        
        QMessageBox.information(
            self,
            "Rolagem de Atributos",
            "Todos os atributos foram rolados!\n\n" + "\n".join(results)
        )
    
    def on_race_changed(self, race_name: str):
        if race_name:
            self.character.set_race(race_name)
            self.character.set_subrace('None')
            # Atualizar subraças disponíveis
            self.subrace_combo.clear()
            subraces = SubraceDatabase.get_subraces_for_race(race_name)
            if subraces:
                self.subrace_combo.addItems(list(subraces.keys()))
            self.update_stats_display()
            self.character_updated.emit()
    
    def on_subrace_changed(self, subrace_name: str):
        if subrace_name:
            self.character.set_subrace(subrace_name)
            self.update_stats_display()
            self.update_skills_list()
            self.character_updated.emit()
    
    def on_class_changed(self, class_name: str):
        if class_name:
            self.character.set_class(class_name)
            self.update_skills_list()
            self.character_updated.emit()
    
    def update_skills_list(self):
        # Atualizar perícias da classe
        self.skills_list.clear()
        if self.character.character_class:
            available_skills = self.character.character_class.available_skills
            self.skills_list.addItems(available_skills)
            
            max_skills = self.character.character_class.skill_proficiencies_count
            self.available_skills_label.setText(
                f"Selecione {max_skills} perícias da classe:"
            )
        
        # Atualizar perícias da subraça (se houver)
        self.subrace_skills_list.clear()
        if self.character.subrace and self.character.subrace.skill_proficiencies_count > 0:
            # Mostrar lista de perícias da subraça
            self.subrace_skills_label.setVisible(True)
            self.subrace_skills_list.setVisible(True)
            
            # Lista completa de todas as perícias disponíveis
            all_skills = [
                'Acrobatics', 'Animal Handling', 'Arcana', 'Athletics', 'Deception',
                'History', 'Insight', 'Intimidation', 'Investigation', 'Medicine',
                'Nature', 'Perception', 'Performance', 'Persuasion', 'Religion',
                'Sleight of Hand', 'Stealth', 'Survival'
            ]
            self.subrace_skills_list.addItems(all_skills)
            
            subrace_max = self.character.subrace.skill_proficiencies_count
            self.subrace_skills_label.setText(
                f"Selecione {subrace_max} perícias da subraça ({self.character.subrace.name}):"
            )
        else:
            # Esconder lista de perícias da subraça
            self.subrace_skills_label.setVisible(False)
            self.subrace_skills_list.setVisible(False)
    
    def update_stats_display(self):
        for stat_name, widgets in self.stat_inputs.items():
            value = widgets['spin'].value()
            modifier = (value - 10) // 2
            sign = '+' if modifier >= 0 else ''
            widgets['modifier'].setText(f"({sign}{modifier})")
    
    def update_character(self):
        self.character.name = self.name_input.text()
        self.character.level = self.level_spin.value()
        self.character.background = self.background_input.text()
        self.character.alignment = self.alignment_combo.currentText()
        
        for stat_name, widgets in self.stat_inputs.items():
            value = widgets['spin'].value()
            setattr(self.character.base_stats, stat_name, value)
        
        self.character.recalculate_stats()
        
        # Validar perícias da classe
        selected_class_skills = [item.text() for item in self.skills_list.selectedItems()]
        if self.character.character_class:
            max_skills = self.character.character_class.skill_proficiencies_count
            if len(selected_class_skills) > max_skills:
                QMessageBox.warning(
                    self,
                    "Aviso",
                    f"Você pode selecionar no máximo {max_skills} perícias da classe."
                )
                return
        
        # Validar perícias da subraça
        selected_subrace_skills = [item.text() for item in self.subrace_skills_list.selectedItems()]
        if self.character.subrace and self.character.subrace.skill_proficiencies_count > 0:
            max_subrace_skills = self.character.subrace.skill_proficiencies_count
            if len(selected_subrace_skills) > max_subrace_skills:
                QMessageBox.warning(
                    self,
                    "Aviso",
                    f"Você pode selecionar no máximo {max_subrace_skills} perícias da subraça."
                )
                return
        
        # Combinar perícias de classe e subraça
        self.character.skill_proficiencies = selected_class_skills + selected_subrace_skills
        
        self.update_stats_display()
        self.character.update_derived_stats()
        self.character_updated.emit()
    
    def set_character(self, character: Character):
        self.character = character
        
        self.name_input.setText(character.name)
        self.level_spin.setValue(character.level)
        self.background_input.setText(character.background)
        
        if character.alignment:
            index = self.alignment_combo.findText(character.alignment)
            if index >= 0:
                self.alignment_combo.setCurrentIndex(index)
        
        if character.race:
            index = self.race_combo.findText(character.race.name)
            if index >= 0:
                self.race_combo.setCurrentIndex(index)
        
        if character.character_class:
            index = self.class_combo.findText(character.character_class.name)
            if index >= 0:
                self.class_combo.setCurrentIndex(index)
        
        if character.subrace:
            index = self.subrace_combo.findText(character.subrace.name)
            if index >= 0:
                self.subrace_combo.setCurrentIndex(index)
        
        for stat_name, widgets in self.stat_inputs.items():
            value = getattr(character.stats, stat_name)
            widgets['spin'].setValue(value)
        
        self.update_stats_display()
        self.update_skills_list()
        
        # Restaurar seleção de perícias da classe
        for i in range(self.skills_list.count()):
            item = self.skills_list.item(i)
            if item.text() in character.skill_proficiencies:
                item.setSelected(True)
        
        # Restaurar seleção de perícias da subraça
        for i in range(self.subrace_skills_list.count()):
            item = self.subrace_skills_list.item(i)
            if item.text() in character.skill_proficiencies:
                item.setSelected(True)
        