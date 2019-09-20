#user-based, item-based similarity
#only use rating matrix
# Collaborative filtering model

import numpy as np
from sklearn.neighbors import NearestNeighbors
import logging

class CFmodel():
    RARECASE = 5
    logging.basicConfig(level=logging.INFO)

    def __init__(self):
        self.knnModel = NearestNeighbors(n_neighbors=15)
        self.log = logging.getLogger(__name__)

    #svd提取主要特征 只取矩阵的前几行
    def _CFSVD(self,ratingsMat):
        user_ratings_mean = np.mean(ratingsMat,axis=1) #列
        #1.demean the rating matrix
        R_demean = ratingsMat - user_ratings_mean.reshape(-1,1)
        from scipy.sparse.linalg import svds
        #2.svd the demeaned rating matrix 提取重要特征
        U, sigma, Vt = svds(R_demean, k=10)
        sigma = np.diag(sigma)
        #3.dot the svd + mean rating matrix = completed rating matrix
        self.complete_rating_matrix = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)

    #不应该用complete的rating matrix来train吗？
    def train(self, ratingMat, itemFeatureTable):
        indices = itemFeatureTable.index #index从1开始
        self.knnModel.fit(itemFeatureTable) #item-based: feature similarity
        assert(ratingMat.shape[1] == itemFeatureTable.index.max())
        rareCases = np.where((ratingMat>0).sum(axis=0) < self.RARECASE)[0] #the row where ratings are less than 5

        #do not do action on your original data
        ratingMatFinal = ratingMat.copy()
        count = 0
        #predict每个item的rating
        #针对rarecase
        for case in rareCases:
            if case+1 in itemFeatureTable.index:
                features = itemFeatureTable.loc[case+1]
                neighbors = self.knnModel.kneighbors(features.values.reshape(1,-1), return_distance=False)[0]
                neighborPos = indices[neighbors]-1 #ratingMat index从0开始
                target_count = (ratingMat[:,neighborPos] > 0).sum(axis=1)
                target_ratings = ratingMat[:,neighborPos].sum(axis=1).astype(float)/target_count

                for i in range(ratingMat.shape[0]):
                    if ratingMat[i,case] == 0 and target_count[i]>10:
                        if target_ratings[i]!=0:
                            ratingMatFinal[i,case] = target_ratings[i]
                            count += 1
        #补全 补全之后提取出大致方向
        self._CFSVD(ratingMatFinal)
    def predict(self,userId):
        return self.complete_rating_matrix[userId-1]
    def provideRec(self,userId):
        return self.complete_rating_matrix[userId-1].argsort()[::-1]+1 #??
