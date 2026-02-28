from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QPushButton, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from models import Character
from .character_creation_tab import CharacterCreationTab
from .character_sheet_tab import CharacterSheetTab
from .dice_roller_tab import DiceRollerTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.character = Character()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("D&D 5e Character Builder")
        self.setGeometry(100, 100, 1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        button_layout = QHBoxLayout()
        
        self.new_char_btn = QPushButton("Nova Ficha")
        self.new_char_btn.clicked.connect(self.new_character)
        button_layout.addWidget(self.new_char_btn)
        
        self.save_btn = QPushButton("Salvar Ficha")
        self.save_btn.clicked.connect(self.save_character)
        button_layout.addWidget(self.save_btn)
        
        self.load_btn = QPushButton("Carregar Ficha")
        self.load_btn.clicked.connect(self.load_character)
        button_layout.addWidget(self.load_btn)
        
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        self.tabs = QTabWidget()
        
        self.creation_tab = CharacterCreationTab(self.character)
        self.creation_tab.character_updated.connect(self.on_character_updated)
        self.tabs.addTab(self.creation_tab, "Criação de Personagem")
        
        self.sheet_tab = CharacterSheetTab(self.character)
        self.tabs.addTab(self.sheet_tab, "Ficha Completa")
        
        self.dice_tab = DiceRollerTab(self.character)
        self.tabs.addTab(self.dice_tab, "Rolagem de Dados")
        
        main_layout.addWidget(self.tabs)
    
    def on_character_updated(self):
        """Atualiza todas as abas quando o personagem é modificado"""
        self.sheet_tab.update_display()
        self.dice_tab.update_character(self.character)
    
    def new_character(self):
        reply = QMessageBox.question(
            self, 
            'Nova Ficha',
            'Deseja criar uma nova ficha? Alterações não salvas serão perdidas.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.character = Character()
            self.creation_tab.set_character(self.character)
            self.sheet_tab.set_character(self.character)
            self.dice_tab.update_character(self.character)
            self.on_character_updated()
    
    def save_character(self):
        if not self.character.name:
            QMessageBox.warning(self, "Aviso", "Por favor, dê um nome ao personagem antes de salvar.")
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Ficha de Personagem",
            f"{self.character.name}.json",
            "JSON Files (*.json)"
        )
        
        if filepath:
            try:
                self.character.save_to_file(filepath)
                QMessageBox.information(self, "Sucesso", f"Ficha salva em:\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar ficha:\n{str(e)}")
    
    def load_character(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Carregar Ficha de Personagem",
            "",
            "JSON Files (*.json)"
        )
        
        if filepath:
            try:
                self.character = Character.load_from_file(filepath)
                self.creation_tab.set_character(self.character)
                self.sheet_tab.set_character(self.character)
                self.dice_tab.update_character(self.character)
                self.on_character_updated()
                QMessageBox.information(self, "Sucesso", "Ficha carregada com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao carregar ficha:\n{str(e)}")
