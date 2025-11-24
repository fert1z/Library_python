"""Модель записи о выдаче книги."""

from dataclasses import dataclass
from datetime import date

from book import Book
from user import User


@dataclass
class Loan:
    """Описание факта выдачи книги."""

    book: Book
    user: User
    issued_on: date
    due_on: date

