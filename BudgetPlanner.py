import logging
import os.path
import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
# noinspection PyUnresolvedReferences
from __feature__ import snake_case, true_property

from MainWindow import MainWindow

logging.basicConfig(filename='error.log', level=logging.INFO)

class MainClass(object):
    def __init__(self):
        self.lockfile = os.path.normpath('lockfile')
        self.return_value = 0
        self.main_window = None

        try:
            if os.path.exists(self.lockfile):
                os.unlink(self.lockfile)
            self.fd = os.open(self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            self.is_running = False
        except OSError:
            _, value, _ = sys.exc_info()
            if value.errno == 13:
                logging.info("App is already running, closing myself again.")
                self.is_running = True
            self.return_value = value.errno
        self.initialized = True

    def __del__(self):
        if not self.initialized:
            return

        try:
            if hasattr(self, 'fd'):
                os.close(self.fd)
                os.unlink(self.lockfile)
        except Exception as e:
            logging.warning(e)

    def run(self):
        app = QApplication(sys.argv)

        self.main_window = MainWindow()
        self.main_window.show()

        system_tray = QSystemTrayIcon(QIcon('sys_tray3.png'))
        system_tray.tool_tip = 'Budget Planner'
        system_tray.show()
        system_tray.activated.connect(self.on_sys_tray_activated)

        exit_action = QAction('Exit')
        exit_action.triggered.connect(self.on_exit)

        sys_tray_menu = QMenu('')
        sys_tray_menu.add_action(exit_action)
        system_tray.set_context_menu(sys_tray_menu)

        self.return_value = app.exec()

    def on_sys_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self.main_window.is_hidden():
                self.main_window.show()

    @staticmethod
    def on_exit():
        QCoreApplication.exit()

if __name__ == "__main__":
    mc = MainClass()

    if not mc.is_running:
        mc.run()

    return_value = mc.return_value
    del mc
    sys.exit(return_value)
