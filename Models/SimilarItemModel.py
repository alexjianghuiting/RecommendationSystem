class SimilarItemModel():
    LOWEST = 3.0

    def __init__(self, clusteringModel):
        self.clusteringModel = clusteringModel
        self.recs = []

    def train(self, itemFeatureTable, rating):
        indices = [[]]
        indices[0] = predict(self, itemFeatureTable)

        if rating >= self.LOWEST:
            self.recs = indices[0]
        else:
            self.recs = []
    def provideRec(self):
        return self.recs
def predict(self, itemFeatureTable):
    itemFeature = itemFeatureTable.values.reshape(1,-1)
    center, indices = self.clusteringModel.predict(itemFeature)
    return indices[0]

