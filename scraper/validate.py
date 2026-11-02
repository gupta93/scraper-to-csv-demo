from __future__ import annotations

from scraper.models import Book


def dedupe_books(books: list[Book]) -> list[Book]:
    seen: set[str] = set()
    unique: list[Book] = []
    for book in books:
        key = book.dedupe_key()
        if key in seen:
            continue
        seen.add(key)
        unique.append(book)
    return unique


def validate_books(books: list[Book]) -> list[str]:
    """Return human-readable validation errors (empty list means OK)."""
    errors: list[str] = []
    for index, book in enumerate(books, start=1):
        prefix = f"Row {index} ({book.product_url})"
        if not book.title.strip():
            errors.append(f"{prefix}: missing title")
        if book.price <= 0:
            errors.append(f"{prefix}: invalid price {book.price}")
        if book.rating not in (1, 2, 3, 4, 5):
            errors.append(f"{prefix}: invalid rating {book.rating}")
        if not book.availability.strip():
            errors.append(f"{prefix}: missing availability")
        if not book.category.strip():
            errors.append(f"{prefix}: missing category")
        if not book.product_url.startswith("http"):
            errors.append(f"{prefix}: invalid product URL")
    return errors
