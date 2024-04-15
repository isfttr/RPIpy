import requests
import zipfile
import os
import glob
import xml.etree.ElementTree as ET
import pandas as pd
import asyncio

from modules.rpi.patent_extractor import get_rpi_patentes, rename_xml
from modules.rpi.patent_transformer import extract_data



# numero_rpi = input('Escreva o número de RPI desejado: ')
url_template = 'https://revistas.inpi.gov.br/txt/P{}.zip'

directory = os.getcwd()

xml_files = glob.glob('*.xml')


for i, xml_file in enumerate(xml_files):
    filename = os.path.splitext(os.path.basename(xml_file))[0]
    numero_rpi_str = ''.join(filter(str.isdigit, filename))
    
    if numero_rpi_str: 
        numero_rpi = int(numero_rpi_str)
        print(f"Processando {xml_file}... para RPI {numero_rpi} Patentes!")
        tree = ET.parse(xml_file)
        root = tree.getroot()

        data = []
        
        for despacho in root.findall('despacho'):
            data.extend(extract_data(despacho, numero_rpi))

            df = pd.DataFrame(data, columns=['numero_rpi', 'despacho_id', 'codigo_despacho', 'titulo', 'numero_processo', 'data_deposito', 'comentario', 'sequencia_titular', 'nome_completo', 'uf', 'pais'])
            
            
            query = df['despacho_id'].nunique()
            print(f'Processamento finalizado...')
            print(f'Total de {query} despachos na RPI {numero_rpi} Patentes!')
            print(f'--------------')
            df.to_csv(f'P{numero_rpi}.csv')

# extract_data(despacho, numero_rpi)    



async def prepare_files() -> None:
    get_rpi_patentes(url_template, numero_rpi_start, numero_rpi_end)
    rename_xml(directory)
    
    print(f'Arquivos prontos para extração...')


async def main() -> None:
    await prepare_files()
    process_xml()

if __name__ == '__main__':
    # Prompt for RPI number
    numero_rpi_start = int(input(f'Escreva o número de RPI inicial: '))
    numero_rpi_end = int(input(f'Escreva o número de RPI final: '))

    asyncio.run(main())
