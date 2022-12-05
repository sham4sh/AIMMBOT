


#Store data that needs to be passed between windows
class currentData():

    def __init__(self):
        self.userDict = dict(user = 'default')
        self.keywordDict = dict(keyword = 'default')

    def updateUser(self, newUser):
        self.userDict['user'] = newUser

    def getUser(self):
        return self.userDict['user']

    def updateKeyword(self, newKeyword):
        self.keywordDict['keyword'] = newKeyword

    def getKeyword(self):
        return self.keywordDict['keyword']