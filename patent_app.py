import requests
import zipfile
import os
import glob
import xml.etree.ElementTree as ET
import pandas as pd
import asyncio

from modules.rpi.patent_extractor import check_xml_exists, get_rpi_patentes, unzip, rename_xml
from modules.rpi.patent_transformer import check_csv_exists, find_xml_in_missing_rpi_csv, extract_metadata, build_dataframe

url_template = 'https://revistas.inpi.gov.br/txt/P{}.zip'


if __name__ == '__main__':
    # Prompt for RPI number
    numero_rpi_start = int(input(f'PatentApp: Escreva o número de RPI inicial: '))
    numero_rpi_end = int(input(f'PatentApp: Escreva o número de RPI final: '))

    missing_rpi = check_xml_exists(numero_rpi_start, numero_rpi_end)

    missing_rpi_csv = check_csv_exists(numero_rpi_start, numero_rpi_end)
    found_xml_files = find_xml_in_missing_rpi_csv(missing_rpi_csv)


    if missing_rpi is None:
        missing_rpi
    else:
        get_rpi_patentes(url_template, missing_rpi)
        unzip(missing_rpi)
        rename_xml(missing_rpi)

    if found_xml_files is None:
        find_xml_in_missing_rpi_csv
    else:
        for numero_rpi in found_xml_files:
            xml_file_name = 'P{}.xml'.format(numero_rpi)
            tree = ET.parse(xml_file_name)
            root = tree.getroot()
            despacho = root.find('despacho')

            extract_metadata(numero_rpi, despacho)
            build_dataframe(found_xml_files)
    


