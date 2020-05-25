select  DT_ARQUIVO,
        count(*)
from ind_econ_b3
GROUP BY DT_ARQUIVO
ORDER BY DT_ARQUIVO DESC;

SELECT DISTINCT CD_INDICADOR
from ind_econ_b3;

select *
from ind_econ_b3
limit 10;