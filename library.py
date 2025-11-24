"""Модуль с моделью библиотеки."""

from dataclasses import dataclass, field
from typing import List

from book import Book
from loan import Loan
from user import User


@dataclass
class Library:
    """Простейшее описание библиотеки."""

    name: str
    books: List[Book] = field(default_factory=list)
    users: List[User] = field(default_factory=list)
    loans: List[Loan] = field(default_factory=list)

