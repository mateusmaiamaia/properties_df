import requests
import json
from bs4 import BeautifulSoup
import time

# Cabeçalhos para imitar um navegador real
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://www.google.com/'
}

# Função para criar uma sopa (parser) da URL
def make_soup(url, session):
    response = session.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

# Função para extrair links da página
def extract_links_from_page(url, session):
    response = session.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a', class_='new-card')
    
    page_links = []
    for link in links:
        href = link.get('href')
        full_url = f'https://www.dfimoveis.com.br{href}'  # URL completa do link
        page_links.append(full_url)

    return page_links

# Função para raspar todas as páginas
def scrape_all_pages(base_url, last_page):
    session = requests.Session()
    all_links = []

    for page in range(1, last_page + 1):
        url = f'{base_url}?pagina={page}'
        print(f'Raspando página {page}... {url}')

        try:
            links = extract_links_from_page(url, session)
            print(f'Encontrados {len(links)} links na página {page}')
            all_links.extend(links)
        except Exception as e:
            print(f'Erro ao raspar página {page}: {e}')
            continue

    return all_links

# Função para obter o título
def get_title(link, session):
    soup = make_soup(link, session)
    title = soup.find('div', {'class': 'col-9'})
    if title:
        return title.text.strip()
    return "Título não encontrado"

# Função para obter o preço
def get_price(link, session):
    soup = make_soup(link, session)
    div = soup.find('div', {'class': 'col-6 pr-0'})
    if div:
        price = div.find('small', {'class': 'display-5 text-warning'})
        if price:
            return price.text.strip()
    return "Preço não encontrado"

# Função para obter o preço por m²
def get_sqm_price(link, session):
    soup = make_soup(link, session)
    sqm_price = soup.find('small', {'class': 'display-5 text-warning m2-valor-salao'})
    if sqm_price:
        return sqm_price.text.strip()
    return "Preço por m² não encontrado"

# Função para obter a área
def get_area(link, session):
    soup = make_soup(link, session)
    area = soup.find('small', {'class': 'display-5 text-warning'})
    if area:
        return area.text.strip()
    return "Área não encontrada"

if __name__ == '__main__':
    BASE_URL = 'https://www.dfimoveis.com.br/venda/df/todos/imoveis'
    LAST_PAGE = 1407  # Ajuste o número de páginas conforme necessário

    adverts = []
    session = requests.Session()

    all_links = scrape_all_pages(BASE_URL, LAST_PAGE)

    for idx, link in enumerate(all_links):
        print(f"\nProcessando link {idx + 1}/{len(all_links)}: {link}")
        
        try:
            advert_title = get_title(link, session)
            print(f"Título extraído: {advert_title}")

            advert_price = get_price(link, session)
            print(f"Preço extraído: {advert_price}")

            advert_sqm_price = get_sqm_price(link, session)
            print(f"Preço por m² extraído: {advert_sqm_price}")

            advert_area = get_area(link, session)
            print(f"Área extraída: {advert_area}")

            advert = {
                'title': advert_title,
                'price': advert_price,
                'sqm_price': advert_sqm_price,
                'area': advert_area
            }

            adverts.append(advert)
        except Exception as e:
            print(f"Erro ao processar link {link}: {e}")
            continue

        time.sleep(0.1)  # Adicionando atraso para evitar bloqueio entre requisições

    total_links = len(all_links)
    print(f"Total de links extraídos: {total_links}")

    # Salvar os dados em um arquivo JSON
    with open('adverts.json', 'w') as f:
        json.dump(adverts, f, indent=4)

    print("Dados salvos como JSON em 'adverts.json'.")
