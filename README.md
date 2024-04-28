# AmazonScraper

Obtains information about the closest item available on Amazon relative to a provided 

## Installation

1. Get [Python Poetry](https://python-poetry.org/)
2. `cd` into the root of this repository
3. Run `poetry install`

## Usage
```python
search_query = 'ipad air'
scraper = AmazonScraper()

reviews = scraper.get_closest_product_reviews(search_query, num_reviews = 5, debug=True)

print(reviews)
# [{'customer_name': 'Kenova Pelletier', 'rating': 1, 'review': 'This looked amazing out of the box...
```

## Disclaimer
This project is intended for personal and educational purposes only. Any use of this project for commercial or production purposes is not recommended. The author does not take responsibility for any misuse or consequences arising from the use of this project outside of its intended scope.