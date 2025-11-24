"""Модуль с моделью библиотеки."""

from typing import Dict, List, Optional

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

    def add_user(self, user: User) -> None:
        """Заглушка для добавления пользователя."""
        raise NotImplementedError

    def find_book(self, book_id: str) -> Optional[Book]:
        """Заглушка для поиска книги по идентификатору."""
        raise NotImplementedError

    def find_user(self, user_id: str) -> Optional[User]:
        """Заглушка для поиска пользователя по идентификатору."""
        raise NotImplementedError

    def get_users_and_their_books(self) -> List[Dict[str, List[str]]]:
        """Возвращает сведения о пользователях и их книгах."""
        result: List[Dict[str, List[str]]] = []
        for user in self.users.values():
            result.append(
                {
                    "user_id": user.user_id,
                    "name": user.name,
                    "borrowed_books": list(user.borrowed_books),
                }
            )
        return result

