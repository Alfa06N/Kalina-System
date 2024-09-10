currentUser = None

def setUser(user):
  global currentUser
  currentUser = user
  print(f"{user} ha iniciado sesión")

def getCurrentUser():
  return currentUser

def clearCurrentUser():
  global currentUser
  currentUser = None