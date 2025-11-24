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

    def get_all_books_report(self) -> List[Dict[str, str]]:
        """Возвращает краткий отчёт по всем книгам."""
        report: List[Dict[str, str]] = []
        for book_id, book in self.books.items():
            if book.reserved_by:
                status = f"Reserved by {book.reserved_by}"
            elif book.is_available:
                status = "Available"
            else:
                status = "Borrowed"

            report.append(
                {
                    "id": book_id,
                    "title": book.title,
                    "author": book.author,
                    "status": status,
                }
            )
        return report

