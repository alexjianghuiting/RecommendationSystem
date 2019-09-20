#read in user history data

from ModelStore import ModelStore
from Databaseinterface import DatabaseInterface
import logging
import numpy as np

class OfflineLearner(object):
    logging.basicConfig(level=logging.INFO)

    #database, modelStore, modelRegister
    def __init__(self, database, modelStore):
        self.database = database
        self.modelStore = modelStore
        self.log = logging.getLogger(__name__)
        self.modelRegistry = [(ModelStore.KNN_MODEL_KEY, "k nearest neighbor most popular model"),
                              (ModelStore.MP_MODEL_KEY, "most popular item model"),
                              (ModelStore.CL_MODEL_KEY, "item feature clustering model"),
                              (ModelStore.CL_MODEL_KEY, "collaborative filtering model")]


    def trainModel(self):
        self.log.info("start offline training...")
        #extract the data by using keys
        historyRating = self.database.extract(DatabaseInterface.HISTORY_KEY)
        itemFeatureTable = self.database.extract(DatabaseInterface.ITEM_FEATURE_KEY).loc[:, "unknown":]
        userFeatureTable = self.database.extract(DatabaseInterface.USER_FEATURE_KEY).loc[:, "age":]
        ratingMat = self.transformToMat(historyRating)

        #update the model
        for record in self.modelRegistry:
            model = self.modelStore.getModel(record[0])
            self.log.info("training %s" %record[1])
            if record[0] == ModelStore.KNN_MODEL_KEY:
                model.train(userFeatureTable, ratingMat)
            elif record[0] == ModelStore.MP_MODEL_KEY:
                model.train(historyRating)
            elif record[0] == ModelStore.CL_MODEL_KEY:
                model.train(itemFeatureTable)
            #协同过滤 rating+itemFeature
            elif record[0] == ModelStore.CF_MODEL_KEY:
                model.train(ratingMat, itemFeatureTable)
            else:
                raise Exception("no model is found")

            self.log.info("update %s", record[1])
            self.pushModel(model, record[0])

    def pushModel(self, model, key):
        self.modelStore.setModel(model, key)

    @staticmethod
    def transformToMat(historyRating):
        users = historyRating.user_id.max()
        items = historyRating.item_id.max()
        ratingMat = np.zeros([users, items])
        for r in historyRating.itertuples():
            ratingMat[r[1]-1,r[2]-1] = r[3]
        return ratingMat



