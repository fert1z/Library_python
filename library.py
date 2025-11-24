"""Модуль с моделью библиотеки."""

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

