import flet as ft
from exceptions import InvalidData, DataNotFoundError, DataAlreadyExists
  
class ExchangeRateManager:
  def __init__(self):
    self.subscribers = []
    self.currentRate = None
    
  def setRate(self, rate):
    self.currentRate = rate
    self.notifySubscribers()
    return self.currentRate
  
  def getRate(self):
    return self.currentRate
  
  def clearRate(self):
    self.currentRate = None
  
  def clearSubscribers(self):
    self.subscribers = []
  
  def subscribe(self, container):
    self.subscribers.append(container)
    
  def notifySubscribers(self):
    try:
      for container in self.subscribers:
        container.updateAboutRate(self.currentRate)
    except Exception as err:
      print(err)

# What is supposed to be imported
exchangeRateManager = ExchangeRateManager()