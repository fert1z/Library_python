"""Модуль с моделью библиотеки."""

from datetime import date
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

    def get_overdue_books(self) -> List[Dict[str, str | int]]:
        """Возвращает информацию о просроченных книгах."""
        today = date.today()
        overdue_items: List[Dict[str, str | int]] = []
        for loan in self.loans:
            if not loan.is_overdue(today):
                continue

            book = self.books.get(loan.book_id)
            user = self.users.get(loan.user_id)
            days_overdue = (today - loan.due_date).days

            overdue_items.append(
                {
                    "book_id": loan.book_id,
                    "book_title": book.title if book else "Unknown",
                    "user_id": loan.user_id,
                    "user_name": user.name if user else "Unknown",
                    "days_overdue": days_overdue,
                }
            )

        return overdue_items

    def get_top_readers(self) -> List[Dict[str, str | int]]:
        """Возвращает список самых активных читателей, отсортированных по количеству взятых книг."""
        readers_data: List[Dict[str, str | int]] = []
        for user in self.users.values():
            readers_data.append(
                {
                    "user_id": user.user_id,
                    "name": user.name,
                    "books_count": len(user.borrowed_books),
                }
            )
        readers_data.sort(key=lambda x: x["books_count"], reverse=True)
        return readers_data

