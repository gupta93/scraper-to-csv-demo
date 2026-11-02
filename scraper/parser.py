from __future__ import annotations

import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

BASE_SITE = "https://books.toscrape.com/"

RATING_WORDS = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}

PRICE_RE = re.compile(r"[\d.]+")


def rating_from_class(star_rating_el) -> int | None:
    if star_rating_el is None:
        return None
    classes = star_rating_el.get("class", [])
    for name in classes:
        if name in RATING_WORDS:
            return RATING_WORDS[name]
    return None


def parse_price(text: str) -> float | None:
    match = PRICE_RE.search(text.replace(",", ""))
    if not match:
        return None
    return float(match.group())


def parse_availability(availability_el) -> str | None:
    if availability_el is None:
        return None
    text = availability_el.get_text(" ", strip=True)
    return text or None


def parse_listing_page(html: str, page_url: str) -> list[dict]:
    """Parse a catalogue listing page into partial book records."""
    soup = BeautifulSoup(html, "html.parser")
    books: list[dict] = []

    for article in soup.select("article.product_pod"):
        title_link = article.select_one("h3 a")
        if title_link is None:
            continue

        relative_href = title_link.get("href")
        if not relative_href:
            continue

        title = title_link.get("title") or title_link.get_text(strip=True)
        product_url = urljoin(page_url, relative_href)

        rating = rating_from_class(article.select_one("p.star-rating"))
        price = parse_price(article.select_one("p.price_color").get_text(strip=True))
        availability = parse_availability(article.select_one("p.availability"))

        books.append(
            {
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability,
                "product_url": product_url,
            }
        )

    return books


def parse_category_from_product_page(html: str) -> str | None:
    """Return the book's category from breadcrumb (second-to-last crumb)."""
    soup = BeautifulSoup(html, "html.parser")
    crumbs = soup.select("ul.breadcrumb li")
    if len(crumbs) < 2:
        return None

    # Last item is the book title (active); category is usually the one before it.
    category_li = crumbs[-2]
    link = category_li.select_one("a")
    if link is not None:
        return link.get_text(strip=True)
    return category_li.get_text(strip=True) or None


def catalogue_page_url(page: int) -> str:
    return urljoin(BASE_SITE, f"catalogue/page-{page}.html")
