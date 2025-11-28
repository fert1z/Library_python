"""
Главная программа для системы управления библиотекой.
"""

from library import Library
from book import Book
from user import User


def print_menu():
    """Вывод меню на экран."""
    print("\n" + "="*50)
    print("СИСТЕМА УПРАВЛЕНИЯ БИБЛИОТЕКОЙ")
    print("="*50)
    print("1  - Добавить книгу")
    print("2  - Удалить книгу")
    print("3  - Добавить пользователя")
    print("4  - Удалить пользователя")
    print("5  - Взять книгу")
    print("6  - Вернуть книгу")
    print("7  - Забронировать книгу")
    print("8  - Показать отчёты")
    print("9  - Сохранить данные")
    print("10 - Загрузить данные")
    print("0  - Выход")
    print("="*50)


def add_book_menu(library: Library):
    """Меню добавления книги."""
    print("\n--- Добавление книги ---")
    title = input("Введите название книги: ").strip()
    if not title:
        print("Ошибка: название книги не может быть пустым")
        return
    
    author = input("Введите автора книги: ").strip()
    if not author:
        print("Ошибка: автор книги не может быть пустым")
        return
    
    book = Book(title, author)
    if library.add_book(book):
        print(f"Книга '{title}' успешно добавлена (ID: {book.book_id})")
    else:
        print("Ошибка: книга с таким ID уже существует")


def remove_book_menu(library: Library):
    """Меню удаления книги."""
    print("\n--- Удаление книги ---")
    book_id = input("Введите ID книги для удаления: ").strip()
    if not book_id:
        print("Ошибка: ID книги не может быть пустым")
        return
    
    if library.remove_book(book_id):
        print(f"Книга с ID '{book_id}' успешно удалена")
    else:
        print("Ошибка: книга не найдена или выдана пользователю")


def add_user_menu(library: Library):
    """Меню добавления пользователя."""
    print("\n--- Добавление пользователя ---")
    name = input("Введите имя пользователя: ").strip()
    if not name:
        print("Ошибка: имя пользователя не может быть пустым")
        return
    
    user = User(name)
    if library.add_user(user):
        print(f"Пользователь '{name}' успешно добавлен (ID: {user.user_id})")
    else:
        print("Ошибка: пользователь с таким ID уже существует")


def remove_user_menu(library: Library):
    """Меню удаления пользователя."""
    print("\n--- Удаление пользователя ---")
    user_id = input("Введите ID пользователя для удаления: ").strip()
    if not user_id:
        print("Ошибка: ID пользователя не может быть пустым")
        return
    
    if library.remove_user(user_id):
        print(f"Пользователь с ID '{user_id}' успешно удалён")
    else:
        print("Ошибка: пользователь не найден или имеет взятые книги")


def borrow_book_menu(library: Library):
    """Меню выдачи книги."""
    print("\n--- Выдача книги ---")
    user_name = input("Введите имя пользователя: ").strip()
    if not user_name:
        print("Ошибка: имя пользователя не может быть пустым")
        return
    
    book_title = input("Введите название книги: ").strip()
    if not book_title:
        print("Ошибка: название книги не может быть пустым")
        return
    
    success, message = library.borrow_book(user_name, book_title)
    print(message)


def return_book_menu(library: Library):
    """Меню возврата книги."""
    print("\n--- Возврат книги ---")
    user_name = input("Введите имя пользователя: ").strip()
    if not user_name:
        print("Ошибка: имя пользователя не может быть пустым")
        return
    
    book_title = input("Введите название книги: ").strip()
    if not book_title:
        print("Ошибка: название книги не может быть пустым")
        return
    
    success, message = library.return_book(user_name, book_title)
    print(message)


def reserve_book_menu(library: Library):
    """Меню бронирования книги."""
    print("\n--- Бронирование книги ---")
    user_name = input("Введите имя пользователя: ").strip()
    if not user_name:
        print("Ошибка: имя пользователя не может быть пустым")
        return
    
    book_title = input("Введите название книги: ").strip()
    if not book_title:
        print("Ошибка: название книги не может быть пустым")
        return
    
    success, message = library.reserve_book(user_name, book_title)
    print(message)


