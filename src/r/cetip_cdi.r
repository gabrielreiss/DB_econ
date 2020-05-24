library(bizdays)

cetip_cdi = function(dt) {
    #A função recebe uma data e retorna um valor numérico em percentual
    stopifnot(length(dt) == 1)

    dt = as.Date(dt)
    url = format(dt, "ftp://ftp.cetip.com.br/MediaCDI/%Y%m%d.txt")

    txt = readLines(url)
    txt = gsub(" ", "", txt)

    cdi = as.numeric(txt)/100
    return(cdi)
}

#fazer um link com a ultima data que o programa rodou e colocar no inicio
gerar_cdi <- function(inicio = as.Date("2012-08-20"),
                      hoje = Sys.Date()
                      ){
    #gerar dias uteis
    cal = bizdays::create.calendar( "ANBIMA", bizdays::holidaysANBIMA, weekdays = c("saturday", "sunday") )
    datas = bizdays::bizseq( as.Date(inicio), as.Date(hoje), "ANBIMA" )

    #gerar df com os valores
    df_cdi = data.frame()
    total = length(datas)
    for( i in 1:total){
        dt = datas[i]
        cdi = cetip_cdi(dt)
        df_cdi = rbind(df_cdi, c(as.character(dt), cdi), stringsAsFactors = F)
        print(paste(i, "de", total))
    }
    names(df_cdi) <- c("data", "cdi")
    df_cdi$data <- as.Date(df_cdi$data)
    df_cdi$cdi <- as.numeric(df_cdi$cdi)

    return(df_cdi)
}

#salvando em csv
atualizando_cdi <- function(arquivo_csv = "data/df_cdi.csv"){
    if( file.exists(arquivo_csv) ){
        #atualizando tabela
        print("atualizando valores do CDI")

        #lê o arquivo
        df_cdi = read.csv(arquivo_csv,
                        stringsAsFactors= F)
        #transforma a data em formato de data
        df_cdi$data = as.Date(df_cdi$data)

        #adiciona os novos valores
        df_cdi = rbind(df_cdi,
                    gerar_cdi(inicio = df_cdi[nrow(df_cdi),"data"])
                    )
        #exclui repetidos, caso tenha
        df_cdi = unique(df_cdi)

        print("printando ultimos valores da tabela:")
        print(tail(df_cdi))

        #salva em csv
        write.csv(df_cdi, file = arquivo_csv, row.names= FALSE)
    } else{
        #criando tabela do zero
        df_cdi = gerar_cdi()
        write.csv(df_cdi, file = arquivo_csv, row.names= FALSE)
    }
}

atualizando_cdi()