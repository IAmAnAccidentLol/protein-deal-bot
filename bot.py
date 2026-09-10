import os
import requests


PROTEIN_LIMIT = 2.00


def calculate_deal(price, protein_per_serving, servings):
    total_protein = protein_per_serving * servings
    effective_price = price / total_protein

    return {
        "price": price,
        "total_protein": total_protein,
        "effective_price": effective_price,
        "qualifies": effective_price < PROTEIN_LIMIT,
    }


def send_telegram(message):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": chat_id,
            "text": message,
        },
        timeout=30,
    )

    response.raise_for_status()


# Temporary test deal
deal = calculate_deal(
    price=1099,
    protein_per_serving=25,
    servings=24,
)

if deal["qualifies"]:
    message = (
        "🚨 PROTEIN DEAL FOUND!\n\n"
        f"💰 Price: ₹{deal['price']:.0f}\n"
        f"🥛 Total protein: {deal['total_protein']:.0f} g\n"
        f"📊 Effective cost: ₹{deal['effective_price']:.2f}/g\n\n"
        "✅ Below ₹2/g protein"
    )

    send_telegram(message)

print(
    f"Price: ₹{deal['price']:.0f} | "
    f"Protein: {deal['total_protein']:.0f} g | "
    f"₹/g: ₹{deal['effective_price']:.2f}"
)
