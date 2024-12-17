import csv
import json
import random
import time

import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, url):
        self._headers = {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "cookie": "ppms_privacy_5175571d-16e9-40c5-9eca-bcb6d5e49f20={%22visitorId%22:%2233791f38-d7b4-492c-8de2-5ff7c8419e1e%22%2C%22domain%22:{%22normalized%22:%22www.supermonitoring.com%22%2C%22isWildcard%22:false%2C%22pattern%22:%22www.supermonitoring.com%22}%2C%22consents%22:{%22analytics%22:{%22status%22:1%2C%22updatedAt%22:%222024-12-16T20:12:39.639Z%22}%2C%22conversion_tracking%22:{%22status%22:1%2C%22updatedAt%22:%222024-12-16T20:12:39.639Z%22}%2C%22user_feedback%22:{%22status%22:1%2C%22updatedAt%22:%222024-12-16T20:12:39.639Z%22}%2C%22marketing_automation%22:{%22status%22:1%2C%22updatedAt%22:%222024-12-16T20:12:39.639Z%22}}%2C%22staleCheckpoint%22:%222024-12-16T20:12:37.615Z%22}; _ga=GA1.1.1788900189.1734379958; _ga_KLCW8G3CY6=GS1.1.1734379956.1.0.1734379959.0.0.0"
        }
        self._url = url
        self._films_titles = list()
        self._films_years = list()
        self._films_descriptions = list()
        self._films_data_list = list()

    def _get_titles(self, films):
        for film in films:
            title = film.find("h2").text.split('(')
            film_title = title[0].strip()
            if len(title) > 1:
                film_year = title[1]
                self._films_years.append(film_year[:-1])
            self._films_titles.append(film_title)

    def _get_infos(self, infos):
        for info in infos[2:]:
            description = info.find("p").text
            self._films_descriptions.append(description.strip())

    def _make_request(self):
        req = requests.get(self._url, self._headers, timeout=30)

        with open(f"data/films.html", "w", encoding="UTF-8") as file:
            file.write(req.text)

    def _write_to_json(self):
        with open("data/films_data.json", "a", encoding="UTF-8") as file:
            json.dump(self._films_data_list, file, indent=4, ensure_ascii=False)

    def _write_to_csv(self):
        with open(f"data/recipes_data.csv", "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self._films_data_list)


    def get_data(self):
        self._make_request()
        with open(f"data/films.html", encoding="UTF-8") as file:
            src = file.read()
        soup = BeautifulSoup(src, "lxml")

        films = soup.find_all("div", class_="article-detail_tag article-detail_tag_h2")
        self._get_titles(films)

        films_infos = soup.find_all("article", class_="article-detail_tag article-detail_tag_p")
        self._get_infos(films_infos)

        self._films_data_list = list(zip(self._films_titles, self._films_years, self._films_descriptions))

        time.sleep(random.randrange(2, 4))

        self._write_to_json()
        self._write_to_csv()


if __name__ == "__main__":
    films_url = 'https://www.thevoicemag.ru/lifestyle/films/luchshie-novogodnie-filmy/'
    films_parser = Parser(films_url)
    films_parser.get_data()