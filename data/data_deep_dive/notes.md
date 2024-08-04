# Data Deep Dive Notes

## Underlying Numerical Data Columns

- **Notes/Findings**
    - Most numerical items follow a uniform distribution (rather than normal)
    - Low cardinality fields:
        - L_Discount, L_Tax
    - L_ExtendedPrice is right skewed
    - 50 distinct values in L_Quantity, each with roughly 120K appearence
        - Wonder why the TPCH designers went with these uniform distributions??
    - O_ShipPriority should be ignored, single value in databse (0)
    - O_TotalPrice seems to be a normal distribution shifted about 100K
        - Slightly right skewed
        - multimodal? 50 and 100K
        - Only field with outliers based on relative min/max calculation (Q1-1.5xIQR and Q3+1.5xIQR, respectively)
            - Boxplot shows outliers and I confirmed with a simple jupyter notebook
    - P_RetailPrice is uniform between 1100-1900 and has tapering tails
- **Next Steps**
    - Would be interesting to see max/min/average/etc. aggregation performance on uniform vs semi-normal distributions for larger fields (high count fields)
        - P_RETAILPRICE vs L_EXTENDEDPRICE and O_TOTALPRICE
        - L_QUANTITY vs L_EXTENDEDPRICE and O_TOTALPRICE
    - Same as above but between uniform distributions with low count and high count
        - P_RETAILPRICE vs. L_QUANTITY
    - Same as above but for low vs high cardinality data
        - PS_SUPPLYCOST vs L_QUANTITY
        - PS_SUPPLYCOST vs S_ACCTBAL



## Query Behavior


## High Level Statistics
### Notes/Findings
- **General**
    - Profit formula below (from Q9 in TPCH doc)
       ```sql
        SUM(L.L_EXTENDEDPRICE * (1 - L.L_DISCOUNT) - (PS.PS_SUPPLYCOST * L.L_QUANTITY))
       ```
    - For customer spend, used O.O_TOTALPRICE
    - O.O_TOTALPRICE is calculated from lineitem as follows
        ```sql
        SUM((L_EXTENDEDPRICE * (1- L_DISCOUNT)) * (1 + L_TAX))
        ```
- **Nation Profit**
    - Iraq is first, Jordan is last
    - 5.1B - 6.1B range
- **Region Profit**
    - America is number 1 in profit
    - Africa is the least
    - All regions have roughly similar profits of 27.8-28.9B
- **Which customers spent the most?**
    - 143500, 95257, 87115, 131113, 103834
- **Which nations have the highest order total?**
    - France, Indonesia, Russia, Mozambique, Jordan
- **Which regions have the highest order total?**
    - Europe, Asia, America, Africa, Middle East
- **Which customers order the most diversely (suppliers in many nations)?**
    - 143500, 95257, 87115, 103834, 134380 all ordered from 25 nations with average nation spend price of > $250K
- **Which customers order the most diversely (suppliers in many regions)?**
    - 143500, 95257, 87115, 131113, 103834 all ordered from 5 regions with average nation spend price of > $1.25M
- **Which market segment had the most orders?**
    - Building, household, furniture, machinery, automobile
    - All roughly the same number of orders, around 300K
- **Which market segment spent the most (average order price)?**
    - automobile, furniture, household, machinery, building
    - all roughly same average order price of $151K, yet order changed from above


## Data Correlation
### Notes/Findings
- In order to run correlations, the data needed to be the same length
    1. Selected data from all numerical columns
    2. Found field with lowest number of datapoints
    3. Randomly select the min value from all other fields to approximate the data distribution
    4. Run correlations
- Only L_QUANTITY and L_EXTENDEDPRICE seem correlated (highly)
    - makes sense... as quantity increases, so does overal price