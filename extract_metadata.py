import xml.etree.ElementTree as ET
import pandas as pd
from uuid import uuid4


def extract_metadata_from_file(numero_rpi) -> None:
    metadata = []

    tree = ET.parse(f'P{numero_rpi}.xml')
    root = tree.getroot()

    # print(f'Metadata list populated for {numero_rpi}.')
    for despacho in root.findall('despacho'):
        # Extract metadata from despacho
        # metadata.append(despacho)

        numero_rpi
        despacho_id = str(uuid4())
        codigo_despacho = despacho.find('codigo').text
        titulo = despacho.find('titulo').text
        processo = despacho.find('processo-patente')
        numero_processo = processo.find('numero').text if processo is not None and processo.find('numero') is not None else None
        
        metadata.extend([numero_rpi, despacho_id, codigo_despacho, titulo, numero_processo])

    return metadata

def write_metadata(metadata) -> None:
    if metadata:
        with open(f'TEST-C{numero_rpi}.txt', 'w') as fp:
            for despacho in metadata:
                # Write each item on a new line
                fp.write("%s\n" % despacho)
                print(f'Metadata for {numero_rpi} list written in file.')
    else:
        print(f'Error: No Metadata list for {numero_rpi}.')

def build_dataframe(metadata) -> None:

    if metadata:
        df = pd.DataFrame(metadata, columns=['numero_rpi', 'despacho_id', 'codigo_despacho', 'titulo', 'numero_processo'])
        query = df['despacho_id'].nunique()
        print(f'BuildDataFrame: Total de {query} despachos na RPI {numero_rpi}!')
        csv_file = df.to_csv(f'P{numero_rpi}.csv')
    else:
        print(f'Error: No Metadata list for {numero_rpi}.')    
    
    return csv_file




if __name__ == '__main__':
    
    numero_rpi_start = int(input('PatentTransformer: Escreva o número de RPI inicial: '))
    numero_rpi_end = int(input('PatentTransformer: Escreva o número de RPI final: '))
    
    for numero_rpi in range(numero_rpi_start, numero_rpi_end+1):
        metadata = extract_metadata_from_file(numero_rpi)
        print(metadata)
        build_dataframe(metadata)