"""Модель пользователя библиотеки."""

from dataclasses import dataclass


@dataclass
class User:
    """Описание читателя."""

    name: str
    email: str

