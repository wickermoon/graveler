import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
# noinspection PyUnresolvedReferences
from __feature__ import snake_case, true_property

from MainWindow import MainWindow


def on_sys_tray_activated(reason):
    if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
        if window.is_hidden():
            window.show()

def on_exit():
    QCoreApplication.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    system_tray = QSystemTrayIcon(QIcon('sys_tray3.png'))
    system_tray.tool_tip = 'Budget Planner'
    system_tray.show()
    system_tray.activated.connect(on_sys_tray_activated)

    exit_action = QAction('Exit')
    exit_action.triggered.connect(on_exit)

    sys_tray_menu = QMenu('')
    sys_tray_menu.add_action(exit_action)
    system_tray.set_context_menu(sys_tray_menu)

    sys.exit(app.exec())
