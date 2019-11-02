from bs4 import BeautifulSoup
from dataclasses import dataclass
import requests


@dataclass
class Product:
    title: str
    price: str
    currency: str
    image: str
    url: str


def fetch_html(url):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    print(f'Fetching {url}')
    r = requests.get(url, headers=headers)
    return BeautifulSoup(r.text, 'html5lib')


def get_next_url(soup):
    node = soup.find('a', {'class': 'next'})
    if node is not None:
        return node.get('href')


def iter_products(soup):
    def get_title():
        return product.find('a').get('title')

    def get_price():
        return product.find('span', {'class': 'woocommerce-Price-amount'}).get_text()

    def get_url():
        return product.find('a').get('href')

    def get_image():
        return product.find('img', {'class': 'primary_image'}).get('src')

    for product in soup.find_all('div', {'class': 'product-wrapper'}):
        yield Product(
            title=get_title(),
            price=get_price(),
            currency='EUR',
            image=get_image(),
            url=get_url(),
        )


def main():
    url = f'https://shopb2b.ghiblisrl.com/en/shop/'
    while True:
        soup = fetch_html(url)
        for product in iter_products(soup):
            print(product)
        url = get_next_url(soup)
        if url is None:
            return


if __name__ == '__main__':
    main()
