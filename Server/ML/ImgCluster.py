import numpy as np
from sklearn.cluster import DBSCAN
from collections import defaultdict

def cluster_images(X,file_paths,eps=0.5,min_samples=2):
    model=DBSCAN(eps=eps,min_samples=min_samples,metric='cosine')
    clusters=model.fit_predict(X)
    groups=defaultdict(list)
    for label,img in zip(clusters,file_paths):
        if label==-1:
            groups['noise'].append(img)
        else:
            groups[f"label {label}"].append(img)
    return groups
