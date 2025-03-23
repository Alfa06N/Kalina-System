import flet as ft
import time
import constants
import exceptions
from config import getDB
from DataBase.crud.employee import getEmployeeById
import re
import string

def validateField(field, condition):
  
  try:
    if not field.error_text == None and condition(field.value.strip()):
      field.error_text = None
      field.focused_border_color = constants.BLACK
      field.update()
    
    return condition(field.value)
  except ValueError as err:
    print(err)
    pass
  
def validateName(field):
  onlychars = string.ascii_letters
  validateField(field, lambda value: len(value.strip()) > 0 and any(char not in onlychars for char in value))

def validateUsername(field):
  validateField(field, lambda value: len(value.strip()) > 0 and not value.strip()[0].isdigit())

def validatePassword(field):
  validateField(field, lambda value: len(value) >= 8)
  
def validateCI(field):
  validateField(field, lambda value: len(value.strip()) > 6 and len(value.strip()) < 9)

def validateNumber(field):
  validValue = re.sub(r"[^-?\d.]", "", field.value)
  
  if validValue.count(".") > 1:
    validValue = validValue.replace(".", "", validValue.count(".") - 1)
    
  if field.value != validValue:
    field.value = validValue
    field.update()
  
  validateField(field, lambda value: float(value) > 0)
  
def validateEmptyField(field):
  validateField(field, lambda value: len(value.strip()) > 0)

def evaluateForm(username=[], name=[], price=[], password=[], ci=[], numbers=[], others=[]):
  isValid = True
  for field in username:
    if len(field.value.strip()) == 0:
      field.error_text = "El nombre de usuario no puede estar vacío"
      field.update()
      isValid = False
    elif field.value.strip()[0].isdigit():
      field.error_text = "El nombre de usuario no puede empezar con dígitos"
      field.update()
      isValid = False
    elif len(field.value.strip()) > 25:
      field.error_text = "Límite de caracteres excedido"
      field.update()
      isValid = False
      
  for field in price:
    if not validatePriceField(field):
      isValid = False
      
  for field in name:
    onlychars = string.ascii_letters + " áéíóúÁÉÍÓÚñÑ"
    if len(field.value.strip()) == 0:
      field.error_text = "El nombre no puede estar vacío"
      field.update()
      isValid = False
    elif any(char not in onlychars for char in field.value):
      field.error_text = "El campo solo puede contener letras"
      field.update()
      isValid = False
    elif len(field.value.strip()) > 25:
      field.error_text = "Límite de caracteres excedido"
      field.update()
      isValid = False
  
  for field in password:
    symbols = string.punctuation
    if len(field.value) < 8:
      field.error_text = "La contraseña debe tener al menos 8 caracteres"
      field.update()
      isValid = False
    elif not any(char.isupper() for char in field.value):
      field.error_text = "La contraseña debe tener mínimo una letra mayúscula"
      field.update()
      isValid = False
    elif not any(char.islower() for char in field.value):
      field.error_text = "La contraseña debe tener mínimo una letra minúscula"
      field.update()
      isValid = False
    elif not any(char.isdigit() for char in field.value):
      field.error_text = "La contraseña debe tener mínimo un número"
      field.update()
      isValid = False
    elif not any(char in symbols for char in field.value):
      field.error_text = "La contraseña debe tener al menos un símbolo"
      field.update()
      isValid = False
    elif len(field.value.strip()) > 25:
      field.error_text = "Límite de caracteres excedido"
      field.update()
      isValid = False

  for field in ci:
    if len(field.value.strip()) < 7 or len(field.value.strip()) > 9:
      field.error_text = "Número fuera de rango"
      field.update()
      isValid = False
  
  for field in others:
    if field.value == None or len(field.value.strip()) == 0:
      field.error_text = "Este campo no puede estar vacío"
      field.update()
      isValid = False
    elif len(field.value.strip()) > 50:
      field.error_text = "Límite de caracteres excedido"
      field.update()
      isValid = False
  
  for field in numbers:
    try:
      if float(field.value) <= 0:
        field.error_text = "Este valor debe ser mayor a 0"
        field.update()
        isValid = False
    except ValueError:
      field.error_text = "Debe ingresar un valor numérico válido"
      field.update()
      isValid = False
  # print("Campos válidos")
  print(isValid)
  return isValid

def validatePriceField(field):
  try:
    isValid = True
    if float(field.value) == 0:
      showErrorMessage(field, f"Este campo no puede estar vacío")
      isValid = False
    else:
      value = float(field.value)
      if value < 0:
        showErrorMessage(field, f"El campo no acepta valores negativos")
        isValid = False
      elif value == 0:
        showErrorMessage(field, f"El campo no puede estar en 0")
        isValid = False
        
      elif not (0 <= value < 10**7 and len(str(value).split(".")[-1]) <= 3):
        showErrorMessage(field, f"El campo debe tener hasta 7 dígitos enteros y 3 decimales")
        isValid = False
      return isValid
  except ValueError:
    showErrorMessage(field, "Debe ingresar un valor numérico válido")
    isValid = False
  except Exception as err:
    print(f"Error validando costos: {err}")

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
  
def showErrorMessage(field, message):
  field.error_text = message
  field.update()