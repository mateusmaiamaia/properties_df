import json
import re  # Importando o módulo de expressões regulares

def escape_string(value):
    if value is None:
        return 'NULL'
    return value.replace("'", "''")

input_file = 'adverts.json'
output_file = 'populate.sql'

unified_cities = {
    'BRASÍLIA': 'Brasília',
    'ÁGUAS CLARAS': 'Águas Claras',
    'ÁGUAS LINDAS DE GOIÁS': 'Águas Lindas De Goiás',
    'ALPHAVILLE': 'Alphaville',
    'BRAZLÂNDIA': 'Brazlândia',
    'CANDANGOLÂNDIA': 'Candangolândia',
    'CEILÂNDIA': 'Ceilândia',
    'CIDADE OCIDENTAL': 'Cidade Ocidental',
    'CRUZEIRO': 'Cruzeiro',
    'FORMOSA': 'Formosa',
    'GAMA': 'Gama',
    'GUARÁ': 'Guará',
    'JARDIM BOTÂNICO': 'Jardim Botânico',
    'LUZIÂNIA': 'Luziânia',
    'NÚCLEO BANDEIRANTE': 'Núcleo Bandeirante',
    'PARANOÁ': 'Paranoá',
    'PLANALTINA': 'Planaltina',
    'PLANALTINA DE GOIÁS': 'Planaltina De Goiás',
    'RECANTO DAS EMAS': 'Recanto Das Emas',
    'RIACHO FUNDO': 'Riacho Fundo',
    'SAMAMBAIA': 'Samambaia',
    'SANTA MARIA': 'Santa Maria',
    'SANTO ANTÔNIO DO DESCOBERTO': 'Santo Antônio Do Descoberto',
    'SÃO SEBASTIÃO': 'São Sebastião',
    'SETOR INDUSTRIAL': 'Setor Industrial',
    'SOBRADINHO': 'Sobradinho',
    'TAGUATINGA': 'Taguatinga',
    'VALPARAÍSO DE GOIÁS': 'Valparaíso De Goiás',
    'VARJÃO': 'Varjão',
    'VICENTE PIRES': 'Vicente Pires',
    'VILA ESTRUTURAL': 'Vila Estrutural',
}

def unify_city_name(city):
    # Extrai a parte antes do "-" e remove espaços em branco ao redor
    match = re.match(r'^\s*([^-]*)', city)  # Captura tudo antes do "-"
    if match:
        city_part = match.group(1).strip()  # Remove espaços em branco antes e depois
        # Verifica se a parte da cidade está nas cidades unificadas
        if city_part in unified_cities:
            return unified_cities[city_part]
    return None  # Retorna None se não houver correspondência

def write_utf8_encoded(file, params):
    title = escape_string(params.get('title', 'NULL'))
    price = escape_string(params.get('price', 'NULL'))
    sqm_price = escape_string(params.get('sqm_price', 'NULL'))
    area = escape_string(params.get('area', 'NULL'))
    city = escape_string(params.get('city', 'NULL'))
    link = escape_string(params.get('link', 'NULL'))

    # Unifica o nome da cidade
    city_name = unify_city_name(city)
    
    # Verifica o preço por metro quadrado
    if sqm_price and sqm_price.isdigit():
        sqm_price_int = int(sqm_price.replace('.', ''))  # Convertendo o preço por m² em inteiro
        if sqm_price_int > 70000:
            print(f"Valor por metro quadrado muito alto para {title} na cidade {city_name}: R$ {sqm_price}. Ignorado.")
            return  # Ignora este imóvel

    if city_name:  # Se o nome da cidade foi unificado com sucesso
        # Cria o comando SQL
        sql_command = f"INSERT INTO properties (title, price, sqm_price, area, city, link) VALUES ('{title}', '{price}', '{sqm_price}', '{area}', '{city_name}', '{link}');\n"
        file.write(sql_command)
    else:
        print(f"Cidade não permitida: {city}")  # Para depuração

with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
    data = json.load(f_in)
    for item in data:
        write_utf8_encoded(f_out, item)  # Escreve o comando SQL no arquivo

print(f'SQL script gerado em {output_file}')
