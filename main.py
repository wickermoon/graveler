import sys

from PySide6.QtWidgets import QApplication
from __feature__ import snake_case, true_property

from MainWindow import MainWindow

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
