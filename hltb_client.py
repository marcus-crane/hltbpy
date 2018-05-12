from bs4 import BeautifulSoup
import requests


class HLTBClient:

    @staticmethod
    def query_title(query, req=requests):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        payload = {
            'queryString': query,
            't': 'games',
            'sorthead': 'popular',
            'sortd': 'Normal Order',
            'length_type': 'main',
        }
        r = req.post('https://howlongtobeat.com/search_main.php?page=1',
                     headers=headers, data=payload)
        return r.text

    @staticmethod
    def cleanse_times(time_string):
        time_string = time_string.replace('½', '.5')
        time_string = time_string.replace('&#189;', '.5')
        time_string = time_string.replace('--', '0')
        time_string = time_string.replace(' Hours', '')
        return float(time_string)

    @staticmethod
    def parse_query(query_data):
        data = []
        time_categories = ['Main Story', 'Main + Extra',
                           'Completionist', 'All Styles']
        soup = BeautifulSoup(query_data, 'html.parser')
        results = soup.find_all('div', class_='search_list_details')
        for result in results:
            game = dict()
            game['id'] = int(result.a.attrs['href'].split('id=')[-1])
            game['title'] = result.a.get_text()
            game['playtime'] = dict()
            for index, entry in enumerate(
                    result.find_all('div', class_='center')):
                category = time_categories[index]
                length = entry.get_text().strip()
                game['playtime'][category] = HLTBClient.cleanse_times(length)
            data.append(game)
        return data

    @staticmethod
    def search(title, req=requests):
        query = HLTBClient.query_title(title, req)
        return HLTBClient.parse_query(query)

