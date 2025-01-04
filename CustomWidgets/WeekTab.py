from calendar import monthrange
from datetime import datetime
from decimal import Decimal
from typing import Optional

from PySide6.QtCore import QObject
from PySide6.QtGui import QContextMenuEvent
from PySide6.QtWidgets import QLabel, QHBoxLayout, QListWidget, QVBoxLayout, QListWidgetItem
# noinspection PyUnresolvedReferences
from __feature__ import snake_case, true_property

import calculations
import core
from CustomWidgets.BudgetItemWidget import BudgetItemWidget
from CustomWidgets.ListContextMenu import ListContextMenu
from CustomWidgets.MoneyLabel import MoneyLabel
from CustomWidgets.ListTab import ListTab


class WeekTab(ListTab):
    def __init__(self,  name:str):
        super().__init__()

        self.name = name
        self.layout = QVBoxLayout()

        self._init_budget()
        self._init_expenses()
        self._init_current()

        self.set_layout(self.layout)
        self._load_information()

    def _init_budget(self):
        budget_label = QLabel('Budget:')
        self.budget = MoneyLabel()

        budget_layout = QHBoxLayout()
        budget_layout.add_widget(budget_label)
        budget_layout.add_widget(self.budget)

        self.layout.add_layout(budget_layout)

    def _init_expenses(self):
        self.expenses = QListWidget()
        self.expenses.install_event_filter(self)

        self.layout.add_widget(self.expenses)

    def _init_current(self):
        sum_label = QLabel('Total:')
        self.total = MoneyLabel()

        sum_layout = QHBoxLayout()
        sum_layout.add_widget(sum_label)
        sum_layout.add_widget(self.total)

        current_label = QLabel('Current budget:')
        self.current = MoneyLabel()

        current_layout = QHBoxLayout()
        current_layout.add_widget(current_label)
        current_layout.add_widget(self.current)

        layout = QVBoxLayout()
        layout.add_layout(sum_layout)
        layout.add_layout(current_layout)

        self.layout.add_layout(layout)

    def _load_information(self):
        self._load_budget()
        self._load_expenses()
        self._calculate_total()
        self._calculate_current()

    def _load_budget(self):
        now = datetime.now()
        days = monthrange(now.year, now.month)[1]

        income = calculations.calculate_sum(calculations.INCOME_FILE)
        expenses = calculations.calculate_sum(calculations.EXPENSES_FILE)
        budget = float(income) - float(expenses)

        if self.name == 'IV':
            text = f'{Decimal((budget / days) * (days - 21)):.2f}'
        else:
            text = f'{Decimal((budget / days) * 7):.2f}'

        self.budget.text = text

    def _load_expenses(self):
        self.expenses.clear()

        with open(core.filepath, 'a+') as file:
            file.seek(0)
            lines = file.read().splitlines()
            for i, line in enumerate(lines):
                items = line.split(';')
                if items[1] == self.name:
                    cli = BudgetItemWidget(items[2], items[0])
                    new_item = QListWidgetItem(self.expenses)
                    new_item.set_size_hint(cli.size_hint)

                    self.expenses.set_item_widget(new_item, cli)

    def _calculate_total(self):
        total = calculations.get_list_total(self.expenses)
        self.total.text = f'{Decimal(total):.2f}'

    def _calculate_current(self):
        budget = float(self.budget.text)
        total = calculations.get_list_total(self.expenses)
        self.current.text = f'{Decimal(budget - total):.2f}'

    # noinspection PyTypeChecker
    def show_context_menu(self, source: QObject, event: QContextMenuEvent, text: Optional[str] = 'Expense') -> ListContextMenu:
        super().show_context_menu(source, event, text)

    def update_list_total(self):
        self._calculate_total()
        self._calculate_current()

    def refresh(self):
        self._load_budget()
        self._calculate_current()

    def save_data(self) -> [str]:
        result = list()
        for index in range(0, self.expenses.count):
            entry = self.expenses.item(index)
            item_widget: BudgetItemWidget = self.expenses.item_widget(entry)
            result.append(f'{item_widget.amount.text};{self.name};{item_widget.name.text}\n')

        return result
