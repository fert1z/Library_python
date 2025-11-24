"""Модель книги."""

from dataclasses import dataclass


@dataclass
class Book:
    """Описание книги."""

    title: str
    author: str
    isbn: str

