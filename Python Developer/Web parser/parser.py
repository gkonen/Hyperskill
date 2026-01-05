import os
import string

import requests
from bs4 import BeautifulSoup, PageElement

BASE_URL = "www.nature.com"

class PageError(Exception):
    pass
class ResourceError(Exception):
    pass

def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def save_page(data, folder, filename):
    with open(f"{folder}/{filename}", 'wb') as f:
        f.write(data.encode('utf-8'))
    print("Content saved")

def find_article_type(article : PageElement):
    span = article.find('span', {'data-test': 'article.type'})
    return span.text

def find_link_article(article : PageElement):
    a = article.find('a', {'data-track-action': 'view article'})
    return f"https://{BASE_URL}"+a['href'], a.text

def save_body_article(link, folder, title):
    headers = {'Accept-Language': 'en-US,en;q=0.5'}
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    teaser = soup.find('p', {'class': 'article__teaser'})
    title = title.translate(str.maketrans('', '', string.punctuation))
    title = title.replace(' ', '_')
    save_page(teaser.text, folder,f"{title}.txt")


def scrape(URL, nb_page, searched_type):
    headers = {'Accept-Language': 'en-US,en;q=0.5'}
    for page in range(1, nb_page+1):
        page_url = f"{URL}&page={page}"
        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        if response.status_code == 200:
            print("Page", page, "open")
            articles = soup.find_all('article')
            create_folder(f"Page_{page}")
            for article in articles:
                article_type = find_article_type(article)
                print("Article Type",article_type, "found")
                if article_type == searched_type:
                    link, title = find_link_article(article)
                    print("Found article", title, "at", link)
                    save_body_article(link, f"Page_{page}", title)
                    print("Saved article")
        else:
            raise ResourceError
        print("="*100)

if __name__ == "__main__":
    nb_page = int(input())
    searched_type = input()
    url = f"https://www.nature.com/nature/articles?sort=PubDate&year=2020"
    try:
        hostname = url.split("//")[1].split("/")[0]
        if hostname != BASE_URL:
            raise PageError
        scrape(url, nb_page, searched_type)

    except PageError:
        print("Invalid page!")
    except ResourceError:
        print("Resource not found!")
