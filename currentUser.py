



class currentUser():

    def __init__(self):
        self.userDict = dict(user = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjNmNjcyNDYxOTk4YjJiMzMyYWQ4MTY0ZTFiM2JlN2VkYTY4NDZiMzciLCJ0eXAiOiJKV1QifQ')

    def updateUser(self, newUser):
        self.userDict['user'] = newUser

    def getUser(self):
        return self.userDict['user']