from bs4 import BeautifulSoup
import unittest
import os

def parse(path_to_file):
    # Поместите ваш код здесь.
    # ВАЖНО!!!
    # При открытии файла, добавьте в функцию open необязательный параметр
    # encoding='utf-8', его отсутствие в коде будет вызвать падение вашего
    # решения на грейдере с ошибкой UnicodeDecodeError
    with open(path_to_file, encoding="utf-8") as file:
        soup = BeautifulSoup(file, "lxml")
        body = soup.find(id="bodyContent")

        # 0
        imgs = len(body.find_all('img', width=lambda x: int(x or 0) > 199))

        # 1
        headers = sum(
            1 for tag in body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) if tag.get_text()[0] in "ETC"
        )
        
        # 2
        tags = body.find_all("a")
        linkslen = -1

        for tag in tags:
            curlen = 1
            for tag in tag.find_next_siblings():
                if tag.name != 'a':
                    break
                curlen += 1
            if curlen > linkslen:
                linkslen = curlen
            tag = tag.find_next("a")

        # 3
        lists = sum(1 for tag in body.find_all(['ol', 'ul']) if not tag.find_parent(['ol', 'ul']))

        return [imgs, headers, linkslen, lists]


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    unittest.main()