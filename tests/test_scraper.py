from __future__ import annotations

from pathlib import Path

import pytest

from scraper.export import write_outputs
from scraper.models import Book
from scraper.parser import (
    catalogue_page_url,
    parse_category_from_product_page,
    parse_listing_page,
)
from scraper.scrape import scrape_books
from scraper.validate import dedupe_books, validate_books

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def listing_html() -> str:
    return (FIXTURES / "catalogue_page-1.html").read_text(encoding="utf-8")


@pytest.fixture
def book_html() -> str:
    return (FIXTURES / "book_a-light-in-the-attic.html").read_text(encoding="utf-8")


def test_catalogue_page_url():
    assert catalogue_page_url(1).endswith("catalogue/page-1.html")


def test_parse_listing_page(listing_html: str):
    books = parse_listing_page(listing_html, catalogue_page_url(1))
    assert len(books) == 20
    first = books[0]
    assert first["title"] == "A Light in the Attic"
    assert first["price"] == 51.77
    assert first["rating"] == 3
    assert first["availability"] == "In stock"
    assert first["product_url"].endswith("a-light-in-the-attic_1000/index.html")


def test_parse_category_from_product_page(book_html: str):
    assert parse_category_from_product_page(book_html) == "Poetry"


def test_dedupe_books():
    sample = Book("A", 1.0, 5, "In stock", "Poetry", "https://example.com/a")
    dupes = [sample, sample]
    assert len(dedupe_books(dupes)) == 1


def test_validate_books_rejects_bad_rating():
    bad = Book("A", 10.0, 6, "In stock", "Poetry", "https://example.com/a")
    errors = validate_books([bad])
    assert any("rating" in err for err in errors)


class FixtureFetcher:
    def __init__(self, listing_html: str, book_html: str) -> None:
        self.listing_html = listing_html
        self.book_html = book_html

    def get(self, url: str) -> str:
        if "page-1.html" in url:
            return self.listing_html
        if "/catalogue/" in url:
            return self.book_html
        raise AssertionError(f"Unexpected URL in test fetcher: {url}")


def test_scrape_books_with_fixtures(listing_html: str, book_html: str):
    fetcher = FixtureFetcher(listing_html, book_html)
    books = scrape_books(pages=1, fetcher=fetcher)
    assert len(books) == 20
    assert all(book.category for book in books)
    assert books[0].category == "Poetry"


def test_write_outputs(tmp_path: Path):
    books = [
        Book(
            title="A Light in the Attic",
            price=51.77,
            rating=3,
            availability="In stock",
            category="Poetry",
            product_url="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
        )
    ]
    csv_path, xlsx_path = write_outputs(books, tmp_path)
    assert csv_path.exists()
    assert xlsx_path.exists()
    assert "A Light in the Attic" in csv_path.read_text(encoding="utf-8")
