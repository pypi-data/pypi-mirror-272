import numpy as _np
import zentropy.knn_utils as _knn_utils
import zentropy.estimators.utils as _utils
import zentropy.estimators.continuous as _continuous
import zentropy.estimators.discrete as _discrete

def entropy(data,discrete_vars=[],cvars=[],base=2,k=3,r=None):
    data, df_discrete_vars = _utils.check_dataframe(data)
    if df_discrete_vars is not None:
        discrete_vars = df_discrete_vars
    cont_vars = [c for c in data.columns if not(c in discrete_vars)]
    if discrete_vars and cont_vars:
        groupings = data.groupby(discrete_vars)
        surprisals = groupings.apply(
            lambda df: _continuous.entropy_from_points(
                df[cont_vars],
                k=k,
                r=(r[df.index] if hasattr(r,"__len__") else r),
                base=base
            )
        )
        counts = data.value_counts(discrete_vars)
        return _discrete.entropy_from_counts(counts,base=2) + (surprisals*counts).sum()/counts.sum()
    elif discrete_vars:
        return _discrete.entropy_from_counts(data.value_counts(discrete_vars),base=base)
    else:
        return _continuous.entropy_from_points(data,k=k,r=r,base=base)

def mutual_info(data,*mutual_vars,cvars=[],discrete_vars=[],base=2,k=3,r=None):
    data, df_discrete_vars = _utils.check_dataframe(data)
    if df_discrete_vars is not None:
        discrete_vars = df_discrete_vars
    cont_vars = [c for c in data.columns if not(c in discrete_vars)]
    all_vars = list(mutual_vars)+cvars

    if cont_vars:
        if discrete_vars and r is None:
            groupings = data.groupby(discrete_vars)
            indices = groupings.apply(lambda df:df.index)
            r_groups = groupings.apply(
                lambda df: _knn_utils.get_knn_distance(df[cont_vars],k=k,)
            )
            r = _np.zeros([data.shape[0]])
            for g in r_groups.index:
                r[indices[g]] = r_groups[g]
        elif r is None:
            r = _knn_utils.get_knn_distance(data,k=k,)
    
    all_vars = _np.array(list(mutual_vars)+cvars,dtype=object)
    n_vars = len(all_vars)
    combo_index = _utils.combination_index(mutual_vars,all_vars)
    coefficients = _utils.entropy_to_atoms_matrix(n_vars)[combo_index]
    pos_coefficients = (coefficients != 0)
    entropy_vars = [list(all_vars[a]) for a in _utils.atoms_to_variables_matrix(n_vars)[pos_coefficients].astype(bool)]
    entropies = _np.array([entropy(data[_utils.reduce_to_list(varlist)],base=base,r=r) for varlist in entropy_vars])
    return entropies.dot(coefficients[pos_coefficients])
