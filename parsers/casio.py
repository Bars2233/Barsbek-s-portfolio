import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
ua = UserAgent()
# url = 'https://www.mircasio.ru/watch/'
headers = {
    'User-Agent': ua.random
}
# with open("mircasio.html", "wb") as f:
#     f.write(response.content)
# with open("mircasio.html", "rb") as f:
#     src = f.read()
data = []
for i in range(1 ,52):
    link = f"https://www.mircasio.ru/watch/?PAGEN_1={i}"
    soup = BeautifulSoup(requests.get(link , headers=headers).text, "lxml")
    watches = soup.find("div", class_ = 'catalog__content_wrapper row cols-3 product-container').find_all("div", class_ = "col")
    for watch in watches:
        url = "https://www.mircasio.ru" + watch.find("a" , class_ = 'product-item__link').attrs["href"]
        name = watch.find("a" , class_ = 'product-item__link').find('p' , class_ = 'product-item__articul').text.strip()
        price = watch.find("p", class_="product-item__price").get_text(strip=True)
        price = price.replace(".руб", "").strip()
        data.append([name, price , url])
    print(f"спарсили PAGEN = {i}")
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
