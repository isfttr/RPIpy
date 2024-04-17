import requests
import zipfile
import os
import re

url_template = 'https://revistas.inpi.gov.br/txt/P{}.zip'

def check_xml_exists(numero_rpi_start: int, numero_rpi_end: int) -> list:
    missing_rpi = []

    for numero_rpi in range(numero_rpi_start, numero_rpi_end+1):  
        xml_file_name = 'P{}.xml'.format(numero_rpi)

        if not os.path.exists(xml_file_name):
            print(f'CheckXML: {xml_file_name} não existe...')
            missing_rpi.append(numero_rpi)

    if missing_rpi:
        print(f'CheckXML: Não foram encontrados os arquivos referentes as RPIs: {", ".join(map(str, missing_rpi))}...')
    else:
        print(f'CheckXML: Todos arquivos encontrados!')
    
    return missing_rpi or None


def get_rpi_patentes(url_template: str, missing_rpi: list) -> None:
    # Construct new URL using numero_rpi 
    for numero_rpi in missing_rpi:
        file_name = 'P{}.zip'.format(numero_rpi)
        url = url_template.format(numero_rpi)
        # Send a GET request to the url_template
        if os.path.exists(file_name):
            print(f'Get: {file_name} já disponível. Indo para o próximo.')
        else:
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

                print(f'Get: Arquivo {file_name} obtido com sucesso!')

            else:
                print(f'Get: Download não finalizado: {response.status_code}')

def unzip(missing_rpi: list) -> None:        
    for numero_rpi in missing_rpi:
        file_name:str = 'P{}.zip'.format(numero_rpi)   
        try:
            with zipfile.ZipFile(file_name, 'r') as zf:
                zf.extractall()
                print(f'Unzip: Arquivo {file_name} descompactado com sucesso!')

        except zipfile.BadZipFile:
            print(f'Unzip Error: O arquivo {file_name} não é um arquivo ZIP válido.')

def rename_xml(missing_rpi: list) -> None:   
    for numero_rpi in missing_rpi:
        pattern = r'(\w{3,20})_(\d{4})_(\d{1,8})\.xml'
        for file_name in os.listdir('.'):  # Iterate through files in the current directory
            if re.match(pattern, file_name):  # Check if the file_name matches the pattern
                match = re.search(pattern, file_name)  # Extract the number from the file_name
                if match.group(2) == str(numero_rpi):  # Check if the extracted numero_rpi matches the input numero_rpi
                    new_file_name = f'P{numero_rpi}.xml'  # Define the new file_name
                    os.rename(file_name, new_file_name)  # Rename the file
                    print(f'RenameXML: Arquivo {file_name} renomeado para {new_file_name}.')

if __name__ == '__main__':
    # Prompt for RPI number
    numero_rpi_start = int(input('PatentExtractor: Escreva o número de RPI inicial: '))
    numero_rpi_end = int(input('PatentExtractor: Escreva o número de RPI final: '))

    missing_rpi = check_xml_exists(numero_rpi_start, numero_rpi_end)
    if missing_rpi is None:
        missing_rpi
    else:
        get_rpi_patentes(url_template, missing_rpi)
        unzip(missing_rpi)
        rename_xml(missing_rpi)
