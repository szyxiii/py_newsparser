import requests
from bs4 import BeautifulSoup


class Parser:
    title = "Parser"
    url_schema = "none"

    proxies = {
        # "http": "http://77.43.149.252:8080",
        # "https": "https://77.43.149.252:8080",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.465 (Edition Yx GX)"
    }

    def get_content(self, query):
        url = self.url_schema.format(query)
        response = requests.get(url, proxies=self.proxies, headers=self.headers)
        return response.content


class YandexParser(Parser):
    title = "Яндекс.Новости"
    url_schema = "https://newssearch.yandex.ru/yandsearch?text={0}&rpt=nnews2&grhow=clutop&nsbr=1"

    def parse(self, query):
        print(f"Парсинг {self.title}")

        result = []
        content = self.get_content(query)

        soup = BeautifulSoup(content, 'lxml')
        divs = soup.find_all("div", {"class": "document i-bem"})
        for div in divs:
            title = div.find("div", {"class": "document__title"})
            if not title:
                continue

            a = title.find("a")
            strong = a.find("strong")
            if strong is None:
                continue

            result.append({"title": a.text, "link": a['href']})

        return result


class GoogleParser(Parser):
    title = "Google Новости"
    url_schema = "https://news.google.com/search?q={0}&hl=ru-RU&gl=US&ceid=RU%3Aru"

    def parse(self, query):
        print(f"Парсинг {self.title}")

        result = []
        content = self.get_content(query)

        soup = BeautifulSoup(content, 'lxml')
        divs = soup.find_all("div", {"class": "NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc"})
        for div in divs:
            h3 = div.find("h3", {"class": "ipQwMb ekueJc RD0gLb"})
            if not h3:
                continue

            a = h3.find("a")
            result.append({"title": a.text, "link": "https://news.google.com" + a['href'][1:]})

        return result
