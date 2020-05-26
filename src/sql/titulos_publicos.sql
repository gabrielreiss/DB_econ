select  DATA_MOV, 
        EMISSAO, 
        QUANT_NEGOCIADA, 
        CODIGO_ISIN,
        count(*)
from titulos_publicos
GROUP BY DATA_MOV, CODIGO_ISIN
order by DATA_MOV desc;


select  DATA_MOV,
        COUNT(*)
from titulos_publicos
GROUP BY DATA_MOV
ORDER BY DATA_MOV DESC
limit 10;

/* head */
select *
from titulos_publicos
limit 10;


/* teste de numero
select 
    sum(CODIGO),
    sum(NUM_DE_OPER),
    sum(QUANT_NEGOCIADA),
    sum(VALOR_NEGOCIADO),
    sum(PU_MIN),
    sum(PU_MED),
    sum(PU_MAX),
    sum(PU_LASTRO),
    sum(VALOR_PAR),
    sum(TAXA_MIN),
    sum(TAXA_MED),
    sum(TAXA_MAX),
    sum(NUM_OPER_COM_CORRETAGEM),
    sum(QUANT_NEG_COM_CORRETAGEM)

from titulos_publicos;
*/
