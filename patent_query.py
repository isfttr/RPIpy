import pandas as pd


# Prompt inicial
numero_rpi_str:str = input("Número de RPI: ") 
numero_rpi:int = int(numero_rpi_str)

file_name:str = str('P'+numero_rpi_str+'.csv')

# Import CSV
df = pd.read_csv(file_name)

# Get a titular to query
titular:str = input('Nome do titular (default: FUB):')
if not titular:
    titular = "Fundação Universidade de Brasília"

# Busca por despachos de um titular
def patent_query(df: any):
    query = df.query('nome_completo == @titular' )
    query.to_csv(str('P'+file_name+'_despachos_salvos.csv'))
    return 

if __name__ == '__main__':
    patent_query(df)
    