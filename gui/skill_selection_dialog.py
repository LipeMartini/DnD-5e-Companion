from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QListWidget, QListWidgetItem, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class SkillSelectionDialog(QDialog):
    """Dialog para seleção de skills (usado por College of Lore e outras features)"""
    
    def __init__(self, character, num_skills: int, title: str = "Escolher Skills", parent=None):
        super().__init__(parent)
        self.character = character
        self.num_skills = num_skills
        self.selected_skills = []
        
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(500, 600)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel(f"Escolha {self.num_skills} Skills")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Descrição
        desc = QLabel(f"Selecione {self.num_skills} perícias adicionais para ganhar proficiência.")
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        # Contador de seleções
        self.counter_label = QLabel(f"Selecionadas: 0/{self.num_skills}")
        self.counter_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.counter_label.setStyleSheet("color: #8B4513; padding: 5px;")
        layout.addWidget(self.counter_label)
        
        # Lista de skills disponíveis
        list_label = QLabel("Skills Disponíveis:")
        list_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(list_label)
        
        self.skills_list = QListWidget()
        self.skills_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.skills_list.itemSelectionChanged.connect(self.on_selection_changed)
        
        # Todas as skills do D&D 5e
        all_skills = [
            "Acrobatics", "Animal Handling", "Arcana", "Athletics",
            "Deception", "History", "Insight", "Intimidation",
            "Investigation", "Medicine", "Nature", "Perception",
            "Performance", "Persuasion", "Religion", "Sleight of Hand",
            "Stealth", "Survival"
        ]
        
        # Adiciona skills, marcando as que já tem proficiência
        for skill in sorted(all_skills):
            item = QListWidgetItem(skill)
            
            # Verifica se já tem proficiência
            if skill in self.character.skill_proficiencies:
                item.setText(f"{skill} (já possui)")
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
                item.setForeground(Qt.GlobalColor.gray)
            
            self.skills_list.addItem(item)
        
        layout.addWidget(self.skills_list)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        confirm_btn = QPushButton("Confirmar Seleção")
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: white;
                border: 2px solid #654321;
                border-radius: 5px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A0522D;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #666666;
            }
        """)
        confirm_btn.clicked.connect(self.confirm_selection)
        buttons_layout.addWidget(confirm_btn)
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #696969;
                color: white;
                border: 2px solid #654321;
                border-radius: 5px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #A0522D;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
    
    def on_selection_changed(self):
        """Atualiza contador quando seleção muda"""
        selected_items = self.skills_list.selectedItems()
        count = len(selected_items)
        
        self.counter_label.setText(f"Selecionadas: {count}/{self.num_skills}")
        
        # Muda cor do contador
        if count == self.num_skills:
            self.counter_label.setStyleSheet("color: green; padding: 5px; font-weight: bold;")
        elif count > self.num_skills:
            self.counter_label.setStyleSheet("color: red; padding: 5px; font-weight: bold;")
        else:
            self.counter_label.setStyleSheet("color: #8B4513; padding: 5px;")
    
    def confirm_selection(self):
        """Confirma seleção de skills"""
        selected_items = self.skills_list.selectedItems()
        count = len(selected_items)
        
        if count != self.num_skills:
            QMessageBox.warning(
                self,
                "Seleção Inválida",
                f"Você deve selecionar exatamente {self.num_skills} skills.\n"
                f"Atualmente selecionadas: {count}"
            )
            return
        
        # Extrai nomes das skills selecionadas
        self.selected_skills = [item.text() for item in selected_items]
        
        self.accept()
    
    def get_selected_skills(self):
        """Retorna lista de skills selecionadas"""
        return self.selected_skills
