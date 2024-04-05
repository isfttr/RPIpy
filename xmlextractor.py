import xml.etree.ElementTree as ET
import pandas as pd
import uuid 
from uuid import uuid4

tree = ET.parse('P2777.xml')

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
        nome_completo = titular.find('nome-completo').text
        endereco = titular.find('endereco')
        uf = endereco.find('uf').text if endereco is not None and endereco.find('uf') is not None else None
        pais = endereco.find('pais/sigla').text if endereco is not None and endereco.find('pais/sigla') is not None else None
        data[-1].extend([nome_completo, uf, pais])

    return data

data = []
root = tree.getroot()
for despacho in root.findall('despacho'):
    data.extend(extract_data(despacho))

print(data)
