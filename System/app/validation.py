import flet as ft
import time
import constants
import exceptions
from config import getDB
from DataBase.crud.employee import getEmployeeById
import re

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
  validateField(field, lambda value: len(value.strip()) > 0 and not any(char.isdigit() for char in value))

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

def evaluateForm(username=[], name=[], password=[], ci=[], numbers=[], others=[]):
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
      
  for field in name:
    if len(field.value.strip()) == 0:
      field.error_text = "El nombre no puede estar vacío"
      field.update()
      isValid = False
    elif any(char.isdigit() for char in field.value):
      field.error_text = "El campo no puede contener dígitos"
      field.update()
      isValid = False
  
  for field in password:
    if len(field.value) < 8:
      field.error_text = "La contraseña debe tener al menos 8 caracteres"
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