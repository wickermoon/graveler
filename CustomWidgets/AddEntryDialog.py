from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit


class AddEntryDialog(QDialog):
    def __init__(self, title: str, name: str = None, amount: str = None):
        super().__init__()

        self.valid_input = False

        self.setWindowTitle(title)
        self.buttonBox = QDialogButtonBox((QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel))
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(super().reject)

        self.name = QLineEdit()
        self.name.setText(name)
        self.name.setPlaceholderText('Name')

        self.amount = QLineEdit()
        self.amount.setText(amount)
        self.amount.setPlaceholderText('Amount')

        validator = QDoubleValidator()
        validator.setDecimals(2)
        validator.setBottom(0)
        self.amount.setValidator(validator)

        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(self.amount)
        dialog_layout.addWidget(self.name)
        dialog_layout.addWidget(self.buttonBox)

        self.setLayout(dialog_layout)

        if amount is not None:
            self.amount.setFocus()

    def accept(self):
        is_error = False

        for line_edit in [self.name, self.amount]:
            if len(line_edit.text()) == 0:
                line_edit.setStyleSheet('border: 2px outset red; padding-left: 6px; border-radius: 5px')
                is_error = True
            else:
                self.name.setStyleSheet('')

        if not is_error:
            super().accept()
