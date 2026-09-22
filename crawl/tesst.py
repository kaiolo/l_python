import pandas as pd 
import re

a=pd.Series([1,3,4,5,"print"])
mask = a.apply(lambda x : isinstance (x , int) )
assert mask.all()
