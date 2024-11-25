from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QToolBar, QMessageBox

from Preferences import Preferences


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setFixedSize(1024, 768)

        self.preferences = Preferences()

        tabs = QTabWidget()

        for color in ['I', 'II', 'III', 'IV']:
            tabs.addTab(QWidget(), color)

        tabs.addTab(self.preferences, 'Preferences')

        self.setCentralWidget(tabs)

        toolbar = QToolBar('Main Toolbar')
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        save_action = QAction('Save', self)
        save_action.setStatusTip('Save current preferences')
        save_action.triggered.connect(self.on_save)

        load_action = QAction('Load', self)
        load_action.setStatusTip('Reload preferences')
        load_action.triggered.connect(self.on_load)

        toolbar.addAction(save_action)
        toolbar.addAction(load_action)

    def on_save(self):
        button = QMessageBox.question(self, f'Save preferences', 'Save preferences?')

        if button == QMessageBox.StandardButton.Yes:
            # save data to files
            pass

    def on_load(self):
        button = QMessageBox.question(self, f'Reload preferences', 'Reload all preferences without saving?')

        if button == QMessageBox.StandardButton.Yes:
            self.preferences.reload_data()
