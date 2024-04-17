import requests
import zipfile
import os
import glob
import xml.etree.ElementTree as ET
import pandas as pd
import asyncio

from modules.rpi.patent_extractor import check_xml_exists, get_rpi_patentes, unzip, rename_xml
from modules.rpi.patent_transformer import check_csv_exists, parse_element

url_template = 'https://revistas.inpi.gov.br/txt/P{}.zip'


if __name__ == '__main__':
    # Prompt for RPI number
    numero_rpi_start = int(input(f'PatentApp: Escreva o número de RPI inicial: '))
    numero_rpi_end = int(input(f'PatentApp: Escreva o número de RPI final: '))

    missing_rpi_xml = check_xml_exists(numero_rpi_start, numero_rpi_end)

    missing_rpi_csv = check_csv_exists(numero_rpi_start, numero_rpi_end)

    if missing_rpi_xml is None:
        missing_rpi_xml
    else:
        get_rpi_patentes(url_template, missing_rpi_xml)
        unzip(missing_rpi_xml)
        rename_xml(missing_rpi_xml)

    if missing_rpi_csv is None:
        missing_rpi_csv
    else:
        for numero_rpi in missing_rpi_csv:
        print(f'PatentTransformer: Processando {numero_rpi}.xml...')
        tree = ET.parse(f'P{numero_rpi}.xml')
        root = tree.getroot()
        data = []
        for child in root:
            item = {}
            parse_element(child, item)
            data.append(item)
            df = pd.DataFrame(data)
            df.to_csv(f'P{numero_rpi}.csv')
        print(f'PatentTransformer: Planilha {numero_rpi}.csv criada!')

    
    


