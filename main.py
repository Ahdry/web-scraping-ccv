import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://www.divan.ru"
CATEGORY_URL = f"{BASE_URL}/category/svetilniki"

def get_lighting_sources():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(CATEGORY_URL, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve page: Status {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.select(".catalog-tile")  # селектор товара; может потребоваться корректировка под сайт

    results = []
    for product in products:
        title_tag = product.select_one(".catalog-tile__title")
        price_tag = product.select_one(".catalog-tile-price__value")
        link_tag = product.select_one("a.catalog-tile__link")

        if title_tag and price_tag and link_tag:
            title = title_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)
            link = BASE_URL + link_tag.get("href")
            results.append({"title": title, "price": price, "link": link})

    # Сохраняем результаты в CSV файл
    csv_file = "lighting_sources.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["title", "price", "link"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Saved {len(results)} records to {csv_file}")

if __name__ == "__main__":
    get_lighting_sources()
