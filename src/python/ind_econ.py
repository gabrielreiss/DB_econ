import pandas as pd
import datetime
import os
import urllib.request
import sqlalchemy
import zipfile
import time
import glob

BASE_DIR = 'F:\Aprendendo python\BD_econ'
BASE_DIR = os.path.dirname(os.path.dirname( os.path.dirname( __file__ ) ) )
DATA_DIR = os.path.join( BASE_DIR, 'data' )
SQL_DIR = os.path.join( BASE_DIR, 'src', 'sql' )
RESULT_DIR = os.path.join( BASE_DIR, 'resultado' )
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'Downloads')

str_connection = 'sqlite:///' + os.path.join( DATA_DIR, 'DB_econ.db' )
engine = sqlalchemy.create_engine( str_connection )
connection = engine.connect()

def ind_econ_b3(date = "2020-05-22",connection= connection):
    #print(date)

    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    url = "ftp://ftp.bmf.com.br/IndicadoresEconomicos/ID{}{}{}.ex_".format(
        date.strftime("%y"),
        date.strftime("%m"),
        date.strftime("%d")
    )

    filename = "ID{}{}{}.exe".format(
        date.strftime("%y"),
        date.strftime("%m"),
        date.strftime("%d")
    )

    urllib.request.urlretrieve(url, os.path.join(DOWNLOAD_DIR, filename))

    with zipfile.ZipFile(os.path.join(DOWNLOAD_DIR, filename), 'r') as zip_ref:
        zip_ref.extractall(DOWNLOAD_DIR)
    #os.startfile(os.path.join(DOWNLOAD_DIR, filename))

    file = glob.glob(os.path.join(DOWNLOAD_DIR, "*.txt"))
    file = file[0]
    layout = pd.read_csv(os.path.join(DATA_DIR,"layout","layout_bmfindic.csv"), sep= ";")
    df_ind = pd.read_fwf(file,
                            widths=layout["tamanho"],
                            names = layout.campo.tolist())

    os.remove(file)
    os.remove(glob.glob(os.path.join(DOWNLOAD_DIR, "*.exe"))[0])

    df_ind["VL_INDICADOR"] = df_ind["VL_INDICADOR"] / 10 ** df_ind["NUM_CASAS_DECIMAIS"]
    del(df_ind["NUM_CASAS_DECIMAIS"])
    df_ind["DT_ARQUIVO"] = df_ind["DT_ARQUIVO"].astype(str)
    df_ind["DT_ARQUIVO"] = pd.to_datetime(df_ind["DT_ARQUIVO"], format="%Y%m%d")
    df_ind = df_ind[df_ind["DT_ARQUIVO"]==date]
    df_ind["DT_ARQUIVO"] = df_ind["DT_ARQUIVO"].astype(str)

    df_ind.to_sql(  "ind_econ_b3",
                    con = connection,
                    if_exists = 'append',
                    index = False)


#ind_econ_b3(date = "2020-05-22",connection= connection)

hoje = datetime.date.today()
inicio = datetime.datetime.strptime("1999-09-30", '%Y-%m-%d')
datas = pd.date_range(start= inicio,end=hoje)
datas = datas.sort_values(ascending = False).astype(str)
total = len(datas)

for i in range(0,total):
    try:
        ind_econ_b3(datas[i])
        #os.remove(os.path.join(DOWNLOAD_DIR,'Indic.txt'))
        #os.remove(os.path.join(DOWNLOAD_DIR, os.listdir(DOWNLOAD_DIR)[0]))
        print(i, "de", total, datas[i])
        #time.sleep(1)
    except:
        #print("não tem valores nesta data: {}".format(date))
        print(i, "de", total, datas[i])