def show_reports_menu(library: Library):
    """Меню отчётов."""
    print("\n--- ОТЧЁТЫ ПО БИБЛИОТЕКЕ ---")
    
    while True:
        print("\n1 - Список всех книг и их статус")
        print("2 - Пользователи и их книги")
        print("3 - Просроченные книги")
        print("4 - Пользователи с наибольшим количеством книг")
        print("0 - Назад в главное меню")
        
        choice = input("\nВыберите отчёт: ").strip()
        
        if choice == "1":
            print("\n--- Список всех книг ---")
            books_status = library.get_all_books_status()
            if not books_status:
                print("В библиотеке нет книг")
            else:
                for book_info in books_status:
                    print(f"\nID: {book_info['id']}")
                    print(f"  Название: {book_info['title']}")
                    print(f"  Автор: {book_info['author']}")
                    print(f"  Статус: {book_info['status']}")
                    if book_info['borrower']:
                        print(f"  Взята пользователем: {book_info['borrower']}")
        
        elif choice == "2":
            print("\n--- Пользователи и их книги ---")
            users_data = library.get_users_and_books()
            if not users_data:
                print("В библиотеке нет пользователей")
            else:
                for user_info in users_data:
                    print(f"\nПользователь: {user_info['name']} (ID: {user_info['user_id']})")
                    if user_info['borrowed_books']:
                        print(f"  Взятые книги ({user_info['count']}):")
                        for book_title in user_info['borrowed_books']:
                            print(f"    - {book_title}")
                    else:
                        print("  Нет взятых книг")
        
        elif choice == "3":
            print("\n--- Просроченные книги ---")
            overdue = library.overdue_books()
            if not overdue:
                print("Нет просроченных книг")
            else:
                for loan in overdue:
                    book = library.books.get(loan.book_id)
                    book_title = book.title if book else loan.book_id
                    days = loan.days_overdue()
                    print(f"\nКнига: {book_title}")
                    print(f"  Пользователь: {loan.user_name}")
                    print(f"  Дата возврата: {loan.return_date.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"  Просрочено на: {days} дней")
        
        elif choice == "4":
            print("\n--- Пользователи с наибольшим количеством книг ---")
            top_users = library.get_top_users(10)
            if not top_users:
                print("В библиотеке нет пользователей")
            else:
                for i, user_info in enumerate(top_users, 1):
                    print(f"{i}. {user_info['name']} - {user_info['count']} книг(и)")
                    if user_info['borrowed_books']:
                        for book_title in user_info['borrowed_books']:
                            print(f"   - {book_title}")
        
        elif choice == "0":
            break
        else:
            print("Неверный выбор")


def save_data_menu(library: Library):
    """Меню сохранения данных."""
    print("\n--- Сохранение данных ---")
    filename = input("Введите имя файла (по умолчанию: library_data.json): ").strip()
    if not filename:
        filename = "library_data.json"
    
    if library.save_to_file(filename):
        print(f"Данные успешно сохранены в файл '{filename}'")
    else:
        print("Ошибка при сохранении данных")


def load_data_menu(library: Library):
    """Меню загрузки данных."""
    print("\n--- Загрузка данных ---")
    filename = input("Введите имя файла (по умолчанию: library_data.json): ").strip()
    if not filename:
        filename = "library_data.json"
    
    if library.load_from_file(filename):
        print(f"Данные успешно загружены из файла '{filename}'")
    else:
        print("Ошибка при загрузке данных")


def main():
    """Главная функция программы."""
    library = Library()
    
    # Попытка загрузить данные при запуске
    print("Попытка загрузить данные из library_data.json...")
    library.load_from_file("library_data.json")
    
    while True:
        print_menu()
        choice = input("\nВыберите действие: ").strip()
        
        if choice == "1":
            add_book_menu(library)
        elif choice == "2":
            remove_book_menu(library)
        elif choice == "3":
            add_user_menu(library)
        elif choice == "4":
            remove_user_menu(library)
        elif choice == "5":
            borrow_book_menu(library)
        elif choice == "6":
            return_book_menu(library)
        elif choice == "7":
            reserve_book_menu(library)
        elif choice == "8":
            show_reports_menu(library)
        elif choice == "9":
            save_data_menu(library)
        elif choice == "10":
            load_data_menu(library)
        elif choice == "0":
            # Предложение сохранить данные перед выходом
            save_choice = input("\nСохранить данные перед выходом? (y/n): ").strip().lower()
            if save_choice == 'y':
                library.save_to_file("library_data.json")
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
        
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()

