from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QWidget
# noinspection PyUnresolvedReferences
from __feature__ import snake_case, true_property


class MoneyLabel(QLabel):
    def __init__(self, text: Optional[str] = '', parent: Optional[QWidget] = None):
        super().__init__(text, parent)

        self.alignment = Qt.AlignmentFlag.AlignRight
        self.style_sheet = 'margin-right:8px'
        self.font = QFont('Cascadia Mono')