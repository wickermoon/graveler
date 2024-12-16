import PyQt6.QtCore
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QToolBar, QMessageBox

from Preferences import Preferences
from WeekTab import WeekTab
from ListTab import ListTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setFixedSize(1024, 768)

        self.tabs = QTabWidget()
        for tab_name in ['I', 'II', 'III', 'IV']:
            self.tabs.addTab(WeekTab(tab_name), tab_name)

        self.preferences = Preferences()
        self.tabs.addTab(self.preferences, 'Preferences')

        self.setCentralWidget(self.tabs)

        toolbar = QToolBar('Main Toolbar')
        toolbar.movable = False
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
            for tab_index in range(0, self.tabs.count()):
                tab = self.tabs.widget(tab_index)
                if isinstance(tab, ListTab):
                    tab.save_data()
            self.on_preferences_changed()

    def on_load(self):
        button = QMessageBox.question(self, f'Reload preferences', 'Reload all preferences without saving?')

        if button == QMessageBox.StandardButton.Yes:
            self.preferences.reload_data()

    def on_preferences_changed(self):
        for tab_index in range(0, self.tabs.count()):
            tab = self.tabs.widget(tab_index)

            if isinstance(tab, WeekTab):
                tab.refresh()
