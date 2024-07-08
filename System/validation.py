import flet as ft
import time
import constants

def validateField(field, condition, errorMessage):
  
  if not field.error_text == None and condition(field.value):
    field.error_text = None
    field.focused_border_color = constants.ORANGE_LIGHT
    field.update()
  
  return condition(field.value)

def validateUsername(field):
  validateField(field, lambda value: len(value) > 0, "El nombre de usuario no puede estar vacío")

def validatePassword(field):
  validateField(field, lambda value: len(value) >= 8, "La contraseña debe tener al menos 8 caracteres")

def evaluateForm(username=list, password=list):
  for field in username:
    if len(field.value) == 0:
      field.error_text = "El nombre de usuario no puede estar vacío"
      field.update()
      return False
  
  for field in password:
    if len(field.value) < 8:
      field.error_text = "La contraseña debe tener al menos 8 caracteres"
      field.update()
      return False
  
  return True