from datetime import datetime

from PySide6.QtWidgets import QListWidget
# noinspection PyUnresolvedReferences
from __feature__ import snake_case, true_property

from CustomWidgets.BudgetItemWidget import BudgetItemWidget


# noinspection PyTypeChecker
def save_data(target_list: QListWidget, filepath):
    with open(filepath, 'w+') as file:
        for index in range(0, target_list.count):
            entry = target_list.item(index)
            item_widget: BudgetItemWidget = target_list.item_widget(entry)
            file.write(f'{item_widget.amount.text};01;{item_widget.name.text}\n')

current_date = datetime.now()
filepath = f'data/weeks/{current_date.year}_{current_date.month:02}'