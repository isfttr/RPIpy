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

def find_xml_in_missing_rpi_csv(missing_rpi_csv: list) -> list:
    found_xml_files = []
    
    for numero_rpi in missing_rpi_csv:
        xml_file_name:str = 'P{}.xml'.format(numero_rpi)
        if os.path.exists(xml_file_name):
            print(f'FindXML: {xml_file_name} encontrado...')
            found_xml_files.append(numero_rpi)
    
    if found_xml_files:
        print(f'FindXML: Encontrado arquivos referentes as RPIs: {", ".join(map(str, found_xml_files))}...')
    else:
        check_xml_exists(missing_rpi_csv)
    
    return found_xml_files or None


def extract_metadata_from_despacho(metadata, numero_rpi, despacho) -> None:
    metadata = []

    numero_rpi
    despacho_id = str(uuid4())
    codigo_despacho = despacho.find('codigo').text
    titulo = despacho.find('titulo').text
    processo = despacho.find('processo-patente')
    numero_processo = processo.find('numero').text if processo is not None and processo.find('numero') is not None else None
    data_deposito = processo.find('data-deposito').text if processo is not None and processo.find('data-deposito') is not None else None
    titulares = processo.findall('.//titular') if processo is not None else []
    comentario = despacho.find('comentario').text if despacho.find('comentario') is not None else None

    if comentario is not None:
        metadata.append([numero_rpi, despacho_id, codigo_despacho, titulo, numero_processo, data_deposito, comentario, None, None, None, None])
    else:
        metadata.append([numero_rpi, despacho_id, codigo_despacho, titulo, numero_processo, data_deposito, None, None, None, None, None])

    for titular in titulares:
        sequencia_titular = titular.attrib['sequencia']
        nome_completo = titular.find('nome-completo').text
        endereco = titular.find('endereco')
        uf = endereco.find('uf').text if endereco is not None and endereco.find('uf') is not None else None
        pais = endereco.find('pais/sigla').text if endereco is not None and endereco.find('pais/sigla') is not None else None

        metadata.append([numero_rpi, despacho_id, codigo_despacho, titulo, numero_processo, data_deposito, None, sequencia_titular, nome_completo, uf, pais])
    
    return metadata

def extract_metadata_from_file(numero_rpi) -> None:
    metadata = []

    tree = ET.parse(f'P{numero_rpi}.xml')
    root = tree.getroot()

    for despacho in root.findall('despacho'):
        # Extract metadata from despacho
        file_metadata = extract_metadata_from_despacho(metadata, numero_rpi, despacho)
        metadata.extend(file_metadata)

    return metadata


def build_dataframe(numero_rpi, metadata) -> None:

    df = pd.DataFrame(metadata, columns=['numero_rpi', 'despacho_id', 'codigo_despacho', 'titulo', 'numero_processo', 'data_deposito', 'comentario', 'sequencia_titular', 'nome_completo', 'uf', 'pais'])
    
    query = df['despacho_id'].nunique()
    print(f'BuildDataFrame: Processamento finalizado!')
    print(f'BuildDataFrame: Total de {query} despachos na RPI {numero_rpi}!')
    print(f'--------------')
    
    df.to_csv(f'P{numero_rpi}.csv')


if __name__ == '__main__':
    
    numero_rpi_start = int(input('PatentTransformer: Escreva o número de RPI inicial: '))
    numero_rpi_end = int(input('PatentTransformer: Escreva o número de RPI final: '))
    
    # swipe_csv(numero_rpi_start, numero_rpi_end)

    missing_rpi_csv = check_csv_exists(numero_rpi_start, numero_rpi_end)
    found_xml_files = find_xml_in_missing_rpi_csv(missing_rpi_csv)

    print(f'Lista de processamento: {found_xml_files}.')

    if found_xml_files:
        metadata = []
        for numero_rpi in found_xml_files:
            tree = ET.parse(f'P{numero_rpi}.xml')
            root = tree.getroot()
            metadata = extract_metadata_from_file(numero_rpi)
            for despacho in root.findall('despacho'):
                extract_metadata_from_despacho(metadata, numero_rpi, despacho)
            build_dataframe(metadata, numero_rpi)

    else:
        find_xml_in_missing_rpi_csv
        
