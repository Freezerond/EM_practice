from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Order:
    """There is no need to describe anything here."""


class Discount(ABC):
    @abstractmethod
    def apply(self, order: Order):
        pass


class FixedDiscount(Discount):
    def apply(self, order: Order):
        pass


class PercentageDiscount(Discount):
    def apply(self, order: Order):
        pass


class LoyaltyDiscount(Discount):
    def apply(self, order: Order):
        pass


class DiscountSelector:
    """
    Определяет, какие скидки применимы к заказу.
    Здесь можно закладывать любую бизнес-логику.
    """
    def __init__(self, order: Order):
        self.order = order

    def get_discounts(self) -> list[Discount]:
        pass


class DiscountApplier:
    """Применяет выбранные скидки к заказу в правильном порядке."""
    def __init__(self, order: Order, discounts: list[Discount]):
        self.order = order
        self.discounts = discounts

    def apply(self) -> None:
        for discount in self.discounts:
            discount.apply(self.order)
