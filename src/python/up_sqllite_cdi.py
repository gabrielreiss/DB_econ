import os
import sqlalchemy
import argparse
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname( os.path.dirname(__file__) ) )
DATA_DIR = os.path.join( BASE_DIR, 'data' )
SQL_DIR = os.path.join( BASE_DIR, 'src', 'sql' )
RESULT_DIR = os.path.join( BASE_DIR, 'resultado' )

print(DATA_DIR)

# Abrindo conexão com banco...

str_connection = os.path.join( 'sqlite:///', DATA_DIR, 'DB_econ.db' )
engine = sqlalchemy.create_engine( str_connection )
connection = engine.connect()

# Encontrando os arquivos de dados
files_names = [ i for i in os.listdir( DATA_DIR ) if i.endswith('.csv') ]

def data_quality(x):
    if type(x) == str:
        return x.replace("\n", "").replace("\r", '')
    else:
        return x

# Para cada arquivo é realizado uma inserção no banco
for i in files_names:
    print(i)
    df_tmp = pd.read_csv( os.path.join( DATA_DIR, i )  )
    for c in df_tmp.columns:
        df_tmp[c] = df_tmp[c].apply(data_quality)

    table_name = "tb_" + i.strip(".csv").replace("df_", "")
    #print(df_tmp.head())
    df_tmp.to_sql( table_name,
                   connection,
                   if_exists='replace',
                   index=False )