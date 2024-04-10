import requests
import zipfile
import xml.etree.ElementTree as ET
import pandas as pd
import uuid 
from uuid import uuid4


# Prompt for RPI number
numero_rpi_str = input('Escreva o número de RPI desejado: ')
url_template = 'https://revistas.inpi.gov.br/txt/P{}.zip'
file_name = str('P'+numero_rpi_str+'.zip')
numero_rpi = int(numero_rpi_str)


def get_rpi_patentes(url_template: str, numero_rpi_str: str) -> None:

    # Construct new URL using numero_rpi_str 
    url = url_template.format(numero_rpi_str)

    # Send a GET request to the url_template
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the file name from the Content-Disposition header
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            file_name = content_disposition.split('filename=')[1]
        else:
            # If the Content-Disposition header is not present, use the url_template as the file name
            file_name = url.split('/')[-1]

        # Save the file to the current working directory
        with open(file_name, 'wb') as f:
            f.write(response.content)

        print(f'Arquivo {file_name} obtido com sucesso!')
    else:
        print(f'Download não finalizado: {response.status_code}')
    return 

def unziper(file_name: str) -> None:

    # Open the ZIP file in read mode
    with zipfile.ZipFile(file_name, 'r') as zf:
        # Extract all the files to the current working directory
        zf.extractall()


# Parsing do arquivo XML
tree = ET.parse('Patente_'+numero_rpi_str+'_*.xml')

# Função de extração de todos os despachos contidos no XML
def extract_data(despacho: any) -> list:
    data = []

    despacho_id = str(uuid4())
    codigo_despacho = despacho.find('codigo').text
    titulo = despacho.find('titulo').text
    processo = despacho.find('processo-patente')
    numero_processo = processo.find('numero').text if processo is not None and processo.find('numero') is not None else None
    data_deposito = processo.find('data-deposito').text if processo is not None and processo.find('data-deposito') is not None else None
    titulares = processo.findall('.//titular') if processo is not None else []
    
    comentario = despacho.find('comentario').text if despacho.find('comentario') is not None else None
    if comentario is not None:
        data.append([despacho_id, codigo_despacho, titulo, numero_processo, data_deposito, comentario])
    else:
        data.append([despacho_id, codigo_despacho, titulo, numero_processo, data_deposito, None])
   
    for titular in titulares:
        sequencia_titular = titular.attrib['sequencia']
        nome_completo = titular.find('nome-completo').text
        endereco = titular.find('endereco')
        uf = endereco.find('uf').text if endereco is not None and endereco.find('uf') is not None else None
        pais = endereco.find('pais/sigla').text if endereco is not None and endereco.find('pais/sigla') is not None else None
        data[-1].extend([[sequencia_titular, nome_completo, uf, pais]])

    return data

data = []
root = tree.getroot()
for despacho in root.findall('despacho'):
    data.extend(extract_data(despacho))

# Essa função organiza os dados para serem compatíveis com dataframe
def flatten_data(data: list) -> any:

    flattened_data = []
    
    for row in data:
        despacho_id = row[0]
        codigo_despacho = row[1]
        titulo = row[2]
        numero_processo = row[3]
        data_deposito = row[4]
        comentario = row[5]
        
    for titular_info in row[6:]:
        sequencia_titular = titular_info[0]
        nome_completo = titular_info[1]
        uf = titular_info[2]
        pais = titular_info[3]
        
    flattened_data.append([despacho_id, codigo_despacho, titulo, numero_processo, data_deposito, comentario, sequencia_titular, nome_completo, uf, pais])

    # Create DataFrame
    df = pd.DataFrame(flattened_data, columns=['despacho_id', 'codigo_despacho', 'titulo', 'numero_processo', 'data_deposito', 'comentario', 'sequencia_titular', 'nome_completo', 'uf', 'pais'])
    
    # Save DataFrame to CSV and SQL
    df.to_csv(str('P'+numero_rpi_str+'.csv'), sep=',', index=False, encoding='utf-8')

    return df

if __name__ == '__main__':

    get_rpi_patentes(url_template,numero_rpi_str)
    unziper(file_name)
    extract_data()
    flatten_data()

