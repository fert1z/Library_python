"""Точка входа для запуска приложения библиотеки."""

from library import Library


def display_menu() -> None:
    """Отображает главное меню программы."""
    print("\n" + "=" * 50)
    print("ГЛАВНОЕ МЕНЮ БИБЛИОТЕКИ")
    print("=" * 50)
    print("1. Добавить книгу")
    print("2. Удалить книгу")
    print("3. Добавить пользователя")
    print("4. Удалить пользователя")
    print("5. Выдать книгу")
    print("6. Вернуть книгу")
    print("7. Забронировать книгу")
    print("8. Показать отчёты")
    print("0. Выход")
    print("=" * 50)


def main() -> None:
    """Главный цикл приложения."""
    library = Library(name="My Library")
    print(f"Библиотека «{library.name}» готова к работе.")

    while True:
        display_menu()
        choice = input("\nВыберите пункт меню: ").strip()

        if choice == "0":
            print("До свидания!")
            break
        elif choice == "1":
            # Добавить книгу
            try:
                title = input("Введите название книги: ").strip()
                author = input("Введите автора книги: ").strip()
                if not title or not author:
                    print("Ошибка: название и автор не могут быть пустыми.")
                    continue
                book = library.add_book(title, author)
                print(f"Книга добавлена: {book}")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "2":
            # Удалить книгу
            try:
                book_id = input("Введите ID книги для удаления: ").strip()
                if library.remove_book(book_id):
                    print(f"Книга {book_id} успешно удалена.")
                else:
                    print(f"Книга {book_id} не найдена.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "3":
            # Добавить пользователя
            try:
                name = input("Введите имя пользователя: ").strip()
                if not name:
                    print("Ошибка: имя не может быть пустым.")
                    continue
                user = library.add_user(name)
                print(f"Пользователь добавлен: {user}")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "4":
            # Удалить пользователя
            try:
                user_id = input("Введите ID пользователя для удаления: ").strip()
                if library.remove_user(user_id):
                    print(f"Пользователь {user_id} успешно удалён.")
                else:
                    print(f"Пользователь {user_id} не найден.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "5":
            # Выдать книгу
            try:
                user_id = input("Введите ID пользователя: ").strip()
                book_id = input("Введите ID книги: ").strip()
                loan = library.borrow_book(user_id, book_id)
                print(f"Книга выдана. Срок возврата: {loan.due_date}")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "6":
            # Вернуть книгу
            try:
                user_id = input("Введите ID пользователя: ").strip()
                book_id = input("Введите ID книги: ").strip()
                library.return_book(user_id, book_id)
                print("Книга успешно возвращена.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "7":
            # Забронировать книгу
            try:
                user_id = input("Введите ID пользователя: ").strip()
                book_id = input("Введите ID книги: ").strip()
                library.reserve_book(user_id, book_id)
                print("Книга успешно забронирована.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "8":
            # Показать отчёты
            print("\n" + "=" * 50)
            print("ОТЧЁТЫ")
            print("=" * 50)
            
            # Отчёт по всем книгам
            print("\n--- Все книги ---")
            books_report = library.get_all_books_report()
            if books_report:
                for book in books_report:
                    print(f"ID: {book['id']}, Название: {book['title']}, "
                          f"Автор: {book['author']}, Статус: {book['status']}")
            else:
                print("Книг нет.")
            
            # Пользователи и их книги
            print("\n--- Пользователи и их книги ---")
            users_books = library.get_users_and_their_books()
            if users_books:
                for user_info in users_books:
                    books_list = ", ".join(user_info['borrowed_books']) if user_info['borrowed_books'] else "нет книг"
                    print(f"{user_info['name']} (ID: {user_info['user_id']}): {books_list}")
            else:
                print("Пользователей нет.")
            
            # Просроченные книги
            print("\n--- Просроченные книги ---")
            overdue = library.get_overdue_books()
            if overdue:
                for item in overdue:
                    print(f"Книга: {item['book_title']} (ID: {item['book_id']}), "
                          f"Пользователь: {item['user_name']} (ID: {item['user_id']}), "
                          f"Просрочено дней: {item['days_overdue']}")
            else:
                print("Просроченных книг нет.")
            
            # Топ читателей
            print("\n--- Топ читателей ---")
            top_readers = library.get_top_readers()
            if top_readers:
                for reader in top_readers:
                    print(f"{reader['name']} (ID: {reader['user_id']}): {reader['books_count']} книг")
            else:
                print("Читателей нет.")
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()

