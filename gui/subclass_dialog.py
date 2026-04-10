from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QListWidget, QListWidgetItem, QTextEdit,
                             QMessageBox, QComboBox, QDialogButtonBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from models import SubclassDatabase

class SubclassDialog(QDialog):
    """Dialog para seleção de subclasse"""
    
    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character
        self.selected_subclass = None
        self.additional_data = {}
        
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
        self.available_subclasses = SubclassDatabase.get_subclasses_for_class(self.character.character_class.name)
        for subclass_name in sorted(self.available_subclasses.keys()):
            subclass = self.available_subclasses[subclass_name]
            display_name = subclass_name
            if SubclassDatabase.is_optional_source(subclass):
                source_label = SubclassDatabase.get_source_label(subclass)
                display_name = f"{subclass_name} [{source_label}]"
            item = QListWidgetItem(display_name)
            item.setData(Qt.ItemDataRole.UserRole, subclass_name)
            item.setToolTip(subclass.description)
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
        
        self.select_button = QPushButton("Selecionar Subclasse")
        self.select_button.setStyleSheet("""
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
        self.select_button.clicked.connect(self.accept_selection)
        buttons_layout.addWidget(self.select_button)
        
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
        
        # Seleciona primeiro item por padrão ou desabilita se vazio
        if self.subclass_list.count() > 0:
            self.subclass_list.setCurrentRow(0)
        else:
            self.subclass_list.setEnabled(False)
            self.select_button.setEnabled(False)
            self.details_text.setHtml(
                """
                <p><b>Nenhuma subclasse disponível.</b></p>
                <p>Ative o conteúdo opcional correspondente nas Configurações para liberar novas opções.</p>
                """
            )
    
    def on_subclass_selected(self, current, previous):
        """Atualiza detalhes quando uma subclasse é selecionada"""
        if not current:
            return
        
        subclass_name = current.data(Qt.ItemDataRole.UserRole) or current.text()
        subclass = SubclassDatabase.get_subclass(self.character.character_class.name, subclass_name)
        
        if subclass:
            # Monta texto de detalhes
            details = f"<h3>{subclass.name}</h3>"
            details += f"<p><i>{subclass.description}</i></p>"
            source_label = SubclassDatabase.get_source_label(subclass)
            if source_label:
                optional_badge = " (Conteúdo opcional)" if SubclassDatabase.is_optional_source(subclass) else ""
                details += f"<p><b>Fonte:</b> {source_label}{optional_badge}</p>"
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
        
        self.selected_subclass = current_item.data(Qt.ItemDataRole.UserRole) or current_item.text()

        # Solicita arma para Bladesinging
        if self.selected_subclass == "Bladesinging":
            weapon_dialog = QDialog(self)
            weapon_dialog.setWindowTitle("Bladesinging - Escolha a Arma")
            layout = QVBoxLayout(weapon_dialog)
            layout.addWidget(QLabel("Escolha a arma corpo-a-corpo de uma mão com a qual deseja proficiência:"))
            weapon_combo = QComboBox()
            weapon_combo.addItems([
                "Longsword", "Shortsword", "Rapier", "Scimitar", "Battleaxe",
                "Warhammer", "Whip"
            ])
            layout.addWidget(weapon_combo)
            buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(weapon_dialog.accept)
            buttons.rejected.connect(weapon_dialog.reject)
            layout.addWidget(buttons)
            if weapon_dialog.exec() != QDialog.DialogCode.Accepted:
                return
            self.additional_data["bladesinger_weapon"] = weapon_combo.currentText()
        
        self.accept()
    
    def get_selection(self):
        """Retorna a subclasse selecionada e dados adicionais (se houver)."""
        return self.selected_subclass, self.additional_data
