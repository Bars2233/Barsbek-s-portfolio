import requests
from bs4 import BeautifulSoup
import lxml
from fake_useragent import UserAgent
import pandas as pd
import openpyxl

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}
url = "https://www.nbkr.kg/index1.jsp?item=1562&lang=RUS"
response = requests.get(url, headers=headers).text
with open ("pars_project_2.html" , "w" , encoding="utf-8") as file:
    file.write(response)
with open ("pars_project_2.html" , "r" , encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
all_data = []

table = soup.find('table', attrs={'width': '80%', 'border': '1'})
if table:
    rows = table.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) >= 3:
            all_data.append({
                'Код': cols[0].text.strip(),
                'Валюта': cols[1].text.strip(),
                'Курс': cols[2].text.strip().replace(',', '.') # Меняем запятую на точку для расчетов
            })

#  превращаем список в таблицу и сохраняем
df = pd.DataFrame(all_data)
df.to_excel('NBKR_Rates.xlsx', index=False)

print("Файл NBKR_Rates.xlsx создан! Проверь папку проекта.")
