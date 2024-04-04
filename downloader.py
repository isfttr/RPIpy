import requests



# url_template of the file to download
url_template = 'https://revistas.inpi.gov.br/txt/P{}.zip'

# Prompt for RPI numb
number = input('Escreva o número de RPI desejado: ')

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

    print(f'File {file_name} downloaded successfully!')
else:
    print(f'Failed to download file: {response.status_code}')