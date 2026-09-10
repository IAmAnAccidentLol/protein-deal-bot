from dataclasses import dataclass
from typing import Optional


PROTEIN_LIMIT = 2.00


@dataclass
class Product:
    store: str
    name: str
    price: float
    url: str

    # Use ONE of these:
    total_protein_g: Optional[float] = None
    protein_per_serving_g: Optional[float] = None
    servings: Optional[float] = None

    # Or use protein percentage, e.g. 24 means 24g protein per 100g
    protein_per_100g: Optional[float] = None
    pack_size_g: Optional[float] = None

    pin_code: Optional[str] = None

    def calculate_total_protein(self) -> Optional[float]:
        """Calculate total actual protein in the entire pack."""

        if self.total_protein_g is not None:
            return self.total_protein_g

        if (
            self.protein_per_serving_g is not None
            and self.servings is not None
        ):
            return self.protein_per_serving_g * self.servings

        if (
            self.protein_per_100g is not None
            and self.pack_size_g is not None
        ):
            return (self.protein_per_100g / 100) * self.pack_size_g

        return None

    def effective_price(self) -> Optional[float]:
        """Return effective ₹ per gram of actual protein."""

        total_protein = self.calculate_total_protein()

        if total_protein is None or total_protein <= 0:
            return None

        return self.price / total_protein

    def qualifies(self) -> bool:
        """True only when effective cost is below ₹2/g protein."""

        effective = self.effective_price()

        return effective is not None and effective < PROTEIN_LIMIT


def scan_instamart(pin_code: str) -> list[Product]:
    """
    Instamart scanner.

    The actual permitted Instamart product source will be connected here.
    """

    return []


def format_deal(product: Product) -> str:
    effective = product.effective_price()
    total_protein = product.calculate_total_protein()

    return (
        "🚨 PROTEIN DEAL FOUND!\n\n"
        f"🛒 {product.name}\n"
        f"🏪 {product.store}\n"
        f"💰 ₹{product.price:.0f}\n"
        f"🥛 {total_protein:.0f} g actual protein\n"
        f"📊 ₹{effective:.2f}/g protein\n"
        f"📍 PIN: {product.pin_code}\n\n"
        f"🔗 {product.url}"
    )
