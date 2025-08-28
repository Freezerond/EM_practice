from contextlib import ExitStack
from dataclasses import dataclass, field
from itertools import batched
from typing import Iterable, TypeAlias

SomeRemoteData: TypeAlias = int


@dataclass
class Query:
    per_page: int = 3
    page: int = 1


@dataclass
class Page:
    per_page: int = 3
    results: Iterable[SomeRemoteData] = field(default_factory=list)
    next: int | None = None


def request(query: Query) -> Page:
    data = [i for i in range(0, 10)]
    chunks = list(batched(data, query.per_page))
    return Page(
        per_page=query.per_page,
        results=chunks[query.page - 1],
        next=query.page + 1 if query.page < len(chunks) else None,
    )


class RetrieveRemoteData:
    def __init__(self, per_page: int):
        self.per_page = per_page

    def __iter__(self):
        page = request(Query(self.per_page, 1))
        while True:
            yield from page.results
            if page.next is None:
                return
            page = request(Query(self.per_page, page.next))


class Fibo:
    def __init__(self, n: int):
        self.n = n
        self.pre = [0, 1]
        self.cur = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.cur == self.n:
            raise StopIteration
        self.cur += 1

        if self.cur == 1:
            return 0
        elif self.cur == 2:
            return 1

        self.pre = [self.pre[1], sum(self.pre)]
        return self.pre[1]
