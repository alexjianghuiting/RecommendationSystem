#take user actions
#use simiarity model

from ModelStore import ModelStore
from Databaseinterface import DatabaseInterface
import logging

class OnlineLearner(object):
    logging.basicConfig(level=logging.INFO)

    def __init__(self, database, modelStore):
        self.database = database
        self.modelStore = modelStore
        self.log = logging.getLogger(__name__)

    def trainModel(self, action):
        # action was defined in WebServer, has userId, itemId, and rating
        userId = action.userId
        itemId = action.itemId
        rating = action.rating
        model = self.modelStore.getModel(ModelStore.SI_MODEL_KEY, userId)
        itemFeatureTable = self.database.extract(DatabaseInterface.ITEM_FEATURE_KEY)
        itemFeature = itemFeatureTable.loc[itemId, "unknown":]
        model.train(itemFeature, rating)
        self.pushModel(model, userId)

    def pushModel(self, model, userId):
        self.modelStore.setModel(model, ModelStore.SI_MODEL_KEY, userId)

