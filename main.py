import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import unicodedata
import json

headers = Headers(os='win', browser='yandex')

HH = 'https://spb.hh.ru/'
HH_ARTICLLE = f'{HH}/search/vacancy?area=1&area=2&search_field=description&search_field=name&search_field=company_name&' \
              f'text=Python+django+flask&from=suggest_post&ored_clusters=true&enable_snippets=true'


def page_url(url):
    return requests.get(url, headers=headers.generate())


def main():
    main_html = page_url(HH_ARTICLLE).text
    soup = BeautifulSoup(main_html, features='lxml')
    publikac = soup.find_all('div', class_='serp-item')
    res = []
    for publik in publikac:
        kompaniya = publik.find('a', class_='bloko-link bloko-link_kind-tertiary').text
        kompaniya = unicodedata.normalize('NFKD', kompaniya)

        gorod = publik.find(class_='bloko-text', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
        gorod = unicodedata.normalize('NFKD', gorod)

        if publik.find('span', class_='bloko-header-section-3'):
            zarplata = publik.find('span', class_='bloko-header-section-3').text
        else:
            zarplata = 'Не указанно'
        zarplata = unicodedata.normalize('NFKD', zarplata)

        link = publik.find('a')['href']

        res.append({
            'Компания': kompaniya,
            'Город': gorod,
            'Зарплата': zarplata,
            'Сылка': link
        })

        with open('file.json', 'w', encoding='utf-8') as file:
            json.dump(res, file, ensure_ascii=False, indent=4)
    return res


if __name__ == '__main__':
    print(main())
