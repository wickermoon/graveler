import decimal
from calendar import monthrange
from datetime import datetime
from decimal import Decimal
from typing import Optional

from PySide6.QtCore import QObject
from PySide6.QtGui import QContextMenuEvent
from PySide6.QtWidgets import QLabel, QListWidget, QGridLayout, QListWidgetItem, QHBoxLayout, QVBoxLayout, QLayout
# noinspection PyUnresolvedReferences
from __feature__ import snake_case, true_property

import calculations
import core
from CustomWidgets.BudgetItemWidget import BudgetItemWidget
from CustomWidgets.ListContextMenu import ListContextMenu
from CustomWidgets.MoneyLabel import MoneyLabel
from ListTab import ListTab


class Preferences(ListTab):
    def __init__(self):
        super().__init__()
        decimal.getcontext().rounding = decimal.ROUND_DOWN

        self.layout = QGridLayout()

        self._init_income()
        self._init_expenses()
        self._init_budget()

        self.set_layout(self.layout)

    @staticmethod
    def _load_list(list_widget: QListWidget, filepath: str) -> None:
        list_widget.clear()
        with open(filepath, 'a+') as file:
            file.seek(0)
            lines = file.read().splitlines()
            for i, line in enumerate(lines):
                items = line.split(';')
                cli = BudgetItemWidget(items[2], items[0])
                new_item = QListWidgetItem(list_widget)
                new_item.set_size_hint(cli.size_hint)

                list_widget.add_item(new_item)
                list_widget.set_item_widget(new_item, cli)

    # noinspection PyTypeChecker
    @staticmethod
    def _update_list_total(list_widget: QListWidget, label):
        total = calculations.get_list_total(list_widget)
        label.text = f'{total:.2f}'

    def _init_income(self) -> None:
        income_label = QLabel('Fixed Income:')
        self.income_sum = MoneyLabel()

        income_label_layout = QHBoxLayout()
        income_label_layout.add_widget(income_label)
        income_label_layout.add_widget(self.income_sum)

        self.income_list = QListWidget()
        self._load_list(self.income_list, calculations.INCOME_FILE)
        self._update_list_total(self.income_list, self.income_sum)

        self.income_list.install_event_filter(self)

        self.layout.add_layout(income_label_layout, 0, 0)
        self.layout.add_widget(self.income_list, 1, 0)

    def _init_expenses(self) -> None:
        expenses_label = QLabel('Fixed Expenses: ')
        self.expenses_sum = MoneyLabel()

        expenses_label_layout = QHBoxLayout()
        expenses_label_layout.add_widget(expenses_label)
        expenses_label_layout.add_widget(self.expenses_sum)

        self.expenses_list = QListWidget()
        self._load_list(self.expenses_list, calculations.EXPENSES_FILE)
        self._update_list_total(self.expenses_list, self.expenses_sum)

        self.expenses_list.install_event_filter(self)

        self.layout.add_layout(expenses_label_layout, 0, 1)
        self.layout.add_widget(self.expenses_list, 1, 1)

    def _init_budget(self) -> None:
        budget_layout = QVBoxLayout()
        budget_layout.add_layout(self._init_general_budget())
        budget_layout.add_layout(self._init_yearly_budget())
        budget_layout.add_layout(self._init_weekly_budget())

        self._recalculate()

        self.layout.add_layout(budget_layout, 2, 0, 1, 2)

    def _init_general_budget(self) -> QLayout:
        general_budget = QHBoxLayout()
        general_budget.add_widget(QLabel('Budget: '))
        self.budget_total = MoneyLabel()
        general_budget.add_widget(self.budget_total)

        return general_budget

    def _init_yearly_budget(self) -> QLayout:
        yearly_budget = QVBoxLayout()
        yearly_budget.add_widget(QLabel('Yearly: '))

        with open(calculations.YEARLY_FILE, 'a+') as file:
            file.seek(0)
            lines = file.read().splitlines()
            for line in lines:
                line = line.split(';')
                tmp = QHBoxLayout()
                tmp2 = QHBoxLayout()
                tmp.add_widget(MoneyLabel(f'per {line[1]} months:'))
                tmp.add_layout(tmp2)

                tmp2.add_widget(QLabel(line[2]))
                tmp2.add_widget(MoneyLabel(line[0]))
                yearly_budget.add_layout(tmp)

        return yearly_budget

    def _init_weekly_budget(self) -> QLayout:
        weekly_budget = QVBoxLayout()
        weekly_budget.add_widget(QLabel('Weekly:'))

        current = QHBoxLayout()
        current.add_widget(MoneyLabel('Current:'))

        self.current = MoneyLabel()
        current.add_widget(self.current)
        weekly_budget.add_layout(current)

        week1 = QHBoxLayout()
        week1.add_widget(MoneyLabel('Weeks 1-3:'))
        self.week1 = MoneyLabel()
        week1.add_widget(self.week1)
        weekly_budget.add_layout(week1)

        week4 = QHBoxLayout()
        week4.add_widget(MoneyLabel('Weeks 4:'))
        self.week4 = MoneyLabel()
        week4.add_widget(self.week4)
        weekly_budget.add_layout(week4)

        return weekly_budget

    def _recalculate(self):
        budget = float(self.income_sum.text) - float(self.expenses_sum.text)
        now = datetime.now()
        days = monthrange(now.year, now.month)[1]
        day = now.day
        multiplier = 7 if day < 22 else days - 21

        self.budget_total.text = f'{Decimal(budget):.2f}'
        self.current.text = f'{Decimal((budget / days) * multiplier):.2f}'
        self.week1.text = f'{Decimal(budget / 4):.2f} / {Decimal((budget / 30) * 7):.2f} / {Decimal((budget / 31) * 7):.2f}'
        self.week4.text = f'{Decimal((budget / 30) * 9):.2f} / {Decimal((budget / 31) * 10):.2f}'

    # noinspection PyTypeChecker
    def show_context_menu(self, source: QObject, event: QContextMenuEvent, text: Optional[str] = '') -> ListContextMenu:
        text = 'Income' if source is self.income_list else 'Expense'

        super().show_context_menu(source, event, text)

    def update_list_total(self):
        self._update_list_total(self.income_list, self.income_sum)
        self._update_list_total(self.expenses_list, self.expenses_sum)
        self._recalculate()

    def reload_data(self):
        self._load_list(self.income_list, calculations.INCOME_FILE)
        self._load_list(self.expenses_list, calculations.EXPENSES_FILE)

        self.update_list_total()

    def save_data(self):
        core.save_data(self.income_list, calculations.INCOME_FILE)
        core.save_data(self.expenses_list, calculations.EXPENSES_FILE)
