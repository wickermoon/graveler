from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QTabWidget, QToolBar, QMessageBox
# noinspection PyUnresolvedReferences
from __feature__ import snake_case, true_property

import core
from CustomWidgets.Preferences import Preferences
from CustomWidgets.WeekTab import WeekTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.window_title = "My App"
        self.set_fixed_size(1024, 768)

        self.tabs = QTabWidget()
        for tab_name in ['I', 'II', 'III', 'IV']:
            self.tabs.add_tab(WeekTab(tab_name), tab_name)

        self.preferences = Preferences()
        self.tabs.add_tab(self.preferences, 'Preferences')

        self.set_central_widget(self.tabs)

        toolbar = QToolBar('Main Toolbar')
        toolbar.movable = False
        self.add_tool_bar(toolbar)

        save_action = QAction('Save', self)
        save_action.status_tip = 'Save current preferences'
        save_action.triggered.connect(self.on_save)

        load_action = QAction('Load', self)
        load_action.status_tip = 'Reload preferences'
        load_action.triggered.connect(self.on_load)

        toolbar.add_action(save_action)
        toolbar.add_action(load_action)

    def on_save(self):
        week_list = list()
        for tab_index in range(0, self.tabs.count):
            tab = self.tabs.widget(tab_index)
            if isinstance(tab, Preferences):
                tab.save_data()
            elif isinstance(tab, WeekTab):
                week_list.append(tab.save_data())

        with open(core.filepath, 'w+') as file:
            for week in week_list:
                for entry in week:
                    file.write(entry)

        self.on_preferences_changed()

    def on_load(self):
        button = QMessageBox.question(self, f'Reload preferences', 'Reload all preferences without saving?', (QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No), QMessageBox.StandardButton.No)

        if button == QMessageBox.StandardButton.Yes:
            self.preferences.reload_data()

    def on_preferences_changed(self):
        for tab_index in range(0, self.tabs.count):
            tab = self.tabs.widget(tab_index)

            if isinstance(tab, WeekTab):
                tab.refresh()

    def close_event(self, event):
        event.ignore()
        self.hide()