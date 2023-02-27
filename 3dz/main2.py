import requests
from bs4 import BeautifulSoup
import lxml
from fake_headers import Headers
import re
import json
from Decor import logger
list_vacancys = []
@logger("logs")
def get_headers():
    headers = Headers(browser="chrome", os="win", headers=True)
    header = headers.generate()
    return header
host = "https://spb.hh.ru/search/vacancy?area=1&area=2&search_field=name&search_field=company_name&search_field=description&enable_snippets=true&text=python"
res = requests.get(host, headers= get_headers())
html_txt = res.text
soup = BeautifulSoup(html_txt, features="lxml")
# res = requests.get("https://2ip.ru")
# txt = res.text
vacancys = soup.find_all("div", class_="serp-item")
for vacancy in vacancys:
    link = vacancy.find("a", class_="serp-item__title")["href"]
    res = requests.get(link, headers= get_headers())
    html_vacancy = res.text
    soup = BeautifulSoup(html_vacancy, features="lxml")
    title = soup.find("h1").text
    salary = soup.find("div", class_="vacancy-title").find("span", class_="bloko-header-section-2 bloko-header-section-2_lite").text
    company = soup.find("div", class_="vacancy-company-details").find("span", class_="bloko-header-section-2 bloko-header-section-2_lite").text
    city = vacancy.find("div", class_="vacancy-serp-item__info").find_all("div", class_="bloko-text")
    patt = "^(\w+-?\w*)"
    res_city = re.match(patt, city[1].text).group(1)
    info = soup.find("div", class_="vacancy-branded-user-content")
    if info == None:
        info = soup.find("div", class_="g-user-content")
    txt = info.text
    if re.search(r"([D|d]\s?[J|j]ango)|([F|f]lask)", txt) != None:
        dict = {"Вакансия":title, "Ссылка":link,"Зарплата":salary,"Компания":company,"Город":res_city}
        list_vacancys.append(dict)
with open("hh.json", "w", encoding="utf-8") as file:
    json.dump(list_vacancys, file, indent=5, ensure_ascii=False)