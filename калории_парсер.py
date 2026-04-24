import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import random
import csv
ua = UserAgent()
url = "https://health-diet.ru/table_calorie/"
headers = {
    "User-Agent": ua.random
}
response = requests.get(url , headers = headers).text
with open("index.html", "w", encoding="utf-8") as file:
    file.write(response)

with open("index.html", "r", encoding="utf-8") as file:
    src = file.read()
soup = BeautifulSoup(src, "lxml")
all_product_links = soup.find_all("a", class_="mzr-tc-group-item-href")
with open("products_info.csv", "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Продукт", "Калорийность", "Белки", "Жиры", "Углеводы", "Категория"])
for link in all_product_links:
    try:
        href = 'https://health-diet.ru' + link["href"]
        title = link.text.strip()
        print(f"--- Парсим категорию: {title} ---")

        response = requests.get(href, headers=headers).text
        soup_level2 = BeautifulSoup(response, "lxml")
        rows = soup_level2.find_all("tr")
        for row in rows:
            try:
                columns = row.find_all("td")
                if len(columns) >= 5:  # Обрабатываем только полные строки
                        name = columns[0].text.strip()
                        calories = columns[1].text.strip()
                        proteins = columns[2].text.strip()
                        fats = columns[3].text.strip()
                        carbs = columns[4].text.strip()
                        with open("products_info.csv", "a", encoding="utf-8-sig", newline="") as file:
                            writer = csv.writer(file, delimiter=";")
                            writer.writerow([name , calories ,proteins , fats , carbs ,title ])
            except Exception:
                continue

        print(f"Готово: {title} записана.")


        time.sleep(random.uniform(1, 2))
    except Exception as e:
        print(f"Ошибка при обработке категории {link}: {e}")
        continue  # Если категория не открылась — идем к следующей