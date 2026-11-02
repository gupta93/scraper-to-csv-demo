from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scraper.export import write_outputs
from scraper.scrape import ScrapeError, scrape_books


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scrape books.toscrape.com into CSV and Excel files.",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=50,
        help="Number of catalogue pages to scrape (default: 50).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("output"),
        help="Output directory for books.csv and books.xlsx (default: output/).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.25,
        help="Seconds to wait between HTTP requests (default: 0.25).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        books = scrape_books(pages=args.pages, delay_seconds=args.delay)
        csv_path, xlsx_path = write_outputs(books, args.out)
    except ScrapeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {len(books)} books to {csv_path} and {xlsx_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
