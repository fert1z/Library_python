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

    def add_book(self, book: Book) -> None:
        """Заглушка для добавления книги."""
        raise NotImplementedError

    def add_user(self, name: str) -> User:
        """Создаёт пользователя и добавляет в каталог."""
        user_id = uuid4().hex
        user = User(name=name, user_id=user_id)
        self.users[user_id] = user
        return user

    def remove_user(self, user_id: str) -> bool:
        """Удаляет пользователя по идентификатору."""
        return self.users.pop(user_id, None) is not None

    def find_book(self, book_id: str) -> Optional[Book]:
        """Заглушка для поиска книги по идентификатору."""
        raise NotImplementedError

    def find_user(self, user_id: str) -> Optional[User]:
        """Ищет пользователя по идентификатору."""
        return self.users.get(user_id)

