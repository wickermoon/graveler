from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit
from __feature__ import snake_case, true_property

class AddEntryDialog(QDialog):
    def __init__(self, title: str, name: str = None, amount: str = None):
        super().__init__()

        self.valid_input = False

        self.window_title = title
        self.buttonBox = QDialogButtonBox((QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel))
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(super().reject)

        self.name = QLineEdit()
        self.name.text = name
        self.name.placeholder_text = 'Name'

        self.amount = QLineEdit()
        self.amount.text = amount
        self.amount.placeholder_text = 'Amount'

        validator = QDoubleValidator()
        validator.decimals = 2
        validator.bottom = 0
        self.amount.set_validator(validator)

        dialog_layout = QVBoxLayout()
        dialog_layout.add_widget(self.amount)
        dialog_layout.add_widget(self.name)
        dialog_layout.add_widget(self.buttonBox)

        self.set_layout(dialog_layout)

        if amount is not None:
            self.amount.set_focus()

    def accept(self):
        is_error = False

        for line_edit in [self.name, self.amount]:
            if len(line_edit.text) == 0:
                line_edit.style_sheet = 'border: 2px outset red; padding-left: 6px; border-radius: 5px'
                is_error = True
            else:
                self.name.style_sheet = ''

        if not is_error:
            super().accept()
