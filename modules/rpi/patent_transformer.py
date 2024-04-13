import xml.etree.ElementTree as ET
import pandas as pd
import glob
import os
import uuid
from uuid import uuid4


def extract_data(despacho: any, numero_rpi: int) -> list:
    data = []

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
        data.append([numero_rpi, despacho_id, codigo_despacho, titulo, numero_processo, data_deposito, comentario, None, None, None, None])
    else:
        data.append([numero_rpi, despacho_id, codigo_despacho, titulo, numero_processo, data_deposito, None, None, None, None, None])

    for titular in titulares:
        sequencia_titular = titular.attrib['sequencia']
        nome_completo = titular.find('nome-completo').text
        endereco = titular.find('endereco')
        uf = endereco.find('uf').text if endereco is not None and endereco.find('uf') is not None else None
        pais = endereco.find('pais/sigla').text if endereco is not None and endereco.find('pais/sigla') is not None else None

        data.append([numero_rpi, despacho_id, codigo_despacho, titulo, numero_processo, data_deposito, None, sequencia_titular, nome_completo, uf, pais])

    return data

xml_files = glob.glob("*.xml")

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

if __name__ == '__main__':
    extract_data(despacho,numero_rpi)
    print(f'--------------')
