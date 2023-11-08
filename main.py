import requests
from bs4 import BeautifulSoup as BS
import csv

def get_html(url):
    response = requests.get(url)
    return response.text

def get_data(html):
    soup = BS(html, 'lxml')
    catalog = soup.find('div', class_='search-results-table')
    cars_title = catalog.find_all('h2', class_= "name")
    cars_price = catalog.find_all('div', class_='block price')
    cars_img = catalog.find_all('div', class_="list-item list-label")
    cars_info = catalog.find_all('div', class_="block info-wrapper item-info-wrapper")
    
    for names, price, image, info in zip(cars_title, cars_price, cars_img, cars_info):
        try:
            titles = names.text.strip()
        except:
            titles=''
    
        try:
            prices = price.find('strong').text
        except:
            prices=''
        
        try:
            images = image.find('img').get('data-src')
        except:
            images=''
    
        try:
            infos = info.text.split()
            infos = ' '.join(infos)
        except:
            infos=''


        data = {
            'titles': titles,
            'prices': prices,
            'images': images,
            'infos' : infos
        }
        write_csv(data)

def write_csv(data):
    with open('mashina_kg.csv', 'a') as csv_file:
        names = ['titles', 'prices', 'images', 'infos']
        writer = csv.DictWriter(csv_file, delimiter='|', fieldnames=names)
        writer.writerow(data)


def get_last_page(html):
    soup = BS(html, 'lxml')
    pagination = soup.find('ul', class_='pagination')
    if pagination:
        last_page_link = pagination.find('a', class_='page-link', string='15')
        if last_page_link:
            last_page = int(last_page_link.get('href').split('=')[-1])
            return last_page
    return 1

def main():
    url = 'https://www.mashina.kg/search/all/all/?currency=2&sort_by=upped_at%20desc'
    html = get_html(url)
    get_data(html)
    last_page = get_last_page(html)

    for page in range(1, 20):
        url = f'https://www.mashina.kg/search/all/all/?currency=2&sort_by=upped_at+desc&page={page}'
        html = get_html(url)
        get_data(html)

if __name__ == '__main__':
    main()
