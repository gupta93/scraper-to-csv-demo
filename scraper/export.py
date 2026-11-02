from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook

from scraper.models import Book

FIELDNAMES = [
    "title",
    "price",
    "rating",
    "availability",
    "stock_count",
    "category",
    "product_url",
]


def write_csv(books: list[Book], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for book in books:
            writer.writerow(
                {
                    "title": book.title,
                    "price": f"{book.price:.2f}",
                    "rating": book.rating,
                    "availability": book.availability,
                    "stock_count": "" if book.stock_count is None else book.stock_count,
                    "category": book.category,
                    "product_url": book.product_url,
                }
            )


def write_xlsx(books: list[Book], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Books"
    sheet.append(FIELDNAMES)
    for book in books:
        sheet.append(
            [
                book.title,
                book.price,
                book.rating,
                book.availability,
                book.stock_count,
                book.category,
                book.product_url,
            ]
        )
    workbook.save(path)


def write_outputs(books: list[Book], out_dir: Path) -> tuple[Path, Path]:
    csv_path = out_dir / "books.csv"
    xlsx_path = out_dir / "books.xlsx"
    write_csv(books, csv_path)
    write_xlsx(books, xlsx_path)
    return csv_path, xlsx_path
