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
        """Удаляет книгу по идентификатору."""
        if book_id in self.books:
            del self.books[book_id]
            return True
        return False

    def add_user(self, name: str) -> User:
        """Создаёт пользователя и добавляет в каталог."""
        user_id = uuid4().hex
        user = User(name=name, user_id=user_id)
        self.users[user_id] = user
        return user

    def remove_user(self, user_id: str) -> bool:
        """Удаляет пользователя по идентификатору."""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False

    def find_book(self, book_id: str) -> Optional[Book]:
        """Ищет книгу по идентификатору."""
        return self.books.get(book_id)

    def find_user(self, user_id: str) -> Optional[User]:
        """Ищет пользователя по идентификатору."""
        return self.users.get(user_id)

    def borrow_book(self, user_id: str, book_id: str, loan_period_days: int = 14) -> Loan:
        """Выдаёт книгу пользователю."""
        user = self.find_user(user_id)
        if not user:
            raise ValueError(f"Пользователь {user_id} не найден")

        book = self.find_book(book_id)
        if not book:
            raise ValueError(f"Книга {book_id} не найдена")

        if not book.is_available:
            raise ValueError(f"Книга {book_id} уже выдана")

        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=loan_period_days)

        book.is_available = False
        book.reserved_by = user_id
        user.borrowed_books.append(book_id)

        loan = Loan(book_id=book_id, user_id=user_id, borrow_date=borrow_date, due_date=due_date)
        self.loans.append(loan)
        return loan

    def return_book(self, user_id: str, book_id: str) -> bool:
        """Возвращает книгу в библиотеку."""
        user = self.find_user(user_id)
        if not user:
            raise ValueError(f"Пользователь {user_id} не найден")

        book = self.find_book(book_id)
        if not book:
            raise ValueError(f"Книга {book_id} не найдена")

        loan_index = next(
            (idx for idx, loan in enumerate(self.loans) 
             if loan.book_id == book_id and loan.user_id == user_id),
            None
        )
        if loan_index is None:
            raise ValueError("Запись о выдаче не найдена")

        self.loans.pop(loan_index)
        book.is_available = True
        book.reserved_by = None

        if book_id in user.borrowed_books:
            user.borrowed_books.remove(book_id)

        return True

    def reserve_book(self, user_id: str, book_id: str) -> None:
        """Бронирует недоступную книгу для пользователя."""
        user = self.find_user(user_id)
        if not user:
            raise ValueError(f"Пользователь {user_id} не найден")

        book = self.find_book(book_id)
        if not book:
            raise ValueError(f"Книга {book_id} не найдена")

        if book.is_available:
            raise ValueError("Нельзя бронировать доступную книгу")

        if book.reserved_by and book.reserved_by != user_id:
            raise ValueError("Книга уже забронирована другим пользователем")

        book.reserved_by = user_id

    def get_all_books_report(self) -> List[Dict[str, str]]:
        """Возвращает отчёт по всем книгам."""
        report: List[Dict[str, str]] = []
        for book_id, book in self.books.items():
            if book.reserved_by:
                status = f"Reserved by {book.reserved_by}"
            elif book.is_available:
                status = "Available"
            else:
                status = "Borrowed"
            report.append({
                "id": book_id,
                "title": book.title,
                "author": book.author,
                "status": status
            })
        return report

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

