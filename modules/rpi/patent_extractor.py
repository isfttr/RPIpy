import requests
import zipfile
import os


# Prompt for RPI number
numero_rpi_start = int(input('Escreva o número de RPI inicial: '))
numero_rpi_end = int(input('Escreva o número de RPI final: '))

# numero_rpi = input('Escreva o número de RPI desejado: ')
url_template = 'https://revistas.inpi.gov.br/txt/P{}.zip'
# file_name = None

def get_rpi_patentes(url_template: str, numero_rpi_start: int, numero_rpi_end: int) -> None:
    # Construct new URL using numero_rpi 
    for numero_rpi in range(numero_rpi_start, numero_rpi_end+1):
        file_name = 'P{}.zip'.format(numero_rpi)
        url = url_template.format(numero_rpi)
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
                unzip(file_name)

            print(f'Arquivo {file_name} obtido com sucesso!')

            
        else:
            print(f'Download não finalizado: {response.status_code}')

def unzip(file_name: str) -> None:
    try:
        with zipfile.ZipFile(file_name, 'r') as zf:
            zf.extractall()
            print(f'Arquivo {file_name} descompactado com sucesso!')
    except zipfile.BadZipFile:
        print(f'Erro: O arquivo {file_name} não é um arquivo ZIP válido.')

def rename_xml(directory: any) -> None:
    """
    Renames XML files in the given directory to have a shorter name.
    """
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            # Extract the number from the filename
            num = filename[8:12]
            # Construct the new filename
            new_filename = f"P{num}.xml"
            # Construct the full paths for the old and new filenames
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            # Rename the file
            os.rename(old_path, new_path)

# Example usage
directory = os.getcwd()
rename_xml(directory)


if __name__ == '__main__':
    get_rpi_patentes(url_template,numero_rpi_start,numero_rpi_end)
    # unzip(file_name)
    rename_xml(directory)
