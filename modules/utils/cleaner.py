import os
from pathlib import Path

# Função para remover arquivos ZIP do diretório
def swipe_all_extensions(file_extension) -> None:
    # Get the current working directory
    cwd = os.getcwd()

    # Define the directory to search for files
    directory = cwd

    # Iterate over all the files in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file ends with the specified extension
            if file.endswith(file_extension):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f'SwipAllExtensions: Arquivo {file_path} removido com sucesso!')

def swipe_csv(numero_rpi_start: int, numero_rpi_end: int) -> None:
    for numero_rpi in range(numero_rpi_start, numero_rpi_end+1):  
        csv_file_name = 'P{}.csv'.format(numero_rpi)

        if not os.path.exists(csv_file_name):
            print(f'SwipeCSV: {csv_file_name} não existe...')
        else:
            file_path = Path(csv_file_name)
            file_path.unlink()
            print(f'SwipeCSV: {csv_file_name} excluído...')
    

    
def mover():
    pass

if __name__ == '__main__':
    
    file_extensions = ['.zip', '.txt', '.xml', '.csv']
    for extension in file_extensions:
        swipe_all_extensions(extension)
    mover()
