get_ind_econ = function(dt) {
    dt = as.Date(dt)
    url = format(dt, "ftp://ftp.bmf.com.br/IndicadoresEconomicos/ID%y%m%d.ex_")

    filename = format(dt, "Downloads/ID%y%m%d.exe")

    download.file(url = url, destfile = filename, mode = "wb")
    files = unzip(zipfile = filename, exdir = "Downloads")

    layout = read.csv2("data/layout/layout_bmfindic.csv")

    dados = read.fwf(
        file = files,
        widths = layout$tamanho,
        header = FALSE,
        col.names = layout$campo,
        stringsAsFactors = FALSE,
        strip.white = TRUE
    )

    dados$DT_ARQUIVO = as.Date(as.character(dados$DT_ARQUIVO), format = "%Y%m%d")
    dados$VL_INDICADOR = dados$VL_INDICADOR / 10^dados$NUM_CASAS_DECIMAIS
    dados$NUM_CASAS_DECIMAIS = NULL
    dados = dados[dados$DT_ARQUIVO == dt,]

    file.remove(files)
    file.remove(filename)

    return(dados)
}

gen_ind_econ = function(
                        inicio = as.Date("2001-01-01"),
                        hoje = Sys.Date()
) {
    library(bizdays)
    #gerar dias uteis
    cal = bizdays::create.calendar( "ANBIMA", bizdays::holidaysANBIMA, weekdays = c("saturday", "sunday") )
    datas = bizdays::bizseq( as.Date(inicio), as.Date(hoje), "ANBIMA" )
    datas = rev(datas)

    df_econ = data.frame()
    total = length(datas)

    for( i in 1:total){
    dt = datas[i]
    temp = get_ind_econ(dt)
    df_econ = rbind(df_econ, temp)
    write.csv(df_econ, file="data/df_econ.csv", append = TRUE)
    print(paste(i, "de", total))
    }

    return(df_econ)

}

#salvando em csv
atualizando_ind_econ <- function(arquivo_csv = "data/df_econ.csv"){
    if( file.exists(arquivo_csv) ){
        #atualizando tabela
        print("atualizando valores das variáveis economicas da B3")

        #lê o arquivo
        df_econ = read.csv(arquivo_csv,
                        stringsAsFactors= F)
        #transforma a data em formato de data
        df_econ$DT_ARQUIVO = as.Date(df_econ$DT_ARQUIVO)
        df_econ = unique(df_econ)

        #adiciona os novos valores
        df_econ = rbind(df_econ,
                    gen_ind_econ(inicio = df_econ[nrow(df_econ),"data"])
                    )
        #exclui repetidos, caso tenha
        df_econ = unique(df_econ)

        print("printando ultimos valores da tabela:")
        print(tail(df_econ))

        #salva em csv
        write.csv(df_econ, file = arquivo_csv, row.names= FALSE)
    } else{
        #criando tabela do zero
        df_econ = gen_ind_econ()
        write.csv(df_econ, file = arquivo_csv, row.names= FALSE)
    }
}