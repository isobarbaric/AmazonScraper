from selenium import webdriver
from bs4 import BeautifulSoup

AMAZON_SEARCH_URL = 'https://www.amazon.ca/s?k='

def get_amazon_search_page(search_query: str):
    url = AMAZON_SEARCH_URL + '+'.join(search_query.split())

    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(3)

    html_page = driver.page_source
    driver.quit()

    return html_page

def get_closest_product_asin(html_page: str):
    soup = BeautifulSoup(html_page, 'lxml')

    # data-asin grabs products, while data-avar filters out sponsored ads
    listings = soup.findAll('div', attrs={'data-asin': True, 'data-avar': False})

    asin_values = [single_listing['data-asin'] for single_listing in listings if len(single_listing['data-asin']) != 0]

    return asin_values[0]

if __name__ == "__main__":
    search_query = 'iphone 15'
    
    html_page = get_amazon_search_page(search_query)
    product_asin = get_closest_product_asin(html_page)

    print(product_asin)