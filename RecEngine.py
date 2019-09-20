from ModelStore import ModelStore
import logging

class RecEngine(object):
    logging.basicConfig(level=logging.INFO)

#变量小写开头
    def __init__(self, userAnalyzer, modelStore, userActivityTable):
        self.userAnalyzer = userAnalyzer
        self.modelStore = modelStore
        self.userActivityTable = userActivityTable
        self._cacheMostPopular()
        self.log = logging.getLogger(__name__)

    def resetCache(self):
        self._cacheMostPopular()

    def _cacheMostPopular(self):
        #得到rec -> 调用model + provideRec方法
        self.mostPopular = self.modelStore.getModel(ModelStore.MP_MODEL_KEY).provideRec()

    def provideRec(self, request):
        rec = {}
        rec["popular"] = self.mostPopular
        requesAnalyzed = self.userAnalyzer.analyzer(request, self.userActivityTable)

        #online rec
        onlineRec = self.modelStore.getModel(ModelStore.SI_MODEL_KEY, request.userId).provideRec()

        if len(onlineRec)>0:
            rec["online"] = onlineRec
            #如果是self call的话 函数里第一个para self就省略不写
        if requesAnalyzed[0] == "new":
            rec["offline"] = self.modelStore.getModel(ModelStore.KNN_MODEL_KEY).provideRec(requesAnalyzed[1])
        elif requesAnalyzed[0] == "old":
            rec["offline"] = self.modelStore.getModel(ModelStore.CF_MODEL_KEY).provideRec(requesAnalyzed[1])

        return requesAnalyzed[1],rec
