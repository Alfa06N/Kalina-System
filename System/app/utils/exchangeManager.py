import flet as ft
from exceptions import InvalidData, DataNotFoundError, DataAlreadyExists

currentRate = None

def setRate(rate):
  global currentRate
  currentRate = rate
  print(f"Tasa de cambio establecida: {currentRate}")

def getCurrentRate():
  return currentRate

def clearCurrentRate():
  global currentRate
  currentRate = None