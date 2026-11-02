from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Book:
    title: str
    price: float
    rating: int
    availability: str
    stock_count: int | None
    category: str
    product_url: str

    def dedupe_key(self) -> str:
        return self.product_url
