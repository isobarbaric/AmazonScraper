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

def __get_rated_reviews(url: str):
    driver = webdriver.Chrome()

    # make browser headless so it works in the background
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    driver.get(url)
    driver.implicitly_wait(3)

    html_page = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_page, 'lxml')
    html_reviews = soup.findAll('div', attrs={"data-hook": "review"})

    reviews = []
    for html_review in html_reviews:
        # extract text from various span tags and clean up newlines in their strings
        name = html_review.find('span', class_='a-profile-name').text.strip()    

        # Amazon's format is "x.0 stars out of 5" where x = # of stars
        rating = html_review.find('span', class_='a-icon-alt').text.strip()[0]

        review_body = html_review.find('span', attrs={'data-hook': 'review-body'}).text.strip()

        reviews.append({'customer_name': name, 'rating': int(rating),'review': review_body})

    return reviews

def get_reviews(asin: str, num_reviews: int):
    assert num_reviews % 5 == 0

    base_url = AMAZON_REVIEW_URL + asin
    overall_reviews = []

    for star_num in range(1, 6):
        url = base_url + star_page_suffix[star_num]

        page_number = 1
        reviews = []
        reviews_per_star = int(num_reviews / 5)

        while len(reviews) <= reviews_per_star:
            page_url = url + str(page_number)
            print(page_url)

            # no reviews means we've exhausted all reviews
            page_reviews = __get_rated_reviews(page_url)

            if len(page_reviews) == 0:
                break

            reviews += page_reviews
            page_number += 1

        # shave off extra reviews coming from the last page
        reviews = reviews[:reviews_per_star]
        overall_reviews += reviews

    return overall_reviews

if __name__ == "__main__":
    search_query = 'iphone 15'
    
    html_page = get_amazon_search_page(search_query)
    product_asin = get_closest_product_asin(html_page)
    # print(product_asin)

    reviews = get_reviews(asin = product_asin, num_reviews = 10)
    print(reviews)