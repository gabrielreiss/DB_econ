library('RSQLite')
library('readr')

conn = dbConnect(dbDriver("SQLite"), 'data/DB_econ.db')

#dbWriteTable escreve
#dbGetQuery lê
# a query pode ser escrita direto
#df = dbGetQuery(conn, "select max(DT_ARQUIVO) from ind_econ_b3;")

#ou através de um arquivo
df <- RSQLite::dbGetQuery(conn, statement = read_file('src/sql/max_date.sql'))

#cuidar com datas