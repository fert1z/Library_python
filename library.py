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

    def return_book(self, user_id: str, book_id: str) -> bool:
        """Возвращает книгу: обновляет выдачу, книгу и пользователя."""
        user = self.users.get(user_id)
        if not user:
            raise ValueError(f"Пользователь {user_id} не найден")

        book = self.books.get(book_id)
        if not book:
            raise ValueError(f"Книга {book_id} не найдена")

        loan_index = next(
            (idx for idx, loan in enumerate(self.loans) if loan.book_id == book_id and loan.user_id == user_id),
            None,
        )
        if loan_index is None:
            raise ValueError("Запись о выдаче не найдена")

        self.loans.pop(loan_index)
        book.is_available = True
        book.reserved_by = None

        if book_id in user.borrowed_books:
            user.borrowed_books.remove(book_id)

        return True

