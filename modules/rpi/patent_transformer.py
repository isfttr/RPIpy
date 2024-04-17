import xml.etree.ElementTree as ET
import pandas as pd
import os
from uuid import uuid4
# import sys
# sys.path.append('utils/')
# from utils.cleaner import swipe_csv

def check_xml_exists(missing_rpi_csv: list) -> list:
    missing_rpi = []

    for numero_rpi in missing_rpi_csv:  
        xml_file_name = 'P{}.xml'.format(numero_rpi)

        if not os.path.exists(xml_file_name):
            print(f'CheckXML: {xml_file_name} não existe...')
            missing_rpi.append(numero_rpi)

    if missing_rpi:
        print(f'CheckXML: Não foram encontrados os arquivos referentes as RPIs: {", ".join(map(str, missing_rpi))}...')
    else:
        print(f'CheckXML: Todos arquivos encontrados!')
    
    return missing_rpi or None


def check_csv_exists(numero_rpi_start: int, numero_rpi_end: int) -> list:
    missing_rpi_csv = []

    for numero_rpi in range(numero_rpi_start, numero_rpi_end+1):  
        xml_file_name = 'P{}.csv'.format(numero_rpi)

        if not os.path.exists(xml_file_name):
            print(f'CheckCSV: {xml_file_name} não existe...')
            missing_rpi_csv.append(numero_rpi)

    if missing_rpi_csv:
        print(f'CheckCSV: Não foram encontrados os arquivos referentes as RPIs: {", ".join(map(str, missing_rpi_csv))}...')
    else:
        print(f'CheckCSV: Todos arquivos encontrados!')
    
    return missing_rpi_csv or None


def parse_element(element, item):
    if len(list(element)) == 0:
        item[element.tag] = element.text
    else:
        for child in list(element):
            parse_element(child, item)


if __name__ == '__main__':
    
    numero_rpi_start = int(input('PatentTransformer: Escreva o número de RPI inicial: '))
    numero_rpi_end = int(input('PatentTransformer: Escreva o número de RPI final: '))
    missing_rpi_csv = check_csv_exists(numero_rpi_start, numero_rpi_end)
    missing_rpi = check_xml_exists(missing_rpi_csv)

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

        
