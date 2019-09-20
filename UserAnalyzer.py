class UserAnalyzer(object):
    def __init__(self):
        pass

    #groupby.size
    def analyzer(self, request, userActivityDB):
        if isinstance(request.userId, str):
            return ["anonymous", -1, request]
        else:
            if userActivityDB[request.userId] >= 30:
                return ["old", request.userId, request]
            else:
                return ["new", request.userId, request]

    def analyzeAction(self, action):
        if isinstance(action.userId, str):
            return "anonymous"
        else:
            return "registered"
