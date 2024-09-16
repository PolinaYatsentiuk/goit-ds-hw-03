import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Підключення до MongoDB
client = MongoClient(
    "mongodb+srv://pyatsentyuk:tiger66one@cluster0.epc74.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)

db = client.test

quotes_collection = db.quotes
authors_collection = db.authors


# Функція для скрапінгу сторінок сайту
def scrape_quotes():
    base_url = "http://quotes.toscrape.com"
    page_url = "/page/1"
    quotes = []
    authors = []
    visited_authors = set()

    while page_url:
        response = requests.get(base_url + page_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Скрапінг цитат
        quote_divs = soup.find_all('div', class_='quote')
        for quote_div in quote_divs:
            text = quote_div.find('span', class_='text').get_text()
            author_name = quote_div.find('small', class_='author').get_text()
            tags = [tag.get_text() for tag in quote_div.find_all('a', class_='tag')]

            quotes.append({
                "quote": text,
                "author": author_name,
                "tags": tags
            })

            # Скрапінг авторів, якщо ще не скраплені
            if author_name not in visited_authors:
                visited_authors.add(author_name)
                author_url = base_url + quote_div.find('a')['href']
                author_response = requests.get(author_url)
                author_soup = BeautifulSoup(author_response.text, 'html.parser')

                born_date = author_soup.find('span', class_='author-born-date').get_text()
                born_location = author_soup.find('span', class_='author-born-location').get_text()
                description = author_soup.find('div', class_='author-description').get_text().strip()

                authors.append({
                    "fullname": author_name,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description
                })

        # Знаходження наступної сторінки
        next_button = soup.find('li', class_='next')
        page_url = next_button.find('a')['href'] if next_button else None

    return quotes, authors


# Запуск скрапінгу
quotes, authors = scrape_quotes()

# Збереження даних в JSON-файли
with open('quotes.json', 'w', encoding='utf-8') as q_file:
    json.dump(quotes, q_file, ensure_ascii=False, indent=4)

with open('authors.json', 'w', encoding='utf-8') as a_file:
    json.dump(authors, a_file, ensure_ascii=False, indent=4)

# Імпорт в MongoDB
quotes_collection.insert_many(quotes)
authors_collection.insert_many(authors)

print("Скрапінг завершено та дані збережено в MongoDB.")
