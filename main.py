"""Точка входа для запуска приложения библиотеки."""

from library import Library


def display_menu() -> None:
    """Отображает главное меню программы."""
    print("\n" + "=" * 50)
    print("ГЛАВНОЕ МЕНЮ БИБЛИОТЕКИ")
    print("=" * 50)
    print("1. Добавить книгу")
    print("2. Добавить пользователя")
    print("3. Выдать книгу")
    print("4. Вернуть книгу")
    print("5. Забронировать книгу")
    print("6. Просмотреть все книги")
    print("7. Просмотреть пользователей и их книги")
    print("8. Просмотреть просроченные книги")
    print("9. Просмотреть топ читателей")
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
            print("Функция в разработке")
        elif choice == "2":
            print("Функция в разработке")
        elif choice == "3":
            print("Функция в разработке")
        elif choice == "4":
            print("Функция в разработке")
        elif choice == "5":
            print("Функция в разработке")
        elif choice == "6":
            print("Функция в разработке")
        elif choice == "7":
            print("Функция в разработке")
        elif choice == "8":
            print("Функция в разработке")
        elif choice == "9":
            print("Функция в разработке")
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()

