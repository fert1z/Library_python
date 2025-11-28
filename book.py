from datetime import datetime
from typing import List, Optional


class Book:
    """Класс для представления книги в библиотеке."""
    
    def __init__(self, title: str, author: str, book_id: Optional[str] = None):
        """
        Инициализация книги.
        
        Args:
            title: Название книги
            author: Автор книги
            book_id: Уникальный идентификатор книги (генерируется автоматически, если не указан)
        """
        self.title = title
        self.author = author
        self.book_id = book_id or f"book_{id(self)}"
        self.is_available = True
        self.reservations: List[str] = []  # Список имён пользователей, зарезервировавших книгу
    
    def __repr__(self) -> str:
        """Строковое представление книги."""
        status = "доступна" if self.is_available else "занята"
        return f"Book(id={self.book_id}, title='{self.title}', author='{self.author}', status={status})"
    
    def __eq__(self, other) -> bool:
        """Проверка равенства книг по ID."""
        if isinstance(other, Book):
            return self.book_id == other.book_id
        return False
    
    def to_dict(self) -> dict:
        """Преобразование книги в словарь для сохранения в JSON."""
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "is_available": self.is_available,
            "reservations": self.reservations
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """Создание объекта Book из словаря (для загрузки из JSON)."""
        book = cls(data["title"], data["author"], data["book_id"])
        book.is_available = data["is_available"]
        book.reservations = data.get("reservations", [])
        return book

