import os

# Função para remover arquivos ZIP do diretório
def swiper(file_extension) -> None:


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
                print(f'File {file_path} removed successfully!')


def mover():
    pass

if __name__ == '__main__':
    
    file_extensions = ['.zip', '.txt']
    for ext in file_extensions:
        swiper(ext)
    mover()
