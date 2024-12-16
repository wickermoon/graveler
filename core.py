from PySide6.QtWidgets import QListWidget

from CustomWidgets.BudgetItemWidget import BudgetItemWidget


# noinspection PyTypeChecker
def save_data(target_list: QListWidget, filepath):
    with open(filepath, 'w+') as file:
        for index in range(0, target_list.count()):
            entry = target_list.item(index)
            item_widget: BudgetItemWidget = target_list.itemWidget(entry)
            file.write(f'{item_widget.amount.text()};01;{item_widget.name.text()}\n')
