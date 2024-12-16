from PySide6.QtGui import QContextMenuEvent, QAction
from PySide6.QtWidgets import QMenu, QListWidget, QListWidgetItem, QMessageBox
# noinspection PyUnresolvedReferences
from __feature__ import snake_case, true_property

from CustomWidgets.AddEntryDialog import AddEntryDialog
from CustomWidgets.BudgetItemWidget import BudgetItemWidget
from ListTab import ListTab


class ListContextMenu(QMenu):
    def __init__(self, parent, source: QListWidget, event: QContextMenuEvent, text: str):
        super().__init__(parent)

        self.parent: ListTab = parent
        self.source = source
        self.text = text

        self.selected_item = self.source.item_at(event.pos())

        new = QAction(f'Add {text}...', self)
        new.tool_tip = f'Adds a new fixed {text.lower()} to the list.'
        new.triggered.connect(self.on_new)
        self.add_action(new)

        if self.selected_item is not None:
            proxy: BudgetItemWidget = self.source.item_widget(self.selected_item)

            edit_item = QAction(f'Edit {proxy.name.text}...', self)
            edit_item.tool_tip = f'Edits {proxy.name.text}'
            edit_item.triggered.connect(self.on_edit)
            self.add_action(edit_item)

            remove = QAction(f'Remove {proxy.name.text}...', self)
            remove.tool_tip = f'Removes {proxy.name.text} from the list.'
            remove.triggered.connect(self.on_remove)
            self.add_action(remove)

    def on_new(self):
        dlg = AddEntryDialog(f'Add {self.text.lower()}')

        if dlg.exec():
            item_widget = BudgetItemWidget(dlg.name.text, dlg.amount.text)
            new_item = QListWidgetItem(self.source)
            new_item.set_size_hint(item_widget.size_hint)

            self.source.add_item(new_item)
            self.source.set_item_widget(new_item, item_widget)
            self.parent.update_list_total()

    # noinspection PyTypeChecker
    def on_edit(self):
        item_widget: BudgetItemWidget = self.source.item_widget(self.selected_item)
        dlg = AddEntryDialog(f'Edit {self.text.lower()}', item_widget.name.text, item_widget.amount.text)

        if dlg.exec():
            self.source.remove_item_widget(self.selected_item)
            cli = BudgetItemWidget(dlg.name.text(), dlg.amount.text)
            self.source.set_item_widget(self.selected_item, cli)
            self.parent.update_list_total()

    def on_remove(self):
        button = QMessageBox.question(self.parent_widget(), f'Remove {self.text}?', 'Are you sure?')

        if button == QMessageBox.StandardButton.Yes:
            self.source.take_item(self.source.current_row)
            del self.selected_item
            self.parent.update_list_total()
