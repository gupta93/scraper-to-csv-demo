# Website to spreadsheet (demo)

This project is a small, polished example of turning a public website into clean spreadsheet files. It visits the practice bookstore at [books.toscrape.com](https://books.toscrape.com), collects details about every book, and saves the results as **CSV** (opens in Google Sheets, Excel, and most tools) and **Excel** (`.xlsx`).

It is meant as a portfolio piece: reliable enough for real client conversations, simple enough to read without being a developer.

## What you get

For each book, the scraper records:

| Column | Example |
|--------|---------|
| **title** | A Light in the Attic |
| **price** | 51.77 (GBP, numeric in Excel) |
| **rating** | 3 (1–5 stars) |
| **availability** | In stock |
| **category** | Poetry |
| **product_url** | Link back to the book page |

A full run across all **50 catalogue pages** produces **1,000 books**. Sample output is included in the [`output/`](output/) folder.

### Preview (first rows)

| title | price | rating | availability | category |
|-------|------:|-------:|--------------|----------|
| A Light in the Attic | 51.77 | 3 | In stock | Poetry |
| Tipping the Velvet | 53.74 | 1 | In stock | Historical Fiction |
| Soumission | 50.10 | 1 | In stock | Fiction |
| Sharp Objects | 47.82 | 4 | In stock | Mystery |
| Sapiens: A Brief History of Humankind | 54.23 | 5 | In stock | History |

## Quick start

**Requirements:** Python 3.11 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .

python3 -m scraper --pages 50 --out output/
```

When it finishes, open `output/books.csv` or `output/books.xlsx`.

### Useful options

- `--pages N` — scrape only the first `N` catalogue pages (default: 50).
- `--out output/` — folder for `books.csv` and `books.xlsx`.
- `--delay 0.25` — seconds to wait between requests (polite scraping).

## How it works (brief)

1. Download each catalogue page with **requests**, using a clear user-agent, retries, and short delays.
2. Parse HTML with **BeautifulSoup** to read titles, prices, ratings, and stock status.
3. Visit each book page once to read its **category** from the breadcrumb trail.
4. Remove duplicate URLs and validate rows (price, rating range, required fields).
5. Write **CSV** and **Excel** files.

Automated tests use saved HTML fixtures only — **no network** during `pytest`.

## Development

```bash
pip install -e ".[dev]"
ruff check .
pytest
```

Continuous integration runs **ruff** and **pytest** on every push (see [`.github/workflows/ci.yml`](.github/workflows/ci.yml)).

## License

MIT — see [LICENSE](LICENSE).

## Author

Tushar Gupta — portfolio demo for “website → spreadsheet” work.
