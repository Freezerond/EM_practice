from wallets.currency import Currency, rub, usd
from wallets.exceptions import NotComparisonException, NegativeValueException
from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    value: float
    currency: Currency

    def __add__(self, other):
        self.comparison_currency(other)
        return Money(self.value + other.value, self.currency)

    def __sub__(self, other):
        self.comparison_currency(other)
        return Money(self.value - other.value, self.currency)

    def comparison_currency(self, other):
        if self.currency != other.currency:
            raise NotComparisonException(f'Валюта не совпадает: {self.currency}/{other.currency}')

    def is_negative_value(self):
        if self.value < 0:
            raise NegativeValueException(f'Деньги не могут быть отрицательными: {self.currency}: {self.value}')


class Wallet:
    def __init__(self, *moneys: Money):
        self.__balance = dict()
        for money in moneys:
            self.add(money)

    def __getitem__(self, item: Currency):
        return self.__balance.get(item, Money(0, item))

    def __setitem__(self, item: Currency, money: Money):
        if item != money.currency:
            raise NotComparisonException(f'Валюта не совпадает: {item}/{money.currency}')
        money.is_negative_value()
        self.__balance[item] = money

    def __delitem__(self, key: Currency):
        if key in self.__balance:
            del self.__balance[key]

    def __len__(self):
        return len(self.__balance)

    def __contains__(self, item: Currency):
        return item in self.__balance

    @property
    def currencies(self):
        return self.__balance.keys()

    def add(self, money: Money):
        self[money.currency] += money
        return self

    def sub(self, money: Money):
        cur_money = self[money.currency] - money
        cur_money.is_negative_value()
        self.__balance[money.currency] = cur_money
        return self

