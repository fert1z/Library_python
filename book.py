"""Модель книги."""

from typing import Optional


class Book:
    """Описание книги с базовой логикой состояния."""

    def __init__(
        self,
        title: str,
        author: str,
        book_id: str,
        is_available: bool = True,
        reserved_by: Optional[str] = None,
    ) -> None:
        self.title = title
        self.author = author
        self.book_id = book_id
        self.is_available = is_available
        self.reserved_by = reserved_by

    def __str__(self) -> str:
        status = "доступна" if self.is_available else "недоступна"
        reserved = (
            f", зарезервирована пользователем {self.reserved_by}"
            if self.reserved_by
            else ""
        )
        return f"Книга[{self.book_id}] «{self.title}» — {self.author}, {status}{reserved}"

