from PyQt6.QtGui import QContextMenuEvent, QAction
from PyQt6.QtWidgets import QMenu, QListWidget, QListWidgetItem, QMessageBox

from CustomWidgets.AddEntryDialog import AddEntryDialog
from CustomWidgets.BudgetItemWidget import BudgetItemWidget
from ListTab import ListTab


class ListContextMenu(QMenu):
    def __init__(self, parent, source: QListWidget, event: QContextMenuEvent, text: str):
        super().__init__(parent)

        self.parent: ListTab = parent
        self.source = source
        self.text = text

        self.selected_item = self.source.itemAt(event.pos())

        new = QAction(f'Add {text}...', self)
        new.setToolTip(f'Adds a new fixed {text.lower()} to the list.')
        new.triggered.connect(self.on_new)
        self.addAction(new)

        if self.selected_item is not None:
            proxy: BudgetItemWidget = self.source.itemWidget(self.selected_item)

            edit_item = QAction(f'Edit {proxy.name.text()}...', self)
            edit_item.setToolTip(f'Edits {proxy.name.text()}')
            edit_item.triggered.connect(self.on_edit)
            self.addAction(edit_item)

            remove = QAction(f'Remove {proxy.name.text()}...', self)
            remove.setToolTip(f'Removes {proxy.name.text()} from the list.')
            remove.triggered.connect(self.on_remove)
            self.addAction(remove)

    def on_new(self):
        dlg = AddEntryDialog(f'Add {self.text.lower()}')

        if dlg.exec():
            item_widget = BudgetItemWidget(dlg.name.text(), dlg.amount.text())
            new_item = QListWidgetItem(self.source)
            new_item.setSizeHint(item_widget.sizeHint())

            self.source.addItem(new_item)
            self.source.setItemWidget(new_item, item_widget)
            self.parent.update_list_total()

    # noinspection PyTypeChecker
    def on_edit(self):
        item_widget: BudgetItemWidget = self.source.itemWidget(self.selected_item)
        dlg = AddEntryDialog(f'Edit {self.text.lower()}', item_widget.name.text(), item_widget.amount.text())

        if dlg.exec():
            self.source.removeItemWidget(self.selected_item)
            cli = BudgetItemWidget(dlg.name.text(), dlg.amount.text())
            self.source.setItemWidget(self.selected_item, cli)
            self.parent.update_list_total()

    def on_remove(self):
        button = QMessageBox.question(self.parentWidget(), f'Remove {self.text}?', 'Are you sure?')

        if button == QMessageBox.StandardButton.Yes:
            self.source.takeItem(self.source.currentRow())
            del self.selected_item
            self.parent.update_list_total()
