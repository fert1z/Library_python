from typing import List, Optional


class User:
    """Класс для представления пользователя библиотеки."""
    
    def __init__(self, name: str, user_id: Optional[str] = None):
        """
        Инициализация пользователя.
        
        Args:
            name: Имя пользователя
            user_id: Уникальный идентификатор пользователя (генерируется автоматически, если не указан)
        """
        self.name = name
        self.user_id = user_id or f"user_{id(self)}"
        self.borrowed_books: List[str] = []  # Список ID взятых книг
    
    def __repr__(self) -> str:
        """Строковое представление пользователя."""
        return f"User(id={self.user_id}, name='{self.name}', borrowed_books={len(self.borrowed_books)})"
    
    def __eq__(self, other) -> bool:
        """Проверка равенства пользователей по ID."""
        if isinstance(other, User):
            return self.user_id == other.user_id
        return False
    
    def to_dict(self) -> dict:
        """Преобразование пользователя в словарь для сохранения в JSON."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "borrowed_books": self.borrowed_books
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Создание объекта User из словаря (для загрузки из JSON)."""
        user = cls(data["name"], data["user_id"])
        user.borrowed_books = data.get("borrowed_books", [])
        return user

