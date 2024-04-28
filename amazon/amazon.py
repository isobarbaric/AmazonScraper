from selenium import webdriver
from bs4 import BeautifulSoup

AMAZON_SEARCH_URL = 'https://www.amazon.ca/s?k='
AMAZON_REVIEW_URL = 'https://www.amazon.ca/product-reviews/'

# all start at page 1
star_page_suffix = {
    5: '/ref=cm_cr_unknown?filterByStar=five_star&pageNumber=',
    4: '/ref=cm_cr_unknown?filterByStar=four_star&pageNumber=',
    3: '/ref=cm_cr_unknown?filterByStar=three_star&pageNumber=',
    2: '/ref=cm_cr_unknown?filterByStar=two_star&pageNumber=',
    1: '/ref=cm_cr_unknown?filterByStar=one_star&pageNumber=',
}

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

def __get_rated_reviews(url: str, num_reviews: int):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(3)

    html_page = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_page, 'lxml')
    reviews = soup.findAll('span', attrs={'data-hook': True})

    reviews = [review for review in reviews if review['data-hook'] == 'review-body']

    # extract text from span tag and clean up newlines in string
    reviews = [review.text.strip() for review in reviews]    

    return reviews

def get_reviews(asin: str, num_reviews: int):
    base_url = AMAZON_REVIEW_URL + asin

    for star_num in [1, 5]:
        url = base_url + star_page_suffix[star_num]
        print(url)


if __name__ == "__main__":
    search_query = 'iphone 15'
    
    html_page = get_amazon_search_page(search_query)
    product_asin = get_closest_product_asin(html_page)
    print(product_asin)

    get_reviews(asin)
