import xml.etree.ElementTree as ET
import pandas as pd
import uuid 
from uuid import uuid4


# Prompt inicial
numero_rpi_str = input("Número de RPI: ")
numero_rpi = int(numero_rpi_str)

# Parsing do arquivo XML
tree = ET.parse('P'+str(numero_rpi)+'.xml')

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
    
    # Save DataFrame to CSV
    df.to_csv(str('P'+numero_rpi_str)+'.csv', sep=',', index=False, encoding='utf-8')
    
    return df

if __name__ == '__main__':

    extract_data()
    flatten_data()
