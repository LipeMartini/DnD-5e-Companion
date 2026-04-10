from typing import Dict, List, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
)

from models import SpellDatabase, Spell


class CantripSelectionDialog(QDialog):
    """Dialog genérico para escolher cantrips de uma lista específica."""

    def __init__(
        self,
        spell_class: str,
        quantity: int,
        parent=None,
        excluded_spells: Optional[List[str]] = None,
    ):
        super().__init__(parent)
        self.spell_class = spell_class
        self.quantity = quantity
        self.excluded_spells = set(excluded_spells or [])
        self.available_spells: Dict[str, Spell] = {}

        self.setWindowTitle(f"Selecionar Truques - {self.spell_class}")
        self.setMinimumSize(500, 500)

        self._build_ui()
        self._load_spells()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel(
            f"Escolha {self.quantity} truque(s) da lista de {self.spell_class}."
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)

        self.selection_hint = QLabel()
        self.selection_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.selection_hint)

        content_layout = QHBoxLayout()
        layout.addLayout(content_layout)

        self.cantrip_list = QListWidget()
        self.cantrip_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.cantrip_list.itemSelectionChanged.connect(self._on_selection_changed)
        content_layout.addWidget(self.cantrip_list, 1)

        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setPlaceholderText("Selecione um truque para ver os detalhes.")
        content_layout.addWidget(self.details_text, 1)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.confirm_button = QPushButton("Confirmar")
        self.confirm_button.clicked.connect(self._on_confirm)
        self.confirm_button.setEnabled(False)
        buttons_layout.addWidget(self.confirm_button)

        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

    def _load_spells(self):
        spells = SpellDatabase.get_spells_by_level(0, self.spell_class)
        if self.excluded_spells:
            spells = {
                name: spell
                for name, spell in spells.items()
                if name not in self.excluded_spells
            }

        self.available_spells = spells
        self.cantrip_list.clear()

        for spell_name in sorted(spells.keys()):
            item = QListWidgetItem(spell_name)
            item.setData(Qt.ItemDataRole.UserRole, spells[spell_name])
            self.cantrip_list.addItem(item)

        self._update_selection_hint()
        if not self.has_sufficient_options():
            self.confirm_button.setEnabled(False)
            if not spells:
                self.selection_hint.setText(
                    "Nenhum truque disponível nessa lista."  # noqa: E501
                )
            else:
                self.selection_hint.setText(
                    "Não há truques suficientes disponíveis para completar a seleção."
                )

    def has_sufficient_options(self) -> bool:
        """Retorna True se há cantrips suficientes para cumprir o requisito."""
        return len(self.available_spells) >= self.quantity

    def _on_selection_changed(self):
        selected_items = self.cantrip_list.selectedItems()
        if selected_items:
            spell = selected_items[-1].data(Qt.ItemDataRole.UserRole)
            if spell:
                details = (
                    f"<h3>{spell.name}</h3>"
                    f"<p><b>Escola:</b> {spell.school}<br>"
                    f"<b>Tempo de Conjuração:</b> {spell.casting_time}<br>"
                    f"<b>Alcance:</b> {spell.range}<br>"
                    f"<b>Componentes:</b> {spell.components}<br>"
                    f"<b>Duração:</b> {spell.duration}</p>"
                    f"<p>{spell.description.replace(chr(10), '<br>')}</p>"
                )
                self.details_text.setHtml(details)
        else:
            self.details_text.clear()

        self._update_selection_hint()

    def _update_selection_hint(self):
        selected_count = len(self.cantrip_list.selectedItems())
        self.selection_hint.setText(
            f"Selecionados: {selected_count} / {self.quantity}"
        )
        self.confirm_button.setEnabled(
            self.has_sufficient_options() and selected_count == self.quantity
        )

    def _on_confirm(self):
        if len(self.cantrip_list.selectedItems()) != self.quantity:
            QMessageBox.warning(
                self,
                "Seleção incompleta",
                f"Você deve escolher exatamente {self.quantity} truque(s).",
            )
            return
        self.accept()

    def get_selected_cantrips(self) -> List[str]:
        return [item.text() for item in self.cantrip_list.selectedItems()]
