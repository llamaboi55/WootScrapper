# WootScrapper
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {"User-Agent": "Mozilla/5.0"}

categories = {
    "https://www.woot.com/category/electronics/headphones": "Headphones",
    "https://www.woot.com/category/electronics/video-games": "Video Games",
    "https://www.woot.com/category/electronics/phones-accessories": "Phones & Accessories",
    "https://www.woot.com/category/electronics/televisions-projectors": "Televisions & Projectors",
    "https://www.woot.com/category/electronics/home-audio-theater": "Home Audio & Theater",
    "https://www.woot.com/category/electronics/other-electronics": "Other Electronics",
    "https://www.woot.com/category/electronics/cameras-accessories": "Cameras & Accessories",
    "https://www.woot.com/category/electronics/portable-audio": "Portable Audio",
    "https://www.woot.com/category/electronics/security-surveillance": "Security & Surveillance",
    "https://www.woot.com/category/electronics/dj-equipment-musical-instruments": "DJ & Musical Instruments",
    "https://www.woot.com/category/electronics/car-audio-electronics": "Car Audio & Electronics"
}

all_items = []

for url, category_name in categories.items():
    print(f"Scraping: {category_name} - {url}")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.select("ul.product-grid li")

        for product in products:
            try:
                a_tag = product.find("a", href=True)
                if not a_tag:
                    continue

                title_tag = a_tag.find("span", class_="title")
                price_tag = a_tag.find("span", class_="price")
                list_price_tag = a_tag.find("span", class_="list-price")
                image_tag = a_tag.find("img")

                if not title_tag or not price_tag:
                    continue

                title = title_tag.get_text(strip=True)

                price_text = price_tag.get_text(strip=True).replace("$", "").replace(",", "")
                price_values = [float(p.strip()) for p in price_text.split("–") if p.strip().replace(".", "").isdigit()]
                price = max(price_values) if price_values else None

                if list_price_tag:
                    list_text = list_price_tag.get_text(strip=True).replace("$", "").replace(",", "")
                    list_values = [float(p.strip()) for p in list_text.split("–") if p.strip().replace(".", "").isdigit()]
                    list_price = max(list_values) if list_values else None
                else:
                    list_price = None

                discount = round(((list_price - price) / list_price) * 100, 2) if list_price else None

                if price and price >= 250:
                    all_items.append({
                        "Category": category_name,
                        "Title": title,
                        "Price": price,
                        "List Price": list_price,
                        "Discount (%)": discount,
                        "Link": a_tag["href"],
                        "Image URL": image_tag["src"] if image_tag else None
                    })

            except Exception as e:
                print("  Error parsing product:", e)
                continue

    except Exception as e:
        print(f"  Failed to scrape {url}: {e}")
        continue

df = pd.DataFrame(all_items)
df.sort_values(by=["Category", "Title"], inplace=True)
df.to_csv("woot_electronics_250plus_by_category.csv", index=False)

print("\nScraping complete.")
print(f"Total items found: {len(df)}")
print("Saved to: woot_electronics_250plus_by_category.csv")
