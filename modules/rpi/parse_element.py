import xml.etree.ElementTree as ET
import pandas as pd


def parse_element(element, item):
    if len(list(element)) == 0:
        item[element.tag] = element.text
    else:
        for child in list(element):
            parse_element(child, item)


if __name__ == '__main__':    
    
    numero_rpi_start = int(input('ParseElement: Escreva o número de RPI inicial: '))
    numero_rpi_end = int(input('ParseElement: Escreva o número de RPI final: '))
    
    for numero_rpi in range(numero_rpi_start, numero_rpi_end+1):
        print(f'Iniciando para {numero_rpi}...')
        tree = ET.parse(f'P{numero_rpi}.xml')
        root = tree.getroot()
        data = []
        for child in root:
            item = {}
            parse_element(child, item)
            data.append(item)
            df = pd.DataFrame(data)
            df.to_csv(f'P{numero_rpi}.csv')
        print(f'Finalizado {numero_rpi}...')
