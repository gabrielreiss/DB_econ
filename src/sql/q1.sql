select  DT_ARQUIVO,
        count(*)
from ind_econ_b3
GROUP BY DT_ARQUIVO;

SELECT DISTINCT CD_INDICADOR
from ind_econ_b3;