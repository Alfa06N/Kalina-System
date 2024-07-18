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
  
def validateCI(field):
  validateField(field, lambda value: len(value) > 6 and len(value) < 9, "Número fuera de rango")

def evaluateForm(username=list, password=list, ci=list):
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
  
  
  return isValid