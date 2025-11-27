"""Модуль с моделью библиотеки."""

import json
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

    def save_to_file(self, filename: str) -> None:
        """Сохраняет состояние библиотеки в JSON-файл."""
        # Сериализация книг
        books_data = {}
        for book_id, book in self.books.items():
            books_data[book_id] = {
                "title": book.title,
                "author": book.author,
                "book_id": book.book_id,
                "is_available": book.is_available,
                "reserved_by": book.reserved_by,
            }

        # Сериализация пользователей
        users_data = {}
        for user_id, user in self.users.items():
            users_data[user_id] = {
                "name": user.name,
                "user_id": user.user_id,
                "borrowed_books": list(user.borrowed_books),
            }

        # Сериализация выдач (с конвертацией дат в строки)
        loans_data = []
        for loan in self.loans:
            loans_data.append({
                "book_id": loan.book_id,
                "user_id": loan.user_id,
                "borrow_date": loan.borrow_date.isoformat(),
                "due_date": loan.due_date.isoformat(),
            })

        # Объединение всех данных
        data = {
            "name": self.name,
            "books": books_data,
            "users": users_data,
            "loans": loans_data,
        }

        # Сохранение в файл
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_file(self, filename: str) -> None:
        """Загружает состояние библиотеки из JSON-файла."""
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Восстановление имени библиотеки
        self.name = data.get("name", "My Library")

        # Восстановление книг
        self.books = {}
        books_data = data.get("books", {})
        for book_id, book_info in books_data.items():
            book = Book(
                title=book_info["title"],
                author=book_info["author"],
                book_id=book_info["book_id"],
                is_available=book_info["is_available"],
                reserved_by=book_info.get("reserved_by"),
            )
            self.books[book_id] = book

        # Восстановление пользователей
        self.users = {}
        users_data = data.get("users", {})
        for user_id, user_info in users_data.items():
            user = User(
                name=user_info["name"],
                user_id=user_info["user_id"],
                borrowed_books=user_info.get("borrowed_books", []),
            )
            self.users[user_id] = user

        # Восстановление выдач (с преобразованием строк дат в объекты date)
        self.loans = []
        loans_data = data.get("loans", [])
        for loan_info in loans_data:
            loan = Loan(
                book_id=loan_info["book_id"],
                user_id=loan_info["user_id"],
                borrow_date=date.fromisoformat(loan_info["borrow_date"]),
                due_date=date.fromisoformat(loan_info["due_date"]),
            )
            self.loans.append(loan)

