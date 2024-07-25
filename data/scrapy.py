import requests
import json
from bs4 import BeautifulSoup
import time
import logging
import random

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# List of User Agents for rotating user agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
]

def get_random_user_agent():
    return random.choice(user_agents)

def make_soup(url, session):
    response = session.get(url, headers={'User-Agent': get_random_user_agent()})
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def extract_links_from_page(url, session):
    response = session.get(url, headers={'User-Agent': get_random_user_agent()})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a', class_='new-card')
    
    page_links = []
    for link in links:
        href = link.get('href')
        full_url = f'https://www.dfimoveis.com.br{href}'  
        page_links.append(full_url)

    return page_links

def scrape_all_pages(base_url, last_page):
    session = requests.Session()
    all_links = []

    for page in range(1, last_page + 1):
        url = f'{base_url}?pagina={page}'

        try:
            links = extract_links_from_page(url, session)
            all_links.extend(links)
            logger.info(f"Successfully scraped page {page}")
        except requests.HTTPError as e:
            logger.error(f"HTTP error on page {page}: {e}")
        except requests.RequestException as e:
            logger.error(f"Error on page {page}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error on page {page}: {e}")

        time.sleep(0.1)  # To avoid being blocked

    return all_links

def get_title(soup):
    title = soup.find('div', {'class': 'col-9'})
    return title.text.strip() if title else "Título não encontrado"

def get_price(soup):
    div = soup.find('div', {'class': 'col-6 pr-0'})
    if div:
        price = div.find('small', {'class': 'display-5 text-warning'})
        return price.text.strip() if price else "Preço não encontrado"
    return "Preço não encontrado"

def get_sqm_price(soup):
    sqm_price = soup.find('small', {'class': 'display-5 text-warning m2-valor-salao'})
    return sqm_price.text.strip() if sqm_price else "Preço por m² não encontrado"

def get_area(soup):
    area = soup.find('small', {'class': 'display-5 text-warning'})
    return area.text.strip() if area else "Área não encontrada"

def get_city(soup):
    city_div = soup.find('div', style='display: flex; align-items: center; justify-content: space-between;')
    if city_div:
        city = city_div.find('small', {'class': 'text-muted'})
        return city.text.strip() if city else "Cidade não encontrada"
    return "Cidade não encontrada"

if __name__ == '__main__':
    BASE_URL = 'https://www.dfimoveis.com.br/venda/df/todos/imoveis'
    LAST_PAGE = 1407  

    adverts = []
    session = requests.Session()

    all_links = scrape_all_pages(BASE_URL, LAST_PAGE)

    for idx, link in enumerate(all_links):
        try:
            soup = make_soup(link, session)
            advert_title = get_title(soup)
            advert_price = get_price(soup)
            advert_sqm_price = get_sqm_price(soup)
            advert_area = get_area(soup)
            advert_city = get_city(soup)

            advert = {
                'title': advert_title,
                'price': advert_price,
                'sqm_price': advert_sqm_price,
                'area': advert_area,
                'city': advert_city,
                'link': link  # Add the link to the advert dictionary
            }

            adverts.append(advert)
            logger.info(f"Processed advert {idx + 1}/{len(all_links)}")

            # Print the scraped data for verification
            print(f"Advert {idx + 1}:")
            print(json.dumps(advert, indent=4, ensure_ascii=False))

        except requests.HTTPError as e:
            logger.error(f"HTTP error for link {link}: {e}")
        except requests.RequestException as e:
            logger.error(f"Error for link {link}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error for link {link}: {e}")

        time.sleep(0.2)  # To avoid being blocked

    with open('adverts.json', 'w') as f:
        json.dump(adverts, f, indent=4, ensure_ascii=False)

    logger.info("Data saved as JSON in 'adverts.json'.")
