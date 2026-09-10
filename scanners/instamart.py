from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    store: str
    name: str
    price: float
    protein_per_serving: float
    servings: float
    url: str
    location: Optional[str] = None

    @property
    def total_protein(self) -> float:
        return self.protein_per_serving * self.servings

    @property
    def effective_price(self) -> float:
        if self.total_protein <= 0:
            return float("inf")

        return self.price / self.total_protein

    @property
    def qualifies(self) -> bool:
        return self.effective_price < 2.0


def scan_instamart(pin_code: str) -> list[Product]:
    """
    Instamart scanner interface.

    The actual permitted Instamart data source will be connected here.
    For now this returns no products instead of using an unreliable
    or unauthorized scraper.
    """
    return []
