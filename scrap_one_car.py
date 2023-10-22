from decouple import config
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/118.0.0.0 Safari/537.36",
    "accept": "*/*"
}

URL = config("URL")

# request = requests.get(URL, headers=HEADERS)
# page_code = request.text

with open("mashinakg.html") as file:
    page_code = file.read()

soup = BeautifulSoup(page_code, "html.parser")
all_data = soup.find_all(class_="list-item list-label")

a_tag_info = []
for item in all_data:
    a_tag_info.append(item.find("a"))

car_href_list = []
for i in a_tag_info:
    car_href_list.append("https://www.mashina.kg" + i.get("href"))


car_1 = car_href_list[0]

request = requests.get(car_1, headers=HEADERS)
car_page_code = request.text

soup = BeautifulSoup(car_page_code, "html.parser")

name = soup.find("div", class_="head-left").find("h1").get_text()
print(name)

image = soup.find("div", class_="main-info clr").find("a").get("href")
print(image)

description = soup.find("h2", class_="comment").get_text()
print(description)

views = soup.find("span", class_="listing-icons views").get_text()
print(views)

price_dollar = soup.find("div", class_="price-dollar").get_text() #.replace(" ", "").replace("$", "")
print(price_dollar)

price_som = soup.find("div", class_="price-som").get_text() #.replace(" ", "").replace("сом", "")
print(price_som)
