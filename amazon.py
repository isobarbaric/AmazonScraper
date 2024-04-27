from autoscraper import AutoScraper

# scraper = AutoScraper()
amazon_scraper = AutoScraper()
amazon_scraper.load('amazon-search.config')
    # scraper.set_rule_aliases({})

AMAZON_URL = 'https://www.amazon.ca/s?k='

def amazon_search(search_query, search_query_lst):
    url = AMAZON_URL + search_query
    # result = amazon_scraper.build(url, search_query_lst)
    result = amazon_scraper.get_result_similar(url, grouped=True, group_by_alias=True)
    # result = amazon_scraper.get_result_similar(url, group_by_alias=True)
    return result

iphone = ['iPhone 15']

ans = amazon_search("iPhone 15", iphone)
print(ans)
