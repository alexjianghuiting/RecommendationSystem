#group items with similar features
from sklearn.cluster import KMeans

class ClusteringModel():
    def __init__(self, n_cluster=10):
        self.model = KMeans(n_cluster, random_state=1234)
        self.groups = {} #keyed by cluster index and values are itemId's
        self.trained = False

    def train(self, itemFeatureTable):
        self.indices = itemFeatureTable.index
        self.model.fit(itemFeatureTable)
        self.labels = self.model.labels_
        for k,v in zip(self.labels, itemFeatureTable.index.tolist()):
            self.groups.setdefault(k,[]).append(v)
        self.trained = True

    def predict(self, itemFeatureTable):
        centers = self.model.predict(itemFeatureTable)
        return centers, [self.groups[c] for c in centers]

