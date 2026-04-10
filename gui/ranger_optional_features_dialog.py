from __future__ import annotations

from dataclasses import dataclass

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QGroupBox,
    QLabel,
    QRadioButton,
    QVBoxLayout,
)

from models import AppSettings


@dataclass
class RangerOptionalSelection:
    favored_choice: str = "phb"
    explorer_choice: str = "phb"


class RangerOptionalFeaturesDialog(QDialog):
    """Dialog that lets Rangers opt into Tasha's optional features."""

    def __init__(self, *, include_level1: bool, parent=None):
        super().__init__(parent)
        self.include_level1 = include_level1
        self.selection = RangerOptionalSelection()

        self.setWindowTitle("Opções de Ranger - Tasha's")
        self.setModal(True)
        self.setMinimumWidth(540)

        self._favored_group: QButtonGroup | None = None
        self._explorer_group: QButtonGroup | None = None

        self._build_ui()

    def has_choices(self) -> bool:
        return self.include_level1

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(14)

        intro = QLabel(
            "<b>Tasha's Cauldron of Everything</b> oferece substituições para as features iniciais do Ranger."
            " Escolha abaixo quais versões deseja manter nesta ficha."
        )
        intro.setWordWrap(True)
        intro.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(intro)

        if self.include_level1:
            layout.addWidget(self._build_level1_section())

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _build_level1_section(self) -> QFrame:
        container = QFrame()
        frame_layout = QVBoxLayout(container)
        frame_layout.setSpacing(12)

        title = QLabel("<b>Nível 1</b> — escolha entre as versões do Player's Handbook e Tasha's")
        frame_layout.addWidget(title)

        self._favored_group = QButtonGroup(self)
        frame_layout.addWidget(self._build_radio_pair(
            group=self._favored_group,
            header="Inimigo Favorito vs Favored Foe",
            phb_label="Favored Enemy (PHB)",
            phb_desc="Listas de inimigos favoritos, vantagem em Sobrevivência/Inteligência contra eles.",
            tasha_label="Favored Foe (Tasha's)",
            tasha_desc="Marca um inimigo e causa dano extra algumas vezes por dia.",
            default_phb=True,
        ))

        self._explorer_group = QButtonGroup(self)
        frame_layout.addWidget(self._build_radio_pair(
            group=self._explorer_group,
            header="Explorador Natural vs Deft Explorer",
            phb_label="Natural Explorer (PHB)",
            phb_desc="Especialização em um terreno favorito, viagem facilitada nesse bioma.",
            tasha_label="Deft Explorer (Tasha's)",
            tasha_desc="Benefícios versáteis: Canny, Roving e Tireless substituem o terreno favorito.",
            default_phb=True,
        ))

        return container

    def _build_radio_pair(
        self,
        *,
        group: QButtonGroup,
        header: str,
        phb_label: str,
        phb_desc: str,
        tasha_label: str,
        tasha_desc: str,
        default_phb: bool,
    ) -> QGroupBox:
        box = QGroupBox(header)
        box_layout = QVBoxLayout(box)
        box_layout.setSpacing(6)

        phb_radio = QRadioButton(phb_label)
        phb_radio.setToolTip(phb_desc)
        tasha_radio = QRadioButton(tasha_label)
        tasha_radio.setToolTip(tasha_desc)

        group.addButton(phb_radio, 0)
        group.addButton(tasha_radio, 1)

        if default_phb:
            phb_radio.setChecked(True)
        else:
            tasha_radio.setChecked(True)

        box_layout.addWidget(phb_radio)
        box_layout.addWidget(self._info_label(phb_desc))
        box_layout.addWidget(tasha_radio)
        box_layout.addWidget(self._info_label(tasha_desc))
        return box

    @staticmethod
    def _info_label(text: str) -> QLabel:
        label = QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet("color: #555; font-size: 11px;")
        return label

    def get_selection(self) -> RangerOptionalSelection:
        if self._favored_group:
            self.selection.favored_choice = "tasha" if self._favored_group.checkedId() == 1 else "phb"

        if self._explorer_group:
            self.selection.explorer_choice = "tasha" if self._explorer_group.checkedId() == 1 else "phb"

        return self.selection


def apply_ranger_optional_features(parent, character, new_features: list[str]) -> list[str]:
    """Apply Ranger optional feature swaps if Tasha's toggle is enabled."""

    if not AppSettings.get_optional_content_flag("tashas_spells"):
        return new_features

    if not character.character_class or character.character_class.name != "Ranger":
        return new_features

    gained_level1 = any(name in {"Favored Enemy", "Natural Explorer"} for name in new_features)
    if not gained_level1:
        return new_features

    dialog = RangerOptionalFeaturesDialog(
        include_level1=gained_level1,
        parent=parent,
    )

    if not dialog.has_choices():
        return new_features

    if dialog.exec() != QDialog.DialogCode.Accepted:
        return new_features

    selection = dialog.get_selection()
    updated_features = list(new_features)

    _apply_level1_choices(character, updated_features, selection)
    return updated_features


def _apply_level1_choices(character, updated_features: list[str], selection: RangerOptionalSelection) -> None:
    favored_target = "Favored Foe" if selection.favored_choice == "tasha" else "Favored Enemy"
    explorer_target = "Deft Explorer" if selection.explorer_choice == "tasha" else "Natural Explorer"

    _replace_feature(character, "Favored Enemy", favored_target, updated_features)
    _replace_feature(character, "Natural Explorer", explorer_target, updated_features)


def _replace_feature(character, original: str, replacement: str, updated_features: list[str]) -> None:
    if original == replacement:
        _ensure_feature(character, original, updated_features)
        return

    _remove_feature(character, original, updated_features)
    _ensure_feature(character, replacement, updated_features)


def _ensure_feature(character, feature_name: str, updated_features: list[str]) -> None:
    if feature_name not in character.class_features:
        character.class_features.append(feature_name)
        if feature_name not in updated_features:
            updated_features.append(feature_name)


def _remove_feature(character, feature_name: str, updated_features: list[str]) -> None:
    if feature_name in character.class_features:
        character.class_features.remove(feature_name)
    if feature_name in updated_features:
        updated_features.remove(feature_name)
