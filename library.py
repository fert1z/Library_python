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

    def add_user(self, name: str) -> User:
        """Создаёт пользователя и добавляет в каталог."""
        user_id = uuid4().hex
        user = User(name=name, user_id=user_id)
        self.users[user_id] = user
        return user

    def remove_user(self, user_id: str) -> bool:
        """Удаляет пользователя по идентификатору."""
        return self.users.pop(user_id, None) is not None

    def find_user(self, user_id: str) -> Optional[User]:
        """Ищет пользователя по идентификатору."""
        return self.users.get(user_id)

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

