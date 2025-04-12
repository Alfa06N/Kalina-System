from datetime import datetime
from config import getDB
from DataBase.crud.product import getLowStockProducts

class InventoryManager:
  def __init__(self):
    self.lowStockProducts = []

  def getProducts(self):
    return self.lowStockProducts

  def checkLowStock(self):
    try:
      self.clearList()
      with getDB() as db:
        recentlyAdded = []
        products = getLowStockProducts(db)

        if not products:
          self.clearList()
          return self.lowStockProducts, len(recentlyAdded) > 0

        for product in products:
          if not product.idProduct in self.lowStockProducts:
            recentlyAdded.append(product.idProduct)
            self.lowStockProducts.append(product.idProduct)
          
        return self.lowStockProducts, len(recentlyAdded) > 0
    except:
      raise
      
  def clearList(self):
    self.lowStockProducts = []
    
inventoryManager = InventoryManager()
inventoryManager.checkLowStock()
