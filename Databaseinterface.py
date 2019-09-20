#just a simulation of database

import os
import pandas as pd
import logging

class DatabaseInterface(object):
    #1.log
    logging.basicConfig(level=logging.INFO)
    #2.import files
    HISTORY = "ratings.csv"
    USER_FEATURE = "userFeature.csv"
    ITEM_FEATURE = "itemFeature.csv"
    INVENTORY = "inventory.csv"
    #3.define keys
    HISTORY_KEY = "history"
    USER_FEATURE_KEY = "user_feature"
    ITEM_FEATURE_KEY = "item_feature"
    INVENTORY_KEY = "inventory"
    USER_ACTIVITY_KEY = "user_activity"
    #4.register the static database, name + path
    dbTable = {HISTORY_KEY: HISTORY,
			   USER_FEATURE_KEY: USER_FEATURE,
			   ITEM_FEATURE_KEY: ITEM_FEATURE,
			   INVENTORY_KEY: INVENTORY}

    def __init__(self,path):
        self.log = logging.getLogger(__name__)
        self.path = path
        self.started = False
        self.connTable = {}

    def startEngine(self):
        if self.started:
            self.log.warning("the database has already started")
        else:
            self.log.info("start the database engine...")
            #
            for tableName, tablePath in self.dbTable.items():
                self.log.info("loading table %s..."% tableName)
                #join root+tablePath
                #row by row
                self.connTable[tableName] = pd.read_csv(os.path.join(self.path,tablePath), index_col=0)

            self.log.info("creating table user_activity...")
            #rating的数量groupby userid
            #不能用string, immutable
            self.connTable[self.USER_ACTIVITY_KEY] = self.connTable["history"].groupby("user_id").size()
            #actually a series

            self.log.info("database successfully started")
            self.started = True
    #extract the database
    def extract(self, tableName):
        return (self.connTable[tableName])

    def putAction(self, action):
        insertRow(self.connTable["history"], [action.userId, action.itemId, action.rating])

def insertRow(df,row):
    #len(df) = 有多少行
    df.loc[len(df)]=row

if __name__ == '__main__':
    connector = DatabaseInterface("DATA")
    connector.startEngine()
