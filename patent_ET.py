import requests
import zipfile
import os

from modules.rpi.patent_extractor import get_rpi_patentes, rename_xml
from modules.rpi.patent_transformer import extract_data



# numero_rpi = input('Escreva o número de RPI desejado: ')
url_template = 'https://revistas.inpi.gov.br/txt/P{}.zip'

directory = os.getcwd()


def main() -> None:

    get_rpi_patentes(url_template, numero_rpi_start, numero_rpi_end)
    rename_xml(directory)


if __name__ == '__main__':
    # Prompt for RPI number
    numero_rpi_start = int(input(f'Escreva o número de RPI inicial: '))
    numero_rpi_end = int(input(f'Escreva o número de RPI final: '))
    main()
