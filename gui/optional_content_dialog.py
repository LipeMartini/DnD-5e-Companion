from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QPushButton,
    QFrame,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal

from models import AppSettings


class OptionalContentDialog(QDialog):
    """Dialog to enable/disable optional game content (Tasha's / Xanathar's)."""

    content_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Conteúdos Opcionais")
        self.setModal(True)
        self.setMinimumWidth(420)

        self.settings = AppSettings.load()
        self.optional_content = self.settings.get("optional_content", {})

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("Escolha quais livros opcionais deseja carregar")
        title.setFont(QFont("Georgia", 12, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #5D4037;")
        layout.addWidget(title)

        description = QLabel(
            "As magias e demais recursos destes livros são carregados instantaneamente ao ativar os toggles."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #3E2723;")
        layout.addWidget(description)

        layout.addWidget(self._create_toggle_panel())

        button_row = QHBoxLayout()
        button_row.addStretch()
        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.accept)
        button_row.addWidget(close_btn)
        layout.addLayout(button_row)

    def _create_toggle_panel(self) -> QFrame:
        panel = QFrame()
        panel.setStyleSheet(
            """
            QFrame {
                background-color: #FFF8DC;
                border: 2px solid #8B4513;
                border-radius: 8px;
                padding: 12px;
            }
            """
        )
        box_layout = QVBoxLayout(panel)
        box_layout.setSpacing(15)

        self.tashas_checkbox = QCheckBox("Tasha's Cauldron of Everything")
        self.tashas_checkbox.setChecked(self.optional_content.get("tashas_spells", False))
        self.tashas_checkbox.toggled.connect(
            lambda checked: self._handle_toggle("tashas_spells", checked)
        )
        self._style_checkbox(self.tashas_checkbox)
        box_layout.addWidget(self.tashas_checkbox)

        tashas_hint = QLabel("Inclui magias, estilos, subclasses e outras opções adicionais introduzidas em Tasha's.")
        tashas_hint.setWordWrap(True)
        tashas_hint.setStyleSheet("color: #5D4037; font-size: 11px;")
        box_layout.addWidget(tashas_hint)

        self.xanathar_checkbox = QCheckBox("Xanathar's Guide to Everything")
        self.xanathar_checkbox.setChecked(self.optional_content.get("xanathars_spells", False))
        self.xanathar_checkbox.toggled.connect(
            lambda checked: self._handle_toggle("xanathars_spells", checked)
        )
        self._style_checkbox(self.xanathar_checkbox)
        box_layout.addWidget(self.xanathar_checkbox)

        xan_hint = QLabel("Adiciona magias, subclasses e ferramentas expandidas de Xanathar.")
        xan_hint.setWordWrap(True)
        xan_hint.setStyleSheet("color: #5D4037; font-size: 11px;")
        box_layout.addWidget(xan_hint)

        return panel

    def _style_checkbox(self, checkbox: QCheckBox) -> None:
        checkbox.setFont(QFont("Georgia", 11, QFont.Weight.Bold))
        checkbox.setStyleSheet(
            """
            QCheckBox {
                color: #3E2723;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #8B4513;
                background: #F5EBDC;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4CAF50;
                background: #81C784;
                border-radius: 4px;
            }
            """
        )

    def _handle_toggle(self, flag_key: str, value: bool) -> None:
        AppSettings.set_optional_content_flag(flag_key, value)
        self.optional_content[flag_key] = value
        self.content_changed.emit()
