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

URL = config("URL")
CSV_FILE = "mashinakg.csv"

def get_response_data(headers, url):
    response = requests.get(url, headers=headers)
    return response

def content(html_text):
    soup = BeautifulSoup(html_text, "html.parser")

    all_data = soup.find_all("div", class_="list-item list-label")
    car_content = []

    for i in all_data:
        car_content.append(
            {
                "price": i.find("div", class_="block price").get_text().replace(' ', '').strip()
            }
        )
    print(car_content)
#
# def save_csv(cars: list) -> None:
#     with open(CSV_FILE, "w") as f:
#         writer = csv.writer(f, delimeter=",")
#         writer.writerow(["Название", "Картинка", "Описание", "Количество просмотров", "Цена в долларах", "Цена в сомах"])
#     for i in cars:
#         writer.writerow([i["name"], i["image"], i["description"], i["views"], i["price_dollar"], i["price_som"]])
#
#     print("Запись CSV файла завершена!")

def execute():
    html_content = get_response_data(HEADERS, URL)
    if html_content.status_code == 200:
        cars = content(html_content.text)




execute()
