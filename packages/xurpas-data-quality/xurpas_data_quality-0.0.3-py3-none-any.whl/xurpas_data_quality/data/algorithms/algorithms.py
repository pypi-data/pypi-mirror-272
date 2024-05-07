import pandas as pd
from math import log2, ceil, cbrt
from typing import List



def sturges(dataset: pd.Series) -> int:
    return ceil(log2(len(dataset)))

def rice(dataset: pd.Series) -> int:
    return ceil(2*cbrt(len(dataset)))

def freedman_diaconis(dataset: pd.Series) -> int:
    try:
        iqr = dataset.quantile(0.75) - dataset.quantile(0.25)
        n = ceil(2*((iqr)/cbrt(len(dataset))))
        return None if n>100 or n==1 else n
    except:
        return None