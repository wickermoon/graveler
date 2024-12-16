from typing import Optional

from PySide6.QtCore import QObject, QEvent
from PySide6.QtGui import QContextMenuEvent
from PySide6.QtWidgets import QWidget
from __feature__ import snake_case, true_property

from CustomWidgets import ListContextMenu


class ListTab(QWidget):
    def __init__(self):
        super().__init__()

    # noinspection PyTypeChecker
    def event_filter(self, source: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.ContextMenu:
            self.show_context_menu(source, event)
            return True

        return super().event_filter(source, event)

    # noinspection PyTypeChecker
    def show_context_menu(self, source: QObject, event: QContextMenuEvent, text: Optional[str] = '<Template>') -> ListContextMenu:
        context = ListContextMenu.ListContextMenu(self, source, event, text)
        context.exec(event.global_pos())

    def update_list_total(self):
        pass

    def save_data(self):
        pass