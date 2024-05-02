from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

wait_time = 0.3

def search_amazon(search_query: str, headless: bool = True) -> str:
    # setting up a headless web driver to get search query
    start = time.time()
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    url = 'https://www.amazon.com/s?k=' + '+'.join(search_query.split())
    end = time.time()
    print(f'URL construction time: {end - start} seconds')

    start = time.time()
    driver.get(url)
    # driver.implicitly_wait(wait_time)

    html_page = driver.page_source
    driver.quit()
    end = time.time()
    print(f'Page retrieval time: {end - start} seconds')

    return html_page

def extract_products(html_page: str):
    soup = BeautifulSoup(html_page, 'lxml')

    # data-asin grabs products, while data-avar filters out sponsored ads
    listings = soup.findAll('div', attrs={'data-asin': True, 'data-avar': False})

    # filter for all data-asin values to have length 10
    listings = [listing for listing in listings if len(listing['data-asin']) == 10]

    # extract additional information
    products = []
    for listing in listings:
        product = {}

        # extract title
        title_tag = listing.find('span', class_='a-size-base-plus a-color-base a-text-normal')
        product['title'] = title_tag.get_text(strip=True) if title_tag else "No Title Found"

        # extract image URL
        image_tag = listing.find('img', class_='s-image')
        product['image'] = image_tag['src'] if image_tag else "No Image Found"

        # extract product URL, prefixing with the base Amazon URL if not absolute
        product['url'] = f"https://www.amazon.com/dp/{listing['data-asin']}" if listing['data-asin'] else "No URL Found"

        # add ASIN in
        product['asin'] = listing['data-asin']

        # find star rating
        star_rating = soup.find('span', class_='a-icon-alt').text.split()[0]
        product['star_rating'] = star_rating if star_rating else "No Star Rating Found"

        # num_bought = soup.find('span', class_='a-size-base', text=lambda x: 'bought in past month' in x)
        # print(num_bought)

        products.append(product)

    return products

def parse_info(products: list):
    pass

if __name__ == "__main__":
    start = time.time()

    html_page = search_amazon('python programming books')
    print('obtained html page, now parsing...')
    products = extract_products(html_page)

    end = time.time()
    print(json.dumps(products[0], indent=4))
    print(f'Execution time: {end - start} seconds')