import numpy as np
from sklearn.cluster import DBSCAN
from collections import defaultdict
from sklearn.decomposition import PCA
from sklearn.preprocessing import Normalizer

def tune_eps(old_eps,Feedback_uniqueness,alpha=0.005):
    old_eps=old_eps
    uniqueness=Feedback_uniqueness
    change_required=3.5-uniqueness
    new_eps=alpha*change_required+(1-alpha)*old_eps
    return new_eps

def cluster_images(X,file_paths,eps=1.1,min_samples=2):
    #n=X.shape[0]
    '''scale=Normalizer()
    X_scaled=scale.fit_transform(X)
    X=X_scaled
    if n>10:
        pca=PCA(n_components=0.8)
        try:
            X=pca.fit_transform(X_scaled)
        except:
            pass
    '''
    model=DBSCAN(eps=eps,min_samples=min_samples,metric='cosine')
    clusters=model.fit_predict(X)
    groups=defaultdict(list)
    for label,img in zip(clusters,file_paths):
        if label==-1:
            groups['noise'].append(img)
        else:
            groups[f"label {label}"].append(img)
    return groups
