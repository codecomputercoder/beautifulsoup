import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_product_details(url):
    """
    This function takes a product URL as input and returns a dictionary containing product details.
    """
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

    page = requests.get(url, headers=headers)
    # print(page.status_code)
    soup = BeautifulSoup(page.content, "html.parser")
    
    title = soup.find("span", {"id":"productTitle"})
    if title:
        title = title.get_text(strip=True)
    else:
        title = "default_title"

    # print(title)

    product_price = soup.find('span', {'class': 'a-price-whole'})
    product_price=product_price.get_text(strip=True)
    # print(product_price)
    product_rating = soup.find('span', attrs={'class': 'a-icon-alt'}).text.strip().split()[0]
    product_num_reviews = soup.find('span', attrs={'id':'acrCustomerReviewText'}).text.strip().split()[0]
    return {'URL':url, 'Name': title, 'Price': product_price, 'Rating': product_rating, 'NumReviews': product_num_reviews}

product_list = []
for page_num in range(1, 21):
    url = f"https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page_num}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
   # print(soup.prettify())
    product_links = soup.find_all('a', {'class': 'a-link-normal s-no-outline'})
    for link in product_links:
        product_url = "https://www.amazon.in" + link.get('href')
        #print (product_url)
        product_list.append(get_product_details(product_url))

df = pd.DataFrame(product_list)
df.to_csv('part1_products.csv', index=False)
