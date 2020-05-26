#para baixar toda a base de uma vez usa:
#titulos_publicos.py -start "2003-01-01"
#para atualizar a base apenas precisa rodar o codigo sem argumentos

import pandas as pd
import datetime
import os
import urllib.request
import zipfile
import sqlalchemy
import argparse

BASE_DIR = 'F:\Aprendendo python\BD_econ'
BASE_DIR = os.path.dirname(os.path.dirname( os.path.dirname( __file__ ) ) )
DATA_DIR = os.path.join( BASE_DIR, 'data' )
SQL_DIR = os.path.join( BASE_DIR, 'src', 'sql' )
RESULT_DIR = os.path.join( BASE_DIR, 'resultado' )
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'Downloads')

str_connection = 'sqlite:///' + os.path.join( DATA_DIR, 'DB_econ.db' )
engine = sqlalchemy.create_engine( str_connection )
connection = engine.connect()

#criando o argparse
#dados disponivel a partir de '2003-01-01'
parser = argparse.ArgumentParser(description='Data de inicio da busca')
parser.add_argument('-start',
                    help='uma data a partir de 2003-01-01',
                    default=str(datetime.date.today()))
parser.add_argument('-end',
                    help='uma data a partir de 2003-01-01',
                    default=str(datetime.date.today()))
args = parser.parse_args()                    

def titulos_publicos_sql(dt):
    dt = datetime.datetime.strptime(dt, '%Y-%m-%d')

    url = 'https://www4.bcb.gov.br/pom/demab/negociacoes/download/NegE{}{}.ZIP'.format(dt.year, dt.strftime('%m'))

    filename = "NegE{}{}.ZIP".format(
            dt.strftime("%Y"),
            dt.strftime("%m")
    )

    urllib.request.urlretrieve(url, os.path.join(DOWNLOAD_DIR, filename))

    with zipfile.ZipFile(os.path.join(DOWNLOAD_DIR, filename), 'r') as zip_ref:
        zip_ref.extractall(DOWNLOAD_DIR)

    #remove o arquivo zipado
    os.remove(os.path.join(DOWNLOAD_DIR,filename))

    filename = "NegE{}{}.CSV".format(
            dt.strftime("%Y"),
            dt.strftime("%m")
    )

    dados = pd.read_csv(os.path.join(DOWNLOAD_DIR, filename), 
                        sep = ";", 
                        decimal = ",")

    dados.columns = [sub.replace(' ', '_') for sub in dados.columns.to_list()]

    for i in ["DATA_MOV", "VENCIMENTO", "EMISSAO"]:
        dados[i] = dados[i].astype(str)
        dados[i] = pd.to_datetime(dados[i], format="%d/%m/%Y")
        dados[i] = dados[i].astype(str)

    #remove arquivo csv
    os.remove(os.path.join(DOWNLOAD_DIR,filename))               

    dados.to_sql("titulos_publicos",
                con = connection,
                if_exists = 'append',
                index = False
    )

#titulos_publicos_sql("2020-05-01")

#tenta buscar a última data no banco
try:
    with open( os.path.join(SQL_DIR, 'max_date_titulos_publicos.sql') ) as query_file:
        query = query_file.read()

    df = pd.read_sql_query( query,
                            connection
    )
    inicio = df.values.tolist()[0][0]
    inicio = datetime.datetime.strptime(inicio, '%Y-%m-%d') + datetime.timedelta(days=1)
    
    if args.start < inicio:
        inicio = datetime.datetime.strptime(args.start, '%Y-%m-%d')
except:
    inicio = datetime.datetime.strptime(args.start, '%Y-%m-%d')

#busca data de hoje
hoje = datetime.datetime.strptime(args.end, '%Y-%m-%d')

datas = pd.date_range(start= inicio,end=hoje + datetime.timedelta(days=31), freq= 'M')
datas = datas.sort_values(ascending = False).astype(str)
total = len(datas)

if total !=0:
    for i in range(0,total):
        try:
            titulos_publicos_sql(datas[i])
            #os.remove(os.path.join(DOWNLOAD_DIR,'Indic.txt'))
            #os.remove(os.path.join(DOWNLOAD_DIR, os.listdir(DOWNLOAD_DIR)[0]))
            d = datetime.datetime.strptime(datas[i], '%Y-%m-%d')
            print(i+1, "de", total, "inserindo dados do mês {}-{}".format(d.strftime("%Y"),d.strftime("%m")))
            #time.sleep(1)
        except:
            #print("não tem valores nesta data: {}".format(date))
            d = datetime.datetime.strptime(datas[i], '%Y-%m-%d')
            print(i+1, "de", total, "Arquivo não disponível do mês {}-{}".format(d.strftime("%Y"),d.strftime("%m")))
else:
    try:
        data = "{}-{}-{}".format(
        inicio.strftime("%Y"),
        inicio.strftime("%m"),
        inicio.strftime("%d"),
        )
        print("inserindo dados do mês {}-{}".format(inicio.strftime("%Y"),inicio.strftime("%m")))
        titulos_publicos_sql(data)
    except:
        print("Arquivo não disponível do mês {}-{}".format(inicio.strftime("%Y"),inicio.strftime("%m")))

#deletar duplicadas
try:
    print("Apagando dados duplicados...")
    with open( os.path.join(SQL_DIR, 'delete_dupl_titulo_publico.sql') ) as query_file:
        query = query_file.read()
    
    connection.execute(query)
    print("Dados duplicados apagados")

except:
    print("Sem necessidade de deletar duplicadas")