import pandas as pd


# Prompt inicial
numero_rpi_str:str = input("Número de RPI: ") 
numero_rpi:int = int(numero_rpi_str)

file_name:str = str(f'P{numero_rpi_str}.csv')

# Import CSV
df = pd.read_csv(file_name)

# Busca por despachos de um titular
def count_despachos(df: any):
    query = df['despacho_id'].nunique()
    query_series = pd.Series(query, name='count')
    # query_series.to_csv(str(f'P{numero_rpi_str}_despachos_count.csv'))    
    print(query)
    return 

if __name__ == '__main__':
    count_despachos(df)
    