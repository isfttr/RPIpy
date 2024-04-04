#import xml.etree.ElementTree as ET
from lxml import etree as ET

# Parse XML intro ElementTree
tree = ET.parse('P2777.xml')
root = tree.getroot()

numero_rpi = root.get('numero')
data_publicacao = root.get('dataPublicacao')
#data_deposito = tree.findall('data-deposito')


#print(root.attrib)
print("Total de:",len(root)," despachos")

chave_pesquisa = 'UNIVERSIDADE FEDERAL DE MINAS GERAIS'

for nome_completo in root.iter('nome-completo'):
    # Check if the element has text and if it matches the search text
    if nome_completo.text and chave_pesquisa == nome_completo.text:
        # If it matches, print the parent element and its parent
        print(nome_completo.getparent().getparent().getparent().getparent().text)
        despacho = nome_completo.getparent().getparent().getparent().getparent()

        # Print the 'codigo' text
        codigo_despacho = despacho.find('codigo')
        if codigo_despacho is not None:
            print('Código:', codigo_despacho.text)

        titulo_despacho = despacho.find('titulo')
        if titulo_despacho is not None:
            print('Título:', titulo_despacho.text)

        processo_patente = nome_completo.getparent().getparent().getparent()
        numero_protecao = processo_patente.find('numero')
        if numero_protecao is not None:
            print('Número:', numero_protecao.text)

        data_deposito = processo_patente.find('data-deposito')
        if data_deposito is not None:
            print('Data de depósito:', data_deposito.text)

        titulo_protecao = processo_patente.find('titulo')
        if titulo_protecao is not None:
            print('Título:', titulo_protecao.text)

        titular_lista = nome_completo.getparent().getparent()
        #sequencia_titular = titular_lista.find('titular')
        #if sequencia_titular is not None:
        #    print('# Titular:', sequencia_titular.attrib['sequencia'])
        print('Número de titulares: ', len(titular_lista))

        nome_titular = nome_completo.getparent()
        titular = nome_titular.find('nome-completo')
        if titular is not None:
            print('Titular:', titular.text)
            
            print('---')
