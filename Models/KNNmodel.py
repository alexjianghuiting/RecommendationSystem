#KNN model
#for new user, using user feature, find k nearest users, using their ratings for the recommendation

import numpy as np
from sklearn.neighbors import NearestNeighbors

class KNNmodel():
    def __init__(self):
        self.knnModel = None

    def train(self, userFeatureTable, ratingsMat):
        userFeatureTable.loc[:,"age"] = userFeatureTable.loc[:, "age"]/10.
        self.knnModel = NearestNeighbors(n_neighbors=10,algorithm='ball_tree').fit(userFeatureTable)
       
        self.ratingsMat = ratingsMat
        self.userFeatureTable = userFeatureTable
        self.userIds = self.userFeatureTable.index

    def predict(self, userFeatureTable):
        distances, indices = self.knnModel.kneighbors(userFeatureTable)
        return self.userIds[indices[0]]

    def provideRec(self, userId):

        userIds = self.predict(self.userFeatureTable.loc[userId].as_matrix().reshape(1,-1))
        userIds = np.array(list(set(userIds) - set([userId])))
        return self.ratingsMat[userIds-1].mean(axis=0).argsort()[::-1]+1

if __name__ == '__main__':
        from Databaseinterface import DatabaseInterface
