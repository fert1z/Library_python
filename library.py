import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from book import Book
from user import User
from loan import Loan


class Library:
    """Класс для управления библиотекой."""
    
    def __init__(self):
        """Инициализация библиотеки."""
        self.books: Dict[str, Book] = {}  # book_id -> Book
        self.users: Dict[str, User] = {}  # user_id -> User
        self.users_by_name: Dict[str, User] = {}  # user_name -> User (для быстрого поиска)
        self.loans: List[Loan] = []  # Список активных выдач
    
    def add_book(self, book: Book) -> bool:
        """
        Добавление книги в библиотеку.
        
        Args:
            book: Объект Book для добавления
            
        Returns:
            True, если книга успешно добавлена, False если книга с таким ID уже существует
        """
        if book.book_id in self.books:
            return False
        self.books[book.book_id] = book
        return True
    
    def remove_book(self, book_id: str) -> bool:
        """
        Удаление книги из библиотеки.
        
        Args:
            book_id: ID книги для удаления
            
        Returns:
            True, если книга успешно удалена, False если книга не найдена или выдана
        """
        if book_id not in self.books:
            return False
        
        book = self.books[book_id]
        # Проверяем, не выдана ли книга
        if not book.is_available:
            return False
        
        # Удаляем книгу
        del self.books[book_id]
        return True
    
    def add_user(self, user: User) -> bool:
        """
        Добавление пользователя в библиотеку.
        
        Args:
            user: Объект User для добавления
            
        Returns:
            True, если пользователь успешно добавлен, False если пользователь с таким ID уже существует
        """
        if user.user_id in self.users:
            return False
        self.users[user.user_id] = user
        self.users_by_name[user.name] = user
        return True
    
    def remove_user(self, user_id: str) -> bool:
        """
        Удаление пользователя из библиотеки.
        
        Args:
            user_id: ID пользователя для удаления
            
        Returns:
            True, если пользователь успешно удалён, False если пользователь не найден или имеет взятые книги
        """
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        # Проверяем, нет ли у пользователя взятых книг
        if user.borrowed_books:
            return False
        
        # Удаляем пользователя
        del self.users[user_id]
        if user.name in self.users_by_name:
            del self.users_by_name[user.name]
        return True
    
    def find_user_by_name(self, user_name: str) -> Optional[User]:
        """Поиск пользователя по имени."""
        return self.users_by_name.get(user_name)
    
    def find_book_by_title(self, book_title: str) -> Optional[Book]:
        """Поиск книги по названию."""
        for book in self.books.values():
            if book.title == book_title:
                return book
        return None
    
    def borrow_book(self, user_name: str, book_title: str) -> Tuple[bool, str]:
        """
        Выдача книги пользователю.
        
        Args:
            user_name: Имя пользователя
            book_title: Название книги
            
        Returns:
            Кортеж (успех, сообщение)
        """
        user = self.find_user_by_name(user_name)
        if not user:
            return False, f"Пользователь '{user_name}' не найден"
        
        book = self.find_book_by_title(book_title)
        if not book:
            return False, f"Книга '{book_title}' не найдена"
        
        if not book.is_available:
            return False, f"Книга '{book_title}' уже выдана"
        
        # Выдаём книгу
        book.is_available = False
        user.borrowed_books.append(book.book_id)
        loan = Loan(user_name, book.book_id)
        self.loans.append(loan)
        
        # Если книга была зарезервирована этим пользователем, удаляем из резерваций
        if user_name in book.reservations:
            book.reservations.remove(user_name)
        
        return True, f"Книга '{book_title}' успешно выдана пользователю '{user_name}'"
    
    def return_book(self, user_name: str, book_title: str) -> Tuple[bool, str]:
        """
        Возврат книги в библиотеку.
        
        Args:
            user_name: Имя пользователя
            book_title: Название книги
            
        Returns:
            Кортеж (успех, сообщение)
        """
        user = self.find_user_by_name(user_name)
        if not user:
            return False, f"Пользователь '{user_name}' не найден"
        
        book = self.find_book_by_title(book_title)
        if not book:
            return False, f"Книга '{book_title}' не найдена"
        
        if book.book_id not in user.borrowed_books:
            return False, f"Пользователь '{user_name}' не брал книгу '{book_title}'"
        
        # Возвращаем книгу
        book.is_available = True
        user.borrowed_books.remove(book.book_id)
        
        # Удаляем выдачу
        self.loans = [loan for loan in self.loans 
                     if not (loan.user_name == user_name and loan.book_id == book.book_id)]
        
        # Проверяем наличие резерваций
        message = f"Книга '{book_title}' успешно возвращена"
        if book.reservations:
            message += f". Книга зарезервирована пользователем(ями): {', '.join(book.reservations)}"
        
        return True, message
    
    def reserve_book(self, user_name: str, book_title: str) -> Tuple[bool, str]:
        """
        Бронирование книги.
        
        Args:
            user_name: Имя пользователя
            book_title: Название книги
            
        Returns:
            Кортеж (успех, сообщение)
        """
        user = self.find_user_by_name(user_name)
        if not user:
            return False, f"Пользователь '{user_name}' не найден"
        
        book = self.find_book_by_title(book_title)
        if not book:
            return False, f"Книга '{book_title}' не найдена"
        
        if book.is_available:
            return False, f"Книга '{book_title}' доступна, можно взять без бронирования"
        
        if user_name in book.reservations:
            return False, f"Книга '{book_title}' уже зарезервирована пользователем '{user_name}'"
        
        # Добавляем резервацию
        book.reservations.append(user_name)
        return True, f"Книга '{book_title}' зарезервирована для пользователя '{user_name}'"
    
    def overdue_books(self) -> List[Loan]:
        """Получение списка просроченных книг."""
        return [loan for loan in self.loans if loan.is_overdue()]
    
    def get_all_books_status(self) -> List[Dict]:
        """
        Получение статуса всех книг.
        
        Returns:
            Список словарей с информацией о книгах
        """
        result = []
        for book in self.books.values():
            status = "доступна" if book.is_available else "занята"
            if book.reservations:
                status += f" (зарезервирована: {', '.join(book.reservations)})"
            
            # Находим, кто взял книгу, если она занята
            borrower = None
            for loan in self.loans:
                if loan.book_id == book.book_id:
                    borrower = loan.user_name
                    break
            
            result.append({
                "id": book.book_id,
                "title": book.title,
                "author": book.author,
                "status": status,
                "borrower": borrower,
                "reservations": book.reservations.copy()
            })
        return result
    
    def get_users_and_books(self) -> List[Dict]:
        """
        Получение списка пользователей и их взятых книг.
        
        Returns:
            Список словарей с информацией о пользователях
        """
        result = []
        for user in self.users.values():
            borrowed_titles = []
            for book_id in user.borrowed_books:
                if book_id in self.books:
                    borrowed_titles.append(self.books[book_id].title)
            
            result.append({
                "user_id": user.user_id,
                "name": user.name,
                "borrowed_books": borrowed_titles,
                "count": len(borrowed_titles)
            })
        return result
    
    def get_top_users(self, limit: int = 5) -> List[Dict]:
        """
        Получение пользователей с наибольшим количеством взятых книг.
        
        Args:
            limit: Количество пользователей для возврата
            
        Returns:
            Список словарей с информацией о пользователях, отсортированный по количеству книг
        """
        users_data = self.get_users_and_books()
        users_data.sort(key=lambda x: x["count"], reverse=True)
        return users_data[:limit]
    
    def save_to_file(self, filename: str) -> bool:
        """
        Сохранение данных библиотеки в JSON файл.
        
        Args:
            filename: Имя файла для сохранения
            
        Returns:
            True, если сохранение успешно, False в случае ошибки
        """
        try:
            data = {
                "books": [book.to_dict() for book in self.books.values()],
                "users": [user.to_dict() for user in self.users.values()],
                "loans": [loan.to_dict() for loan in self.loans]
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            return False
    
    def load_from_file(self, filename: str) -> bool:
        """
        Загрузка данных библиотеки из JSON файла.
        
        Args:
            filename: Имя файла для загрузки
            
        Returns:
            True, если загрузка успешна, False в случае ошибки
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Загружаем книги
            self.books = {}
            for book_data in data.get("books", []):
                book = Book.from_dict(book_data)
                self.books[book.book_id] = book
            
            # Загружаем пользователей
            self.users = {}
            self.users_by_name = {}
            for user_data in data.get("users", []):
                user = User.from_dict(user_data)
                self.users[user.user_id] = user
                self.users_by_name[user.name] = user
            
            # Загружаем выдачи
            self.loans = []
            for loan_data in data.get("loans", []):
                loan = Loan.from_dict(loan_data)
                self.loans.append(loan)
            
            return True
        except FileNotFoundError:
            print(f"Файл '{filename}' не найден")
            return False
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
            return False

