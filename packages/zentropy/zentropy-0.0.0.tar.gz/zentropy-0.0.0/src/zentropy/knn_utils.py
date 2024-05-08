from sklearn.neighbors import NearestNeighbors as _NearestNeighbors, KDTree as _KDTree
import numpy as _np

def get_knn_distance(xs,k=3,metric="chebyshev",**knn_kwargs):
    nn = _NearestNeighbors(metric=metric,n_neighbors=k,**knn_kwargs)
    nn.fit(xs)
    radii = _np.nextafter(nn.kneighbors()[0][:,-1],0)
    return radii

def count_proper_neighbors(xs,radii,ys=None,metric="chebyshev",**kdtree_kwargs):
    sub = 0
    if ys is None:
        ys = xs
        sub = 1

    kd = _KDTree(ys,metric=metric,**kdtree_kwargs)
    return kd.query_radius(xs,radii,return_distance=False,count_only=True) - sub

def get_neighbors(xs,radii,ys=None,metric="chebyshev",**kdtree_kwargs):
    if ys is None:
        ys = xs

    kd = _KDTree(ys,metric=metric,**kdtree_kwargs)
    return kd.query_radius(xs,radii,return_distance=False,)



