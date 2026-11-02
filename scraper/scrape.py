from __future__ import annotations

from scraper.client import HttpClient, PageFetcher
from scraper.models import Book
from scraper.parser import catalogue_page_url, parse_category_from_product_page, parse_listing_page
from scraper.validate import dedupe_books, validate_books


class ScrapeError(Exception):
    pass


def scrape_books(
    *,
    pages: int,
    fetcher: PageFetcher | None = None,
    delay_seconds: float = 0.25,
) -> list[Book]:
    if pages < 1:
        raise ScrapeError("--pages must be at least 1")

    client = fetcher if fetcher is not None else HttpClient(delay_seconds=delay_seconds)
    books: list[Book] = []

    for page in range(1, pages + 1):
        listing_url = catalogue_page_url(page)
        listing_html = client.get(listing_url)
        partials = parse_listing_page(listing_html, listing_url)

        for partial in partials:
            missing = [k for k, v in partial.items() if v is None and k != "category"]
            if missing:
                raise ScrapeError(
                    f"Incomplete listing data on {listing_url}: missing {', '.join(missing)}"
                )

            detail_html = client.get(partial["product_url"])
            category = parse_category_from_product_page(detail_html)
            if not category:
                raise ScrapeError(f"Could not parse category for {partial['product_url']}")

            books.append(
                Book(
                    title=partial["title"],
                    price=partial["price"],
                    rating=partial["rating"],
                    availability=partial["availability"],
                    category=category,
                    product_url=partial["product_url"],
                )
            )

    books = dedupe_books(books)
    errors = validate_books(books)
    if errors:
        sample = "; ".join(errors[:5])
        extra = f" (+{len(errors) - 5} more)" if len(errors) > 5 else ""
        raise ScrapeError(f"Validation failed: {sample}{extra}")

    return books
