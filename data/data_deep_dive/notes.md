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

#### Nation Profit
- Iraq is first, Jordan is last
- 7.8B - 9.3B range

#### Region Profit
- America is number 1 in profit
- Africa is the least
- All regions have roughly similar profits of 42-44B

## Data Correlation