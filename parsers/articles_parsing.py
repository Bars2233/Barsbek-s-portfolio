import requests
from bs4 import BeautifulSoup
import json
headers = {
"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"}
url = "https://hi-tech.news/other"
response = requests.get(url, headers = headers).text
soup = BeautifulSoup(response, "lxml")
all_pages_num = soup.find("span", {"class" : "navigations"}).find_all("a")[-1].get("href").replace("/other/page/", "").replace("/", "")
data = []
for i in range(2, int(all_pages_num) + 1):
    r = requests.get(url = f"https://hi-tech.news/other/page/{i}/" , headers=headers).text
    soup = BeautifulSoup(r, "lxml")
    posts = soup.find_all("div", class_ = "post-body")
    for post in posts:
        title = post.find("div", class_ = "title").find("a").text.strip()
        excerpt = post.find("div", class_ = "the-excerpt").text.strip()
        href = "https://hi-tech.news" + post.find("a" , class_ = "post-title-a").get("href")
        data.append({"title" : title, "excerpt" : excerpt, "href" : href})

with open("артикли.json", "w") as f:
    json.dump(data, f, indent = 4 , ensure_ascii = False)
