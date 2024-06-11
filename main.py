import requests
from fake_headers import Headers
import bs4
import json


def get_fake_headers():
    return Headers(browser='chrome', os='mac').generate()


response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=get_fake_headers())
main_page_data = bs4.BeautifulSoup(response.text, features='lxml')
vacancies_tags = main_page_data.findAll('div', class_='vacancy-card--z_UXteNo7bRGzxWVcL7y font-inter')
parsed_data = []

for vacancy_tag in vacancies_tags:
    a_tag = vacancy_tag.find('h2', class_='bloko-header-section-2').find('a', class_='bloko-link', target='_blank')
    link = a_tag['href']
    vacancy_response = requests.get(link, headers=get_fake_headers())
    vacancy_page_data = bs4.BeautifulSoup(vacancy_response.text, features='lxml')
    description_tag = vacancy_page_data.find('div', class_='g-user-content')
    if not description_tag:
        description = ''
    else:
        description = description_tag.text
    if 'Django' not in description and 'Flask' not in description:
        continue
    name = a_tag.find('span', class_='vacancy-name--c1Lay3KouCl7XasYakLk serp-item__title-link').text
    salary_tag = vacancy_tag.find('span', class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni compensation-text--kTJ0_rp54B2vNeZ3CTt2 separate-line-on-xs--mtby5gO4J0ixtqzW38wh')
    if not salary_tag:
        salary = ''
    else:
        salary = salary_tag.text.replace('\u202f', '.').replace('\xa0', ' ')
    company = vacancy_tag.find('span', class_='company-info-text--vgvZouLtf8jwBmaD1xgp').text.replace('\xa0', ' ')
    city = vacancy_tag.find('div', class_='info-section--N695JG77kqwzxWAnSePt').find('span', class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni').text
    parsed_data.append(
        {
            'name': name,
            'link': link,
            'salary': salary,
            'company': company,
            'city': city
        }
    )

with open('vacancies.json', 'w') as f:
    f.write(json.dumps(parsed_data, ensure_ascii=False, indent=4))
