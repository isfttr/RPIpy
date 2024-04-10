import xml.etree.ElementTree as ET
import pandas as pd
import glob
import os
import uuid 
from uuid import uuid4

# Prompt inicial
# numero_rpi_str:str = input("Número de RPI: ")
# numero_rpi:int = int(numero_rpi_str)



# Parsing do arquivo XML
xml_files = glob.glob("*.xml")

for i, xml_file in enumerate(xml_files):
    filename = os.path.splitext(os.path.basename(xml_file))[0]
    # Extract the numeric part from the filename
    numero_rpi_str = ''.join(filter(str.isdigit, filename))
    
    if numero_rpi_str: 
        numero_rpi = int(numero_rpi_str)
        print(f"Processando {xml_file}... para RPI {numero_rpi} Patentes!")
        tree = ET.parse(xml_file)
        # Função de extração de todos os despachos contidos no XML
        def extract_data(despacho: any) -> list:
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
                data.append([numero_rpi, despacho_id, codigo_despacho, titulo, numero_processo, data_deposito, comentario])
            else:
                data.append([numero_rpi, despacho_id, codigo_despacho, titulo, numero_processo, data_deposito, None])
        
            for titular in titulares:
                sequencia_titular = titular.attrib['sequencia']
                nome_completo = titular.find('nome-completo').text
                endereco = titular.find('endereco')
                uf = endereco.find('uf').text if endereco is not None and endereco.find('uf') is not None else None
                pais = endereco.find('pais/sigla').text if endereco is not None and endereco.find('pais/sigla') is not None else None
                data[-1].extend([[sequencia_titular, nome_completo, uf, pais]])

            return data

        data = []

        # Process the XML tree
        root = tree.getroot()

        for despacho in root.findall('despacho'):
            data.extend(extract_data(despacho))    # Continue with your code that uses the parsed XML tree

        # Essa função organiza os dados para serem compatíveis com dataframe
        def flatten_data(data: list, xml_file: str) -> any:
            flattened_data = []

            for row in data:
                numero_rpi = row[0]
                despacho_id = row[1]
                codigo_despacho = row[2]
                titulo = row[3]
                numero_processo = row[4]
                data_deposito = row[5]
                comentario = row[6]
                
                for titular_info in row[7:]:
                    sequencia_titular = titular_info[0]
                    nome_completo = titular_info[1]
                    uf = titular_info[2]
                    pais = titular_info[3]
                
                    flattened_data.append([numero_rpi, despacho_id, codigo_despacho, titulo, numero_processo, data_deposito, comentario, sequencia_titular, nome_completo, uf, pais])

            # Create DataFrame
            df = pd.DataFrame(flattened_data, columns=['numero_rpi', 'despacho_id', 'codigo_despacho', 'titulo', 'numero_processo', 'data_deposito', 'comentario', 'sequencia_titular', 'nome_completo', 'uf', 'pais'])
            numero_rpi_str = ''.join(filter(str.isdigit, os.path.splitext(os.path.basename(xml_file))[0]))
            csv_file = df.to_csv(f"P{numero_rpi_str}.csv", sep=',', index=False, encoding='utf-8')
            print(f"CSV criado: {csv_file}.")
            return df 
    

        print(f"Done processing {xml_file}.")
    else:
        print(f"Skipping {xml_file}, no numeric part found in the filename!")
   
 

    

if __name__ == '__main__':
    extract_data(despacho)
    flatten_data(data, xml_file)
