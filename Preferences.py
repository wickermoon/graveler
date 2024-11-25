import decimal
from calendar import monthrange
from datetime import datetime
from decimal import Decimal

from PyQt6.QtCore import QObject, QEvent
from PyQt6.QtGui import QContextMenuEvent
from PyQt6.QtWidgets import QWidget, QLabel, QListWidget, QGridLayout, QListWidgetItem, QHBoxLayout, QVBoxLayout, QLayout

from CustomWidgets.BudgetItemWidget import BudgetItemWidget
from CustomWidgets.MoneyLabel import MoneyLabel
from ListContextMenu import ListContextMenu

INCOME_FILE = 'data/fixed_incomes'
EXPENSES_FILE = 'data/fixed_expenses'

class Preferences(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()

        self._init_income()
        self._init_expenses()
        self._init_budget()

        self.setLayout(self.layout)

    @staticmethod
    def _load_list(list_widget: QListWidget, filepath: str) -> None:
        list_widget.clear()
        with open(filepath) as file:
            lines = file.read().splitlines()
            for i, line in enumerate(lines):
                items = line.split(';')
                cli = BudgetItemWidget(items[2], items[0])
                new_item = QListWidgetItem(list_widget)
                new_item.setSizeHint(cli.sizeHint())

                list_widget.addItem(new_item)
                list_widget.setItemWidget(new_item, cli)

    # noinspection PyTypeChecker
    @staticmethod
    def _update_list_total(list_widget: QListWidget, label):
        total = 0
        for index in range(0, list_widget.count()):
            item_widget: BudgetItemWidget = list_widget.itemWidget(list_widget.item(index))
            total += float(item_widget.amount.text())

        label.setText(f'{total:.2f}')

    def _init_income(self) -> None:
        income_label = QLabel('Fixed Income:')
        self.income_sum = MoneyLabel()

        income_label_layout = QHBoxLayout()
        income_label_layout.addWidget(income_label)
        income_label_layout.addWidget(self.income_sum)

        self.income_list = QListWidget()
        self._load_list(self.income_list, INCOME_FILE)
        self._update_list_total(self.income_list, self.income_sum)

        self.income_list.installEventFilter(self)

        self.layout.addLayout(income_label_layout, 0, 0)
        self.layout.addWidget(self.income_list, 1, 0)

    def _init_expenses(self) -> None:
        expenses_label = QLabel('Fixed Expenses: ')
        self.expenses_sum = MoneyLabel()

        expenses_label_layout = QHBoxLayout()
        expenses_label_layout.addWidget(expenses_label)
        expenses_label_layout.addWidget(self.expenses_sum)

        self.expenses_list = QListWidget()
        self._load_list(self.expenses_list, EXPENSES_FILE)
        self._update_list_total(self.expenses_list, self.expenses_sum)

        self.expenses_list.installEventFilter(self)

        self.layout.addLayout(expenses_label_layout, 0, 1)
        self.layout.addWidget(self.expenses_list, 1, 1)

    def _init_budget(self) -> None:
        decimal.getcontext().rounding = decimal.ROUND_DOWN
        budget = float(self.income_sum.text()) - float(self.expenses_sum.text())

        budget_layout = QVBoxLayout()
        budget_layout.addLayout(self._init_general_budget(budget))
        budget_layout.addLayout(self._init_yearly_budget(budget))
        budget_layout.addLayout(self._init_weekly_budget(budget))

        self.layout.addLayout(budget_layout, 2, 0, 1, 2)

    def _init_general_budget(self, budget: float) -> QLayout:
        general_budget = QHBoxLayout()
        general_budget.addWidget(QLabel('Budget: '))
        self.budget_total = MoneyLabel(f'{Decimal(budget):.2f}')
        general_budget.addWidget(self.budget_total)

        return general_budget

    def _init_yearly_budget(self, budget: float) -> QLayout:
        yearly_budget = QVBoxLayout()
        yearly_budget.addWidget(QLabel('Yearly: '))

        with open('data/yearly_expenses') as file:
            lines = file.read().splitlines()
            for line in lines:
                line = line.split(';')
                tmp = QHBoxLayout()
                tmp2 = QHBoxLayout()
                tmp.addWidget(MoneyLabel(f'per {line[1]} months:'))
                tmp.addLayout(tmp2)

                tmp2.addWidget(QLabel(line[2]))
                tmp2.addWidget(MoneyLabel(line[0]))
                yearly_budget.addLayout(tmp)

        return yearly_budget

    def _init_weekly_budget(self, budget: float) -> QLayout:
        weekly_budget = QVBoxLayout()
        weekly_budget.addWidget(QLabel('Weekly:'))

        current = QHBoxLayout()
        current.addWidget(MoneyLabel('Current:'))

        now = datetime.now()
        days = monthrange(now.year, now.month)[1]
        day = now.day
        multiplier = 7 if day < 22 else days - 21

        self.current = MoneyLabel(f'{Decimal((budget / days) * multiplier):.2f}')
        current.addWidget(self.current)
        weekly_budget.addLayout(current)

        week1 = QHBoxLayout()
        week1.addWidget(MoneyLabel('Weeks 1-3:'))
        self.week1 = MoneyLabel(f'{Decimal((budget / 30) * 7):.2f} / {Decimal((budget / 31) * 7):.2f}')
        week1.addWidget(self.week1)
        weekly_budget.addLayout(week1)

        week4 = QHBoxLayout()
        week4.addWidget(MoneyLabel('Weeks 4:'))
        self.week4 = MoneyLabel(f'{Decimal((budget / 30) * 9):.2f} / {Decimal((budget / 31) * 10):.2f}')
        week4.addWidget(self.week4)
        weekly_budget.addLayout(week4)

        return weekly_budget

    def _recalculate(self):
        budget = float(self.income_sum.text()) - float(self.expenses_sum.text())
        now = datetime.now()
        days = monthrange(now.year, now.month)[1]
        day = now.day
        multiplier = 7 if day < 22 else days - 21

        self.budget_total.setText(f'{Decimal(budget):.2f}')
        self.current.setText(f'{Decimal((budget / days) * multiplier):.2f}')
        self.week1.setText(f'{Decimal((budget / 30) * 7):.2f} / {Decimal((budget / 31) * 7):.2f}')
        self.week4.setText(f'{Decimal((budget / 30) * 9):.2f} / {Decimal((budget / 31) * 10):.2f}')

    # noinspection PyTypeChecker
    def eventFilter(self, source: QObject, event: QEvent) -> None:
        if event.type() == QEvent.Type.ContextMenu:
            self.show_context_menu(source, event)
            return True

        return source.eventFilter(source, event)

    # noinspection PyTypeChecker
    def show_context_menu(self, source: QObject, event: QContextMenuEvent) -> ListContextMenu:
        text = 'Income' if source is self.income_list else 'Expense'

        context = ListContextMenu(self, source, event, text)
        context.exec(event.globalPos())

    def reload_data(self):
        self._load_list(self.income_list, INCOME_FILE)
        self._load_list(self.expenses_list, EXPENSES_FILE)

        self.update_list_total(self.income_list)
        self.update_list_total(self.expenses_list)

    def update_list_total(self, list_widget):
        if list_widget is self.income_list:
            self._update_list_total(self.income_list, self.income_sum)
        else:
            self._update_list_total(self.expenses_list, self.expenses_sum)

        self._recalculate()
