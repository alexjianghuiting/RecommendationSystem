#highest score with most of the users

class MostPopularModel():
    Freq = 0.001

    def __init__(self):
        pass
    def train(self,history):
        itemID = list(history)[1]
        ratings = list(history)[2]
        nLimit = int(history.shape[0]*self.Freq)
        itemRatingGrouped = history.groupby(itemID)
        itemRatingGroupedCount = itemRatingGrouped[ratings].count()
        self.mostPopular = itemRatingGrouped[ratings].mean()[itemRatingGroupedCount>nLimit].sort_values(ascending=False)

    def predict(self,X):
        return [self.mostPopular.index.get_loc(x) for x in X]
    def provideRec(self):
        return self.mostPopular.index.tolist()
