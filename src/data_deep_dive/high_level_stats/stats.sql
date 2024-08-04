DROP VIEW IF EXISTS CUSTORDERPRICE;
DROP VIEW IF EXISTS CUSTOMERSPENDING;
DROP VIEW IF EXISTS MKTSEGMENT;

-- Which nations has the most profit?
DROP VIEW IF EXISTS NATIONPROFIT;
CREATE VIEW NATIONPROFIT AS
    SELECT 
        N.N_NAME,
        SUM(L.L_EXTENDEDPRICE * (1 - L.L_DISCOUNT) - (PS.PS_SUPPLYCOST * L.L_QUANTITY)) AS PROFIT
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


-- Which regions haVE the most profit?
SELECT
    R_NAME, SUM(NP.PROFIT) AS REGION_PROFIT
FROM    
    NATIONPROFIT AS NP
    JOIN NATION N ON NP.N_NAME = N.N_NAME
    JOIN REGION R ON N.N_REGIONKEY = R.R_REGIONKEY
GROUP BY
    R_NAME
ORDER BY
    REGION_PROFIT DESCs;


DROP VIEW IF EXISTS NATIONPROFIT;


-- Which customers spent the most
DROP VIEW IF EXISTS CUSTORDERPRICE;
CREATE VIEW CUSTORDERPRICE AS
    SELECT
        C.C_CUSTKEY,
        C.C_NAME,
        N.N_NAME,
        R.R_NAME,
        SUM(O.O_TOTALPRICE) AS TOTAL_SPENT
    FROM
        CUSTOMER C
        JOIN ORDERS O ON C.C_CUSTKEY = O.O_CUSTKEY
        JOIN NATION N ON C.C_NATIONKEY = N.N_NATIONKEY
        JOIN REGION R ON N.N_REGIONKEY = R.R_REGIONKEY
    GROUP BY
        C.C_CUSTKEY,
        C.C_NAME,
        N.N_NAME,
        R.R_NAME
    ORDER BY
        TOTAL_SPENT DESC;

SELECT * FROM CUSTORDERPRICE;


-- Which nations have the highest order total?
SELECT
    N_NAME,
    SUM(TOTAL_SPENT) AS NATION_TOTAL_SPENT
FROM
    CUSTORDERPRICE
GROUP BY
    N_NAME
ORDER BY NATION_TOTAL_SPENT DESC;


-- Which regions have the highest order total?
SELECT
    R_NAME,
    SUM(TOTAL_SPENT) AS REGION_TOTAL_SPENT
FROM
    CUSTORDERPRICE
GROUP BY
    R_NAME
ORDER BY REGION_TOTAL_SPENT DESC;

DROP VIEW IF EXISTS CUSTORDERPRICE;


-- Which customers order the most diversely (suppliers in many nations)?
DROP VIEW IF EXISTS CUSTOMERSPENDING;
CREATE VIEW CUSTOMERSPENDING AS
    SELECT
        C.C_CUSTKEY,
        C.C_NAME,
        C.C_MKTSEGMENT,
        N.N_NAME,
        R.R_NAME,
        SUM((L_EXTENDEDPRICE * (1- L_DISCOUNT)) * (1 + L_TAX)) AS TOTAL_SPENT
    FROM
        CUSTOMER C
    JOIN
        ORDERS O ON C.C_CUSTKEY = O.O_CUSTKEY
    JOIN
        LINEITEM L ON O.O_ORDERKEY = L.L_ORDERKEY
    JOIN
        PARTSUPP PS ON L.L_PARTKEY = PS.PS_PARTKEY AND L.L_SUPPKEY = PS.PS_SUPPKEY
    JOIN
        SUPPLIER S ON PS.PS_SUPPKEY = S.S_SUPPKEY
    JOIN
        NATION N ON S.S_NATIONKEY = N.N_NATIONKEY
    JOIN
        REGION R ON N.N_REGIONKEY = R.R_REGIONKEY
    GROUP BY
        C.C_CUSTKEY, C.C_NAME, C.C_MKTSEGMENT, N.N_NAME, R.R_NAME;

-- SELECT * FROM CUSTOMERSPENDING;

SELECT
    C_CUSTKEY,
    C_NAME,
    C_MKTSEGMENT,
    COUNT(DISTINCT N_NAME) AS N_NATIONS,
    AVG(TOTAL_SPENT) AS AVG_SPENT_NATION
FROM
    CUSTOMERSPENDING
GROUP BY
    C_CUSTKEY,
    C_NAME,
    C_MKTSEGMENT
ORDER BY
    N_NATIONS DESC, AVG_SPENT_NATION DESC;


-- Which customers order the most diversely (suppliers in many regions)?
SELECT
    C_CUSTKEY,
    C_NAME,
    C_MKTSEGMENT,
    COUNT(DISTINCT R_NAME) AS N_REGIONS,
    SUM(TOTAL_SPENT)/COUNT(DISTINCT R_NAME) AS AVG_SPENT_REGION
FROM
    CUSTOMERSPENDING
GROUP BY
    C_CUSTKEY,
    C_NAME,
    C_MKTSEGMENT
ORDER BY
    N_REGIONS DESC, AVG_SPENT_REGION DESC;

DROP VIEW IF EXISTS CUSTOMERSPENDING;


-- Which market segment had the most orders?
DROP VIEW IF EXISTS MKTSEGMENT;
CREATE VIEW MKTSEGMENT AS
    SELECT
        C.C_MKTSEGMENT,
        COUNT(O.O_ORDERKEY) AS ORDER_COUNT,
        SUM(O.O_TOTALPRICE) AS ORDER_SUM,
        SUM(O.O_TOTALPRICE)/COUNT(O.O_ORDERKEY) AS AVG_ORDER_SPEND
    FROM
        CUSTOMER C
    JOIN
        ORDERS O ON C.C_CUSTKEY = O.O_CUSTKEY
    GROUP BY
        C.C_MKTSEGMENT;

SELECT * FROM MKTSEGMENT
ORDER BY ORDER_COUNT DESC;

-- Which market segment spent the most?
SELECT * FROM MKTSEGMENT
ORDER BY AVG_ORDER_SPEND DESC, ORDER_SUM DESC;

DROP VIEW IF EXISTS MKTSEGMENT;


DROP VIEW IF EXISTS CUSTORDERPRICE;
DROP VIEW IF EXISTS CUSTOMERSPENDING;
DROP VIEW IF EXISTS MKTSEGMENT;