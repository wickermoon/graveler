from PySide6.QtWidgets import QListWidget
# noinspection PyUnresolvedReferences
from __feature__ import snake_case, true_property

from CustomWidgets.BudgetItemWidget import BudgetItemWidget

INCOME_FILE = 'data/fixed_incomes'
EXPENSES_FILE = 'data/fixed_expenses'
YEARLY_FILE = 'data/yearly_expenses'

def calculate_sum(file: str):
    with open(file, 'a+') as file:
        file.seek(0)
        lines = file.read().splitlines()
        result = 0
        for i, line in enumerate(lines):
            items = line.split(';')
            result += float(items[0])
        return result

# noinspection PyTypeChecker
def get_list_total(list_widget: QListWidget):
    total = 0
    for index in range(0, list_widget.count):
        item_widget: BudgetItemWidget = list_widget.item_widget(list_widget.item(index))
        total += float(item_widget.amount.text)
    return total