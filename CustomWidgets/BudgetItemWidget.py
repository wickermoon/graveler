from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
# noinspection PyUnresolvedReferences
from __feature__ import snake_case, true_property


class BudgetItemWidget(QWidget):
    def __init__(self, name: str, amount: str):
        super().__init__()

        self.font = QFont('Cascadia Mono')

        self.name = QLabel(name)
        self.amount = QLabel(f'{float(amount):.2f}')
        self.amount.alignment = Qt.AlignmentFlag.AlignRight

        layout = QHBoxLayout()
        layout.add_widget(self.name)
        layout.add_widget(self.amount)

        self.set_layout(layout)
