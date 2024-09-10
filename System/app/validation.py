import flet as ft
import time
import constants
import exceptions
from config import getDB
from DataBase.crud.employee import getEmployeeById

def validateField(field, condition):
  
  if not field.error_text == None and condition(field.value):
    field.error_text = None
    field.focused_border_color = constants.BLACK
    field.update()
  
  return condition(field.value)

def validateUsername(field):
  validateField(field, lambda value: len(value) > 0)

def validatePassword(field):
  validateField(field, lambda value: len(value) >= 8)
  
def validateCI(field):
  validateField(field, lambda value: len(value) > 6 and len(value) < 9)
  
def validateEmptyField(field):
  validateField(field, lambda value: len(value) > 0)

def evaluateForm(username=[], password=[], ci=[], others=[]):
  isValid = True
  for field in username:
    if len(field.value) == 0:
      field.error_text = "El nombre de usuario no puede estar vacío"
      field.update()
      isValid = False
  
  for field in password:
    if len(field.value) < 8:
      field.error_text = "La contraseña debe tener al menos 8 caracteres"
      field.update()
      isValid = False
  
  for field in ci:
    if len(field.value) < 7 or len(field.value) > 9:
      field.error_text = "Número fuera de rango"
      field.update()
      isValid = False
  
  for field in others:
    if field.value == None or len(field.value) == 0:
      field.error_text = "Este campo no puede estar vacío"
      field.update()
      isValid = False
  
  # print("Campos válidos")
  print(isValid)
  return isValid

def queryUserData(db, username, password):
  from DataBase.crud.user import getUserByUsername
  
  try:
    user = getUserByUsername(db, username)
      
    if user:
      return user.password == password
    else:
      raise exceptions.UserNotFoundError()
  except Exception as e:
    print(f"Error: {e}")
  except exceptions.UserNotFoundError:   
    raise