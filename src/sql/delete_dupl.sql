/*selecionar duplicadas*/
WITH cte AS (
    SELECT 
        DATA_MOV, 
        EMISSAO, 
        QUANT_NEGOCIADA, 
        CODIGO_ISIN,
        ROW_NUMBER() OVER (
            PARTITION BY 
                DATA_MOV, 
                EMISSAO, 
                QUANT_NEGOCIADA, 
                CODIGO_ISIN
            ORDER BY 
                DATA_MOV, 
                EMISSAO, 
                QUANT_NEGOCIADA, 
                CODIGO_ISIN
        ) row_num
     FROM 
        titulos_publicos
)
SELECT * FROM cte
WHERE row_num > 1;

/* deletar selecionadas */
/*
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
*/