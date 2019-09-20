#all the api, all the functions
import logging

from Databaseinterface import DatabaseInterface
from RecEngine import RecEngine
from Ranker import Ranker
from Learners.OfflineLearner import OfflineLearner
from Learners.OnlineLearner import OnlineLearner
from UserAnalyzer import UserAnalyzer
from ModelStore import ModelStore

class Request(object):
    def __init__(self, userId):
        self.userId = userId
    def __str__(self):
        return "request from: "+str(self.userId)
class Action(object):
    def __init__(self, userId, itemId, rating):
        self.userId = userId
        self.itemId = itemId
        self.rating = rating
    def __str__(self):
        return "user: %s, item: %s, rating: %s" %(self.userId, self.itemId, self.rating)

class WebServer(object):
    logging.basicConfig(level=logging.INFO)

    #configMap is in main
    def __init__(self, configMap):
        self.db = DatabaseInterface(configMap['data_dir'])
        self.numberToServe = configMap['numberToServe']
        self.log = logging.getLogger(__name__)
        #要用key idk why, why not a direct string?

    #initialize everything
    def start(self):
        self.db.startEngine()
        self.ranker = Ranker(self.numberToServe, self.db)
        self.userAnalyzer = UserAnalyzer()
        self.modelStore = ModelStore()
        self.offlineLearner = OfflineLearner(self.db, self.modelStore)
        self.onlineLearner = OnlineLearner(self.db, self.modelStore)
        #so that immediately after we start, we can start to give recommendations
        self.offlineLearner.trainModel()
        #had to extract it here
        self.recEngine = RecEngine(self.userAnalyzer, self.modelStore, self.db.extract(DatabaseInterface.USER_ACTIVITY_KEY))

    def getAction(self, action):
        assert (isinstance(action, Action))
        self.onlineLearner.trainModel(action)
        actionType = self.userAnalyzer.analyzeAction(action)
        if actionType == "registered":
            self.db.putAction(action)

    def provideRec(self, request):
        assert (isinstance(request, Request))
        rec = self.recEngine.provideRec(request)
        recReRanked = self.ranker.rerank(rec)
        return recReRanked

    def renderRec(self, request):
        assert(isinstance(request, Request))
        recReRanked = self.provideRec(request)
        return self.db.extract(DatabaseInterface.INVENTORY_KEY).loc[recReRanked].sort_index()

    def increment(self):
        #offline, online, recengine(find the new most popular one)
        self.offlineLearner.trainModel()
        self.modelStore.cleanOnlineModel()
        self.recEngine.resetCache()

    def getFromInventory(self, itemId):
        return self.db.extract(DatabaseInterface.INVENTORY_KEY).loc[itemId]





