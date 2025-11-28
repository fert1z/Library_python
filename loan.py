from datetime import datetime, timedelta
from typing import Optional


class Loan:
    """Класс для представления выдачи книги пользователю."""
    
    # Стандартный срок выдачи книги (в днях)
    LOAN_PERIOD_DAYS = 30
    
    def __init__(self, user_name: str, book_id: str, loan_date: Optional[datetime] = None, 
                 return_date: Optional[datetime] = None):
        """
        Инициализация выдачи книги.
        
        Args:
            user_name: Имя пользователя
            book_id: ID книги
            loan_date: Дата выдачи (по умолчанию - текущая дата)
            return_date: Дата возврата (вычисляется автоматически, если не указана)
        """
        self.user_name = user_name
        self.book_id = book_id
        self.loan_date = loan_date or datetime.now()
        
        if return_date:
            self.return_date = return_date
        else:
            # Вычисляем дату возврата как loan_date + LOAN_PERIOD_DAYS
            self.return_date = self.loan_date + timedelta(days=self.LOAN_PERIOD_DAYS)
    
    def is_overdue(self) -> bool:
        """Проверка, просрочена ли книга."""
        return datetime.now() > self.return_date
    
    def days_overdue(self) -> int:
        """Количество дней просрочки (0, если не просрочена)."""
        if self.is_overdue():
            return (datetime.now() - self.return_date).days
        return 0
    
    def __repr__(self) -> str:
        """Строковое представление выдачи."""
        status = "просрочена" if self.is_overdue() else "активна"
        return f"Loan(user='{self.user_name}', book_id='{self.book_id}', status={status})"
    
    def to_dict(self) -> dict:
        """Преобразование выдачи в словарь для сохранения в JSON."""
        return {
            "user_name": self.user_name,
            "book_id": self.book_id,
            "loan_date": self.loan_date.isoformat(),
            "return_date": self.return_date.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Loan':
        """Создание объекта Loan из словаря (для загрузки из JSON)."""
        loan_date = datetime.fromisoformat(data["loan_date"])
        return_date = datetime.fromisoformat(data["return_date"])
        return cls(
            data["user_name"],
            data["book_id"],
            loan_date,
            return_date
        )

