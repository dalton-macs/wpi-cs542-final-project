select
	sum(l_extendedprice * l_discount) as revenue
from
	lineitem
where
	l_shipdate >= date('1994-01-01')
	and l_shipdate < date('1994-01-01', '1 year')
	and l_discount BETWEEN 0.05 AND 0.07
	and l_quantity < 24;
