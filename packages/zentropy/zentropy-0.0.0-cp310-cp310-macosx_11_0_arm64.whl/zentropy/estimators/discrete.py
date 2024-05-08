from scipy.special import digamma as _digamma, betainc as _betainc, beta as _beta
import numpy as _np
import zentropy.estimators.utils as _utils

def surprisal_from_counts(counts,base=2,p_estimate=0,eps=1e-8):
    N = counts.sum()
    bias_correction = _betainc(N+1,eps,p_estimate)*_beta(N+1,eps)
    return (_digamma(N+1) - _digamma(counts+1) + bias_correction)/_np.log(base)

def weighted_surprisal_from_counts(counts,base=2,p_estimate=0,eps=1e-8):
    N = counts.sum()
    n_psi_ns = _np.empty_like(counts)
    n_psi_ns[counts==0] = 0
    n_psi_ns[counts>0] = counts*_digamma(counts)
    bias_correction = _betainc(N,eps,p_estimate)*_beta(N,eps)
    return ((_digamma(N) + bias_correction)*counts - n_psi_ns)/(N*_np.log(base))

def entropy_from_counts(p_counts,q_counts=None,base=2,**surprisal_kwargs):
    if q_counts is None:
        return weighted_surprisal_from_counts(p_counts,base=base,p_estimate=0,**surprisal_kwargs).sum()
    else:
        return (p_counts*surprisal_from_counts(q_counts,base=base,**surprisal_kwargs)).sum()/p_counts.sum()
