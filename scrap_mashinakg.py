from decouple import config
import requests
from bs4 import BeautifulSoup
import csv

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/118.0.0.0 Safari/537.36",
    "accept": "*/*"
}
CSV_FILE = "mashinakg.csv"

with open(CSV_FILE, "w") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(["Название", "Картинка", "Описание", "Количество просмотров", "Цена в долларах", "Цена в сомах"])
    f.close()

URL = config("URL")

for p in range(1, 15):
    cur_URL = f"{URL}{p}"

    request = requests.get(cur_URL, headers=HEADERS)
    page_code = request.text

    soup = BeautifulSoup(page_code, "html.parser")
    all_data = soup.find_all(class_="list-item list-label")

    a_tag_info = []
    for item in all_data:
        a_tag_info.append(item.find("a"))

    car_href_list = []
    for i in a_tag_info:
        car_href_list.append("https://www.mashina.kg" + i.get("href"))
    if len(car_href_list) == 0:
        break

    cars_data = []
    for href in car_href_list:
        request = requests.get(href, headers=HEADERS)
        car_page_code = request.text
        soup = BeautifulSoup(car_page_code, "html.parser")
        cars_data.append(
            {
                "name": soup.find("div", class_="head-left").find("h1").get_text(),
                "image": soup.find("div", class_="main-info clr").find("a").get("href"),
                "description": soup.find("h2", class_="comment").get_text(),
                "views": soup.find("span", class_="listing-icons views").get_text(),
                "price_dollar": soup.find("div", class_="price-dollar").get_text(),  # .replace(" ", "").replace("$", "")
                "price_som": soup.find("div", class_="price-som").get_text()  # .replace(" ", "").replace("сом", "")
            }
        )
    def save_csv(cars: list) -> None:
        global p
        with open(CSV_FILE, "a") as f:
            writer = csv.writer(f, delimiter=",")
            for i in cars:
                writer.writerow((i.get("name"), i.get("image"), i.get("description"), i.get("views"), i.get("price_dollar"), i.get("price_som")))


            print(f"Парсинг страницы {p} завершен!")

    save_csv(cars_data)

print("Запись данных в CSV файл завершена!")