import concurrent.futures
from dataclasses import dataclass, asdict
from functools import wraps
import hashlib
from io import StringIO
import os
import shutil
from typing import List

import boto3
import pandas as pd
import requests
import s3fs
from bs4 import BeautifulSoup

fs = s3fs.S3FileSystem(anon=False)
bucket = 'rossi-rei-data'


@dataclass
class Product:
    title: str
    price: str
    currency: str
    image: str
    url: str


@dataclass
class DetailedProduct:
    title: str
    price: str
    currency: str
    url: str
    short_description: str
    sku: str
    categories: List
    images: List
    weight: str
    dimensions: str


def catcher(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return None
    return wrapped


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
    for product in soup.find_all('div', {'class': 'product-wrapper'}):
        yield Product(
            title=catcher(lambda: product.find('a').get('title'))(),
            price=catcher(
                lambda: product.find('span', {'class': 'woocommerce-Price-amount'}).get_text().replace('€', ''))(),
            currency='EUR',
            image=catcher(lambda: product.find('img', {'class': 'primary_image'}).get('src'))(),
            url=catcher(lambda: product.find('a').get('href'))(),
        )


def iter_pages():
    url = f'https://shopb2b.ghiblisrl.com/en/shop/'
    while True:
        soup = fetch_html(url)
        for product in iter_products(soup):
            yield product
        url = get_next_url(soup)
        if url is None:
            return


def get_detailed_product(product):
    soup = fetch_html(product.url)

    def get_images():

        def get_size(size_str):
            return int(size_str.replace('w', ''))

        def get_larger_img():
            size, url = max(img_dict.items(), key=lambda item: get_size(item[0]))
            return url

        images = []
        for node in soup.find_all('a', {'class': 'yith_magnifier_thumbnail'}):
            img_dict = dict()
            for img in node.find('img').get('srcset').split(','):
                v, k = img.split()
                img_dict[k] = v
            larger_img = get_larger_img()
            images.append(larger_img)
        return images

    return DetailedProduct(
        title=product.title,
        price=product.price,
        currency='EUR',
        url=product.url,
        short_description=catcher(lambda: soup.find('div', {'class': 'short-description'}).get_text(strip=True))(),
        sku=catcher(lambda: soup.find('span', {'class': 'sku'}).get_text())(),
        categories=catcher(
            lambda: list([node.get_text() for node in soup.find('span', {'class': 'posted_in'}).find_all('a')]))(),
        images=catcher(get_images)(),
        weight=catcher(lambda: soup.find('td', {'class': 'product_weight'}).get_text())(),
        dimensions=catcher(lambda: soup.find('td', {'class': 'product_dimensions'}).get_text())()
    )


def iter_detailed_products(products):
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        future_to_product = {executor.submit(get_detailed_product, product): product for product in products}
        for future in concurrent.futures.as_completed(future_to_product):
            product = future_to_product[future]
            try:
                yield future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (product.url, exc))


def write_df_to_s3(df, key):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    client = boto3.client('s3')
    client.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())


def iter_images_from_df(df):
    for t in df.itertuples():
        for img_url in t.images:
            img_name = os.path.basename(img_url)
            path = f'{bucket}/manufacturers/pictures/{t.unique_id}_{img_name}'
            yield img_url, path


def download_image_to_s3(url, path):
    print(f'Fetching {url}')
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with fs.open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def download_images(images):
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        future_to_url = {executor.submit(download_image_to_s3, *image): image for image in images}
        for future in concurrent.futures.as_completed(future_to_url):
            image_url, path = future_to_url[future]
            try:
                future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (image_url, exc))


def main():
    products = list(iter_pages())
    detailed = list(iter_detailed_products(products))
    products_df = (
        pd.merge(
            pd.DataFrame([asdict(p) for p in products]),
            pd.DataFrame([asdict(p) for p in detailed]),
            on=['title', 'price', 'currency', 'url']
        )
        .assign(
            unique_id=lambda df: df['url'].apply(lambda x: hashlib.md5(x.encode('utf-8')).hexdigest()),
        )
    )
    write_df_to_s3(products_df, 'manufacturers/data/ghibli.csv')
    images = list(iter_images_from_df(products_df[['unique_id', 'images']]))
    download_images(images)


if __name__ == '__main__':
    main()
