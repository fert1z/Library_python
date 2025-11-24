"""Модель пользователя библиотеки."""

from typing import List, Optional


class User:
    """Описание читателя с базовыми сведениями о книгах."""

    def __init__(
        self,
        name: str,
        user_id: str,
        borrowed_books: Optional[List[str]] = None,
    ) -> None:
        self.name = name
        self.user_id = user_id
        self.borrowed_books = borrowed_books or []

    def __str__(self) -> str:
        books = ", ".join(self.borrowed_books) if self.borrowed_books else "нет книг"
        return f"Пользователь[{self.user_id}] {self.name} — {books}"

