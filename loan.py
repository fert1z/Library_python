"""Модель записи о выдаче книги."""

from datetime import date


class Loan:
    """Описание факта выдачи книги для читателя."""

    def __init__(
        self,
        book_id: str,
        user_id: str,
        borrow_date: date,
        due_date: date,
    ) -> None:
        self.book_id = book_id
        self.user_id = user_id
        self.borrow_date = borrow_date
        self.due_date = due_date

    def is_overdue(self, today: date | None = None) -> bool:
        """Вернёт True, если срок возврата истёк."""
        today = today or date.today()
        return today > self.due_date

