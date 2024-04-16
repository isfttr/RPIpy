import os
import re


numero_rpi_start = int(input('Escreva o número de RPI inicial: '))
numero_rpi_end = int(input('Escreva o número de RPI final: '))


def rename_xml(numero_rpi_start: int, numero_rpi_end: int) -> None:
    for numero_rpi in range(numero_rpi_start, numero_rpi_end+1):
        pattern = r'(\w{3,20})_(\d{4})_(\d{1,8})\.xml'

        for file_name in os.listdir('.'):  # Iterate through files in the current directory
            if re.match(pattern, file_name):  # Check if the file_name matches the pattern
                match = re.search(pattern, file_name)  # Extract the number from the file_name
                if match.group(2) == str(numero_rpi):  # Check if the extracted numero_rpi matches the input numero_rpi
                    new_file_name = f'P{numero_rpi}.xml'  # Define the new file_name
                    os.rename(file_name, new_file_name)  # Rename the file
                    print(f'Renamed {file_name} to {new_file_name}.')


if __name__ == '__main__':
    rename_xml(numero_rpi_start, numero_rpi_end)
