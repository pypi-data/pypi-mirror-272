import numpy as _np
import pandas as _pd
import itertools as _it

def check_dataframe(xs,):
    if (type(xs) is _pd.Series):
        df = xs.to_frame()
        return df,list(df.select_dtypes(exclude=_np.inexact).columns)
    elif (type(xs) is _pd.DataFrame):
        return xs, list(xs.select_dtypes(exclude=_np.inexact).columns)
    else:
        return _pd.DataFrame(xs), None
    
def atoms_to_entropy_matrix(n_vars):
    combos = atoms_to_variables_matrix(n_vars)
    atoms_to_entropy = (combos@combos.T>0).astype(int)    
    return atoms_to_entropy

def atoms_to_variables_matrix(n_vars):
    return _np.array([list(reversed([int(x) for x in bin(k)[2:]]))+[0]*(n_vars-1-int(_np.floor(_np.log(k)/_np.log(2)))) for k in range(1,2**n_vars)])

def entropy_to_atoms_matrix(n_vars):
    return _np.linalg.inv(atoms_to_entropy_matrix(n_vars)).astype(int)

def combination_index(some_vars,all_vars):
    return int("".join(reversed([f"{i}" for i in (_np.isin(_np.array(all_vars),some_vars).astype(int))])),2)-1

def reduce_to_list(some_vars):
    return [var for v in some_vars for var in (v if (hasattr(v,"__len__") and (type(v) is not str)) else [v])]