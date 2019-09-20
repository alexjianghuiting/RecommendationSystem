import logging
import numpy as np
from Databaseinterface import DatabaseInterface

class Ranker(object):
    logging.basicConfig(level=logging.INFO)
    def __init__(self, numberToServe, database):
        self.numberToServe = numberToServe
        self.userHistoryDB = database.extract(DatabaseInterface.HISTORY_KEY)
        self.log = logging.getLogger(__name__)

    def _getUsedItems(self, userId):
        if userId == -1 :
            return set([])
        else:
            return set(self.userHistoryDB[self.userHistoryDB.loc[:,"user_id"]==userId].loc[:,"item_id"])

    def rerank(self, recommendationsTuple):
        userId = recommendationsTuple[0]
        recommendations = recommendationsTuple[1]
        usedItems = self._getUsedItems(userId)

        results = []

        if "online" in recommendations:
            results.extend(recommendations["online"][:self.numberToServe])
        if "offline" in recommendations:
            results.extend(recommendations["offline"][:self.numberToServe])
        if "popular" in recommendations:
            results.extend(recommendations["popular"][:self.numberToServe])
        else:
            self.log.error("No data served")

        try:
            results = np.random.choice(list(set(results) - usedItems), self.numberToServe, replace=False)
        except ValueError:
            results = np.random.choice(results, self.numberToServe, replace=False)
        return  results

if __name__ == '__main__':
    from Databaseinterface import DatabaseInterface
    db = DatabaseInterface("DATA")
    db.startEngine()
    ranker = Ranker(numberToServe=10, database=db)
    print(sorted(ranker._getUsedItems(1)))
