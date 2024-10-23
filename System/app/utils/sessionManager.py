currentUser = None

def setUser(user):
  global currentUser
  currentUser = user

def getCurrentUser():
  return currentUser

def clearCurrentUser():
  global currentUser
  currentUser = None