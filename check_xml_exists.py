import os

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
    

        

if __name__ == '__main__':
    # Prompt for RPI number
    numero_rpi_start = int(input('Escreva o número de RPI inicial: '))
    numero_rpi_end = int(input('Escreva o número de RPI final: '))

    check_xml_exists(numero_rpi_start, numero_rpi_end)
    # print(check_xml_exists(numero_rpi_start, numero_rpi_end))