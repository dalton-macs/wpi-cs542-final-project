-- Which nations has the most profit?

DROP VIEW IF EXISTS NATIONPROFIT;
CREATE VIEW NATIONPROFIT AS
    SELECT 
        N.N_NAME,
        SUM(L.L_EXTENDEDPRICE * (1 - L.L_DISCOUNT) - PS.PS_SUPPLYCOST) AS PROFIT
    FROM
        NATION N
        JOIN SUPPLIER S ON N.N_NATIONKEY = S.S_NATIONKEY
        JOIN LINEITEM L ON S.S_SUPPKEY = L.L_SUPPKEY
        JOIN PARTSUPP PS ON L.L_PARTKEY = PS.PS_PARTKEY AND L.L_SUPPKEY = PS.PS_SUPPKEY
    GROUP BY
        N.N_NAME;

SELECT
    *
FROM
    NATIONPROFIT
ORDER BY
    PROFIT DESC;


-- Which regions has the most profit?

SELECT
    R_NAME, SUM(NP.PROFIT) AS REGION_PROFIT
FROM    
    NATIONPROFIT AS NP
    JOIN NATION N ON NP.N_NAME = N.N_NAME
    JOIN REGION R ON N.N_REGIONKEY = R.R_REGIONKEY
GROUP BY
    R_NAME
ORDER BY
    SUM(NP.PROFIT) DESC;


DROP VIEW IF EXISTS NATIONPROFIT;

