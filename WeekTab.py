from calendar import monthrange
from datetime import datetime
from decimal import Decimal
from typing import Optional

from PySide6.QtCore import QObject
from PySide6.QtGui import QContextMenuEvent
from PySide6.QtWidgets import QLabel, QHBoxLayout, QListWidget, QVBoxLayout, QListWidgetItem

import calculations
import core
from CustomWidgets.BudgetItemWidget import BudgetItemWidget
from CustomWidgets.ListContextMenu import ListContextMenu
from CustomWidgets.MoneyLabel import MoneyLabel
from ListTab import ListTab


class WeekTab(ListTab):
    def __init__(self,  name:str):
        super().__init__()

        self.name = name
        self.layout = QVBoxLayout()

        self._init_budget()
        self._init_expenses()
        self._init_current()

        self.setLayout(self.layout)
        self._load_information()

    def _init_budget(self):
        budget_label = QLabel('Budget:')
        self.budget = MoneyLabel()

        budget_layout = QHBoxLayout()
        budget_layout.addWidget(budget_label)
        budget_layout.addWidget(self.budget)

        self.layout.addLayout(budget_layout)

    def _init_expenses(self):
        self.expenses_list = QListWidget()
        self.expenses_list.installEventFilter(self)
        self.layout.addWidget(self.expenses_list)

    def _init_current(self):
        sum_label = QLabel('Total:')
        self.total = MoneyLabel()

        sum_layout = QHBoxLayout()
        sum_layout.addWidget(sum_label)
        sum_layout.addWidget(self.total)

        current_label = QLabel('Current budget:')
        self.current = MoneyLabel()

        current_layout = QHBoxLayout()
        current_layout.addWidget(current_label)
        current_layout.addWidget(self.current)

        layout = QVBoxLayout()
        layout.addLayout(sum_layout)
        layout.addLayout(current_layout)

        self.layout.addLayout(layout)

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

        self.budget.setText(text)

    def _load_expenses(self):
        self.expenses_list.clear()

        current_date = datetime.now()
        filepath = f'data/weeks/{self.name}_{current_date.month}_{current_date.year}'

        with open(filepath, 'a+') as file:
            file.seek(0)
            lines = file.read().splitlines()
            for i, line in enumerate(lines):
                items = line.split(';')
                cli = BudgetItemWidget(items[2], items[0])
                new_item = QListWidgetItem(self.expenses_list)
                new_item.setSizeHint(cli.sizeHint())

                self.expenses_list.addItem(new_item)
                self.expenses_list.setItemWidget(new_item, cli)

    def _calculate_total(self):
        total = calculations.get_list_total(self.expenses_list)
        self.total.setText(f'{Decimal(total):.2f}')

    def _calculate_current(self):
        budget = float(self.budget.text())
        total = calculations.get_list_total(self.expenses_list)
        self.current.setText(f'{Decimal(budget - total):.2f}')

    # noinspection PyTypeChecker
    def show_context_menu(self, source: QObject, event: QContextMenuEvent, text: Optional[str] = 'Expense') -> ListContextMenu:
        super().show_context_menu(source, event, text)

    def update_list_total(self):
        self._calculate_total()
        self._calculate_current()

    def refresh(self):
        self._load_budget()
        self._calculate_current()

    def save_data(self):
        current_date = datetime.now()
        filepath = f'data/weeks/{self.name}_{current_date.month}_{current_date.year}'
        core.save_data(self.expenses_list, filepath)
