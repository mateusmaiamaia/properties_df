# -*- coding: utf-8 -*-

import json

def escape_string(value):
    return value.replace("'", "''")

input_file = 'adverts.json'
output_file = 'populate.sql'

sql_template = u"INSERT INTO properties (title, price, sqm_price, area) VALUES ('{title}', '{price}', '{sqm_price}', '{area}');\n"

def write_utf8_encoded(file, text):
    file.write(text.encode('utf-8'))

with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
    data = json.load(f_in)
    for item in data:
        sql_command = sql_template.format(
            title=escape_string(item['title']),
            price=escape_string(item['price']),
            sqm_price=escape_string(item['sqm_price']),
            area=escape_string(item['area']),
            city=escape_string(item['city']),
            link=escape_string(item['link'])
        )
        write_utf8_encoded(f_out, sql_command)

print (u'SQL script gerado em {}'.format(output_file))
