# AmazonScraper

Retrieve data on the closest item on Amazon corresponding to a given search term

## Installation

1. Get [Python Poetry](https://python-poetry.org/)
2. `cd` into the root of this repository
3. Run `poetry install`

## Usage
```python
search_query = 'ipad air'
scraper = AmazonScraper()

reviews = scraper.get_closest_product_reviews(search_query, num_reviews = 5)

print(reviews)
# [{'customer_name': 'Kenova Pelletier', 'rating': 1, 'review': 'This looked amazing out of the box...
```

### Debug Flag
The `get_closest_product_reviews` method also has a `debug` flag available that outputs the total time taken for execution.

```python
search_query = 'ipad air'
scraper = AmazonScraper()

reviews = scraper.get_closest_product_reviews(search_query, num_reviews = 5, debug=True)
# 13.47 seconds taken
```

## Disclaimer
This project is intended for personal and educational purposes only. Any use of this project for commercial or production purposes is not recommended. The author does not take responsibility for any misuse or consequences arising from the use of this project outside of its intended scope.