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
      with getDB() as db:
        recentlyAdded = []
        products = getLowStockProducts(db)

        if not products:
          self.clearList()
          return self.lowStockProducts

        for product in products:
          if not product.idProduct in self.lowStockProducts:
            recentlyAdded.append(product.idProduct)
            self.lowStockProducts.append(product.idProduct)
          
        return self.lowStockProducts
    except:
      raise
      
  def clearList(self):
    self.lowStockProducts = []
    
inventoryManager = InventoryManager()
inventoryManager.checkLowStock()
