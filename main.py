"""Точка входа для запуска приложения библиотеки."""

from library import Library


def main() -> None:
    """Временная функция запуска приложения."""
    library = Library(name="My Library")
    print(f"Библиотека «{library.name}» готова к настройке.")


if __name__ == "__main__":
    main()

