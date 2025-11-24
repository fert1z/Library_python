"""Модуль с моделью библиотеки."""

from datetime import date, timedelta
from typing import Dict, List, Optional
from uuid import uuid4

from book import Book
from loan import Loan
from user import User


class Library:
    """Контейнер для управления книгами, пользователями и выдачами."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.books: Dict[str, Book] = {}
        self.users: Dict[str, User] = {}
        self.loans: List[Loan] = []

    def add_book(self, title: str, author: str) -> Book:
        """Создаёт книгу и добавляет в каталог."""
        book_id = uuid4().hex
        book = Book(title=title, author=author, book_id=book_id)
        self.books[book_id] = book
        return book

    def remove_book(self, book_id: str) -> bool:
        """Удаляет книгу по идентификатору и возвращает True, если она существовала."""
        return self.books.pop(book_id, None) is not None

    def find_book(self, book_id: str) -> Optional[Book]:
        """Ищет книгу по идентификатору."""
        return self.books.get(book_id)

    def add_user(self, user: User) -> None:
        """Заглушка для добавления пользователя."""
        raise NotImplementedError

    def find_user(self, user_id: str) -> Optional[User]:
        """Заглушка для поиска пользователя по идентификатору."""
        raise NotImplementedError

    def borrow_book(
        self,
        user_id: str,
        book_id: str,
        loan_period_days: int = 14,
        borrow_date: Optional[date] = None,
    ) -> Loan:
        """Выдаёт книгу пользователю при соблюдении всех условий."""
        user = self.users.get(user_id)
        if not user:
            raise ValueError(f"Пользователь {user_id} не найден")

        book = self.books.get(book_id)
        if not book:
            raise ValueError(f"Книга {book_id} не найдена")

        if not book.is_available:
            raise ValueError(f"Книга {book_id} уже выдана")

        borrow_date = borrow_date or date.today()
        due_date = borrow_date + timedelta(days=loan_period_days)

        book.is_available = False
        book.reserved_by = user.name
        user.borrowed_books.append(book_id)

        loan = Loan(
            book_id=book_id,
            user_id=user_id,
            borrow_date=borrow_date,
            due_date=due_date,
        )
        self.loans.append(loan)
        return loan

