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
  
def verifyPermission(page):
  from Modules.customControls import CustomAlertDialog
  with getDB() as db:
    user = getUserByUsername(db, currentUser)
    print(user.username)
    if not user.role == "Administrador":
      print("Acceso denegado")
      dialog = CustomAlertDialog(
        title="Acceso denegado",
        content=ft.Text(
          value="No tienes acceso a esta función porque no eres un usuario administrador.",
          size=18,
          color=constants.BLACK,
        ),
        modal=False,
        
      )
      page.open(dialog)
      return False
    
    return True