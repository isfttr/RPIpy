import requests
import zipfile


# Prompt for RPI number
number = input('Escreva o número de RPI desejado: ')
url_template = 'https://revistas.inpi.gov.br/txt/P{}.zip'
file_name = str('P'+number+'.zip')

def download_file(url_template: str, number: str) -> None:

    # Construct new URL using number 
    url = url_template.format(number)

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

if __name__ == '__main__':

    download_file(url_template,number)
    unziper(file_name)
