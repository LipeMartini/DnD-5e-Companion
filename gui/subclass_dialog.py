from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QListWidget, QListWidgetItem, QTextEdit,
                             QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from models import SubclassDatabase

class SubclassDialog(QDialog):
    """Dialog para seleção de subclasse"""
    
    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character
        self.selected_subclass = None
        
        self.setWindowTitle("Escolher Subclasse")
        self.setModal(True)
        self.resize(700, 500)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel(f"Escolha sua Subclasse de {self.character.character_class.name}")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Descrição
        desc = QLabel(f"No nível {SubclassDatabase.get_selection_level(self.character.character_class.name)}, "
                     f"você deve escolher um arquétipo para sua classe.")
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        # Layout horizontal para lista e detalhes
        content_layout = QHBoxLayout()
        
        # Lista de subclasses
        list_layout = QVBoxLayout()
        list_label = QLabel("Subclasses Disponíveis:")
        list_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        list_layout.addWidget(list_label)
        
        self.subclass_list = QListWidget()
        self.subclass_list.currentItemChanged.connect(self.on_subclass_selected)
        
        # Preenche lista de subclasses
        subclasses = SubclassDatabase.get_subclasses_for_class(self.character.character_class.name)
        for subclass_name in subclasses.keys():
            item = QListWidgetItem(subclass_name)
            self.subclass_list.addItem(item)
        
        list_layout.addWidget(self.subclass_list)
        content_layout.addLayout(list_layout)
        
        # Detalhes da subclasse
        details_layout = QVBoxLayout()
        details_label = QLabel("Detalhes:")
        details_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        details_layout.addWidget(details_label)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        details_layout.addWidget(self.details_text)
        
        content_layout.addLayout(details_layout)
        layout.addLayout(content_layout)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        select_btn = QPushButton("Selecionar Subclasse")
        select_btn.setStyleSheet("""
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
        """)
        select_btn.clicked.connect(self.accept_selection)
        buttons_layout.addWidget(select_btn)
        
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
        
        # Seleciona primeiro item por padrão
        if self.subclass_list.count() > 0:
            self.subclass_list.setCurrentRow(0)
    
    def on_subclass_selected(self, current, previous):
        """Atualiza detalhes quando uma subclasse é selecionada"""
        if not current:
            return
        
        subclass_name = current.text()
        subclass = SubclassDatabase.get_subclass(self.character.character_class.name, subclass_name)
        
        if subclass:
            # Monta texto de detalhes
            details = f"<h3>{subclass.name}</h3>"
            details += f"<p><i>{subclass.description}</i></p>"
            details += "<h4>Features:</h4>"
            
            # Agrupa features por nível
            features_by_level = {}
            for feature in subclass.features:
                if feature.level not in features_by_level:
                    features_by_level[feature.level] = []
                features_by_level[feature.level].append(feature)
            
            # Exibe features organizadas por nível
            for level in sorted(features_by_level.keys()):
                details += f"<p><b>Nível {level}:</b></p>"
                for feature in features_by_level[level]:
                    details += f"<p><b>{feature.name}:</b> {feature.description}</p>"
            
            self.details_text.setHtml(details)
    
    def accept_selection(self):
        """Confirma seleção da subclasse"""
        current_item = self.subclass_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione uma subclasse.")
            return
        
        self.selected_subclass = current_item.text()
        self.accept()
    
    def get_selected_subclass(self):
        """Retorna a subclasse selecionada"""
        return self.selected_subclass
