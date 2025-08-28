from dataclasses import dataclass


@dataclass(frozen=True)
class Currency:
    code: str


rub = Currency('RUB')
usd = Currency('USD')

