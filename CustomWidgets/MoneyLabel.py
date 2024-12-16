from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QWidget


class MoneyLabel(QLabel):
    def __init__(self, text: Optional[str] = '', parent: Optional[QWidget] = None):
        super().__init__(text, parent)

        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setStyleSheet('margin-right:8px')
        self.setFont(QFont('Cascadia Mono'))