import unittest
import os
import re
from bs4 import BeautifulSoup

def build_bridge(path, start, end):
    """возвращает список страниц, по которым можно перейти по ссылкам со start_page на
    end_page, начальная и конечная страницы включаются в результирующий список"""

    # напишите вашу реализацию логики по вычисления кратчайшего пути здесь
    def build_tree(start, end, path):
        link_re = re.compile(r"(?<=/wiki/)[\w()]+")
        files = dict.fromkeys(os.listdir(path), False)
        current_links = [start]
        while current_links:
            new_links = []
            for name in current_links:
                with open("{}{}".format(path, name)) as data:
                    links = re.findall(link_re, data.read())
                for link in links:
                    if files.get(link) is False:
                        files[link] = name
                        if link == end:
                            return files
                        new_links.append(link)
            current_links = new_links

    files = build_tree(start, end, path)
    current_link, bridge = end, [end]
    while current_link != start:
        current_link = files[current_link]
        bridge.append(current_link)
    return bridge


def get_statistics(path, start_page, end_page):
    """собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
    значение - список со статистикой страницы"""

    # получаем список страниц, с которых необходимо собрать статистику 
    pages = build_bridge(path, start_page, end_page)
    # напишите вашу реализацию логики по сбору статистики здесь

    statistic = {}
    for page in pages:
        with open("{}{}".format(path, page), encoding="utf-8") as data:
            soup = BeautifulSoup(data, "html")
            body = soup.find(id="bodyContent")

            imgs = len(body.find_all('img', width=lambda x: int(x or 0) > 199))
            headers = sum(
                1 for tag in body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) if tag.get_text()[0] in "ETC"
            )
            lists = sum(1 for tag in body.find_all(['ol', 'ul']) if not tag.find_parent(['ol', 'ul']))

            tag = body.find_next("a")
            linkslen = -1
            while (tag):
                curlen = 1
                for tag in tag.find_next_siblings():
                    if tag.name != 'a':
                        break
                    curlen += 1
                if curlen > linkslen:
                    linkslen = curlen
                tag = tag.find_next("a")

            statistic[page] = [imgs, headers, linkslen, lists]

    return statistic


STATISTICS = {
    'Artificial_intelligence': [8, 19, 13, 198],
    'Binyamina_train_station_suicide_bombing': [1, 3, 6, 21],
    'Brain': [19, 5, 25, 11],
    'Haifa_bus_16_suicide_bombing': [1, 4, 15, 23],
    'Hidamari_no_Ki': [1, 5, 5, 35],
    'IBM': [13, 3, 21, 33],
    'Iron_Age': [4, 8, 15, 22],
    'London': [53, 16, 31, 125],
    'Mei_Kurokawa': [1, 1, 2, 7],
    'PlayStation_3': [13, 5, 14, 148],
    'Python_(programming_language)': [2, 5, 17, 41],
    'Second_Intifada': [9, 13, 14, 84],
    'Stone_Age': [13, 10, 12, 40],
    'The_New_York_Times': [5, 9, 8, 42],
    'Wild_Arms_(video_game)': [3, 3, 10, 27],
    'Woolwich': [15, 9, 19, 38]}

TESTCASES = (
    ('wiki/', 'Stone_Age', 'Python_(programming_language)',
     ['Stone_Age', 'Brain', 'Artificial_intelligence', 'Python_(programming_language)']),

    ('wiki/', 'The_New_York_Times', 'Stone_Age',
     ['The_New_York_Times', 'London', 'Woolwich', 'Iron_Age', 'Stone_Age']),

    ('wiki/', 'Artificial_intelligence', 'Mei_Kurokawa',
     ['Artificial_intelligence', 'IBM', 'PlayStation_3', 'Wild_Arms_(video_game)',
      'Hidamari_no_Ki', 'Mei_Kurokawa']),

    ('wiki/', 'The_New_York_Times', "Binyamina_train_station_suicide_bombing",
     ['The_New_York_Times', 'Second_Intifada', 'Haifa_bus_16_suicide_bombing',
      'Binyamina_train_station_suicide_bombing']),

    ('wiki/', 'Stone_Age', 'Stone_Age',
     ['Stone_Age', ]),
)


class TestBuildBrige(unittest.TestCase):
    def test_build_bridge(self):
        for path, start_page, end_page, expected in TESTCASES:
            with self.subTest(path=path,
                              start_page=start_page,
                              end_page=end_page,
                              expected=expected):
                result = build_bridge(path, start_page, end_page)
                self.assertEqual(result, expected)


class TestGetStatistics(unittest.TestCase):
    def test_build_bridge(self):
        for path, start_page, end_page, expected in TESTCASES:
            with self.subTest(path=path,
                              start_page=start_page,
                              end_page=end_page,
                              expected=expected):
                result = get_statistics(path, start_page, end_page)
                self.assertEqual(result, {page: STATISTICS[page] for page in expected})


if __name__ == '__main__':
    unittest.main()