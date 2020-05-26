delete from titulos_publicos
where    rowid not in
         (
         select  min(rowid)
         from    titulos_publicos
         group by
                DATA_MOV, 
                EMISSAO, 
                QUANT_NEGOCIADA, 
                CODIGO_ISIN
         )
;
