import requests
from bs4 import BeautifulSoup


class Crawler:

    URL = 'https://namu.wiki/w/소녀전선/인형제조'

    TableKeyword = '제조 시간'

    def __init__(self):
        html = self.fetch()

        self.Table = self.parse(html)

    def fetch(self):
        resp = requests.get(self.URL)
        return resp.text

    def parse(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        tables = soup.select('table.wiki-table')

        table = self.check_tables(tables)

        parsed = self.parse_table(table)

        return parsed

    def check_tables(self, tables):
        index = [idx for idx, i in enumerate(tables) if i.find(text=self.TableKeyword) is not None]
        if len(index) == 1:
            return tables[index[0]]
        else:
            raise ValueError(f"Table check error. {len(index)} target table(s) found.")

    def parse_table(self, table):
        parsed_table = []
        rows = [row.findAll('td') for row in table.findAll('tr')[1:]]
        for idx, row in enumerate(rows):
            if len(row) == 3:
                row = rows[idx-1][0], *row
            parsed_table.append(self.parse_cells(row))
        return parsed_table

    def parse_cells(self, cells):
        time = self._parse_time(cells[0])
        grade = self._parse_grade(cells[1])
        cls = self._parse_class(cells[2])
        dolls = self._parse_dolls(cells[3])
        return time, grade, cls, dolls

    @staticmethod
    def _parse_time(cell):
        return [i.strip() for i in cell.text.split(':')]

    @staticmethod
    def _parse_grade(cell):
        return len(cell.text)

    @staticmethod
    def _parse_class(cell):
        image_title = cell.select_one('a').get('title')
        return image_title.split('_')[1].split('.')[0]

    @staticmethod
    def _parse_dolls(cell):
        dolls = cell.findAll('a')
        return [(i.text, i.get('href')) for i in dolls if not i.get('href').startswith('#')]

if __name__ == '__main__':
    crawled = Crawler()
    for i in crawled.Table:
        print(i)