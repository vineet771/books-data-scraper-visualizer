# Auto-install required libraries
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try importing and install if missing
try:
    import requests
except ImportError:
    install("requests")
    import requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    install("beautifulsoup4")
    from bs4 import BeautifulSoup

# URL of the website to scrape
url = "http://books.toscrape.com/"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Parse the page content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all book containers
books = soup.find_all('article', class_='product_pod')

# List to store scraped data
book_data = []

# Loop through each book container to extract details
for book in books:
    # Extract book title
    title = book.h3.a['title']
    
    # Extract book price
    price = book.find('p', class_='price_color').text
    
    # Add details to the list
    book_data.append({'title': title, 'price': price})

# Display the scraped data
for i, book in enumerate(book_data, start=1):
    print(f"{i}. {book['title']} - {book['price']}")

# Save the data to a CSV file
import csv

with open('books.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['title', 'price'])
    writer.writeheader()
    writer.writerows(book_data)

print("Data saved to books.csv")
