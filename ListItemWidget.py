from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel


class ListItemWidget(QWidget):
    def __init__(self, name: str, amount: str):
        super().__init__()

        self.setFont(QFont('Cascadia Mono'))

        self.name = QLabel(name)
        self.amount = QLabel(f'{float(amount):.2f}')
        self.amount.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout = QHBoxLayout()
        layout.addWidget(self.name)
        layout.addWidget(self.amount)

        self.setLayout(layout)
