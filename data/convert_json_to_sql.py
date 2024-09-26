# -*- coding: utf-8 -*-

import json

def escape_string(value):
    # Escapa aspas simples e trata valores None
    if value is None:
        return 'NULL'
    return value.replace("'", "''")

input_file = 'adverts.json'
output_file = 'populate.sql'

def write_utf8_encoded(file, params):
    # Escapa cada valor adequadamente
    title = escape_string(params.get('title', 'NULL'))
    price = escape_string(params.get('price', 'NULL'))
    sqm_price = escape_string(params.get('sqm_price', 'NULL'))
    area = escape_string(params.get('area', 'NULL'))
    city = escape_string(params.get('city', 'NULL'))
    link = escape_string(params.get('link', 'NULL'))

    # Cria o comando SQL
    sql_command = f"INSERT INTO properties (title, price, sqm_price, area, city, link) VALUES ('{title}', '{price}', '{sqm_price}', '{area}', '{city}', '{link}');\n"
    file.write(sql_command)

with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
    data = json.load(f_in)
    for item in data:
        write_utf8_encoded(f_out, item)  # Escreve o comando SQL no arquivo

print(f'SQL script gerado em {output_file}')
