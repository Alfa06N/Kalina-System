from DataBase.crud.user import getUserByUsername
import constants
from config import getDB
import flet as ft

currentUser = None

def setUser(user):
  global currentUser
  currentUser = user

def getCurrentUser():
  return currentUser

def clearCurrentUser():
  global currentUser
  currentUser = None
  
  
def isAdmin():
  with getDB() as db:
    return getUserByUsername(db, getCurrentUser()).role == "Administrador"