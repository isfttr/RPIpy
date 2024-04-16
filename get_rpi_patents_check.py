import requests
import os

url_template = 'https://revistas.inpi.gov.br/txt/P{}.zip'

def check_xml_exists(numero_rpi_start, numero_rpi_end) -> list:
    missing_rpi = []

    for numero_rpi in range(numero_rpi_start, numero_rpi_end+1):  
        xml_file_name = 'P{}.xml'.format(numero_rpi)

        if not os.path.exists(xml_file_name):
            print(f'CheckXML: {xml_file_name} não existe...')
            missing_rpi.append(numero_rpi)

    if missing_rpi:
        print(f'CheckXML: Não foram encontrados os arquivos referentes as RPIs: {", ".join(map(str, missing_rpi))}...')
        return missing_rpi
    else:
        print(f'CheckXML: Todos arquivos encontrados!')

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

if __name__ == '__main__':
    # Prompt for RPI number
    numero_rpi_start = int(input('PatentExtractor: Escreva o número de RPI inicial: '))
    numero_rpi_end = int(input('PatentExtractor: Escreva o número de RPI final: '))
    missing_rpi = check_xml_exists(numero_rpi_start, numero_rpi_end)
    get_rpi_patentes(url_template, missing_rpi)