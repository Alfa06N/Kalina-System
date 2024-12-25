from DataBase.crud.product import getProductById, getProducts
from DataBase.crud.combo import getComboById, getCombos
from DataBase.crud.client import getClientById
from DataBase.crud.transaction import createTransactionWithoutCommit, createManyWithoutCommit
from DataBase.crud.sale import createSaleWithoutCommit, calculateSaleGain
from DataBase.crud.sale_product import createSaleProduct, createManySaleProducts
from DataBase.crud.sale_combo import createSaleCombo, createManySaleCombos
from exceptions import ErrorOperation
from config import getDB
from sqlalchemy.orm import Session
from DataBase.models import Sale, Transaction, SaleProduct, SaleCombo


class SaleMakerManager:
  def __init__(self):
    self.itemsSelector = None
    self.saleContainer = None
    
  def setItemSelector(self, itemsSelector):
    self.itemsSelector = itemsSelector
    
  def setSaleContainer(self, saleContainer):
    self.saleContainer = saleContainer
    
  def getSaleItems(self):
    if self.itemsSelector:
      return self.itemsSelector.getItemsWithQuantity()
    else:
      return None
    
  def validateAvailability(self):
    try:
      products, combos = self.getSaleItems()
        
      necessaryProducts = {}
        
      def addToList(idProduct, quantity):
        if idProduct in necessaryProducts:
          necessaryProducts[idProduct] += quantity
        else:
          necessaryProducts[idProduct] = quantity
        
      for product in products:
        idProduct = product["id"]
        quantity = product["quantity"]
        addToList(idProduct, quantity)
          
            
      for combo in combos:
        for product in combo["products"]:
          idProduct = product["id"]
          quantity = product["totalQuantity"]
          addToList(idProduct, quantity)
        
      with getDB() as db:
        for idProduct, quantity in necessaryProducts.items():
          product = getProductById(db, idProduct)
          print(f"Product: {product.name} - Quantity: {quantity}")
          availableQuantity = getProductById(db, idProduct).stock
            
          if quantity > availableQuantity:
            raise ErrorOperation(f"No hay suficiente stock del producto con \"{product.name}\". Disponible: {availableQuantity}, Necesario: {quantity}")
        
      return True, products, combos
    except:
      raise
  
  def makeSale(self, ciClient:int, idUser:int, price:float, payments:list=[], changes:list=[]):
    try:
      isValid, products, combos = self.validateAvailability()
      with getDB() as db:
        sale = createSaleWithoutCommit(
          db=db,
          totalPrice=price,
          gain=calculateSaleGain(products=products, combos=combos),
          ciClient=ciClient,
          idUser=idUser,
        )
        print(f"#{sale.idSale} Sale: \nPrice:{sale.totalPrice}$ / Gain:{sale.gain}")
        
        salePayments = createManyWithoutCommit(
          db=db,
          idSale=sale.idSale,
          transactions=payments,
        )
        
        saleChanges = createManyWithoutCommit(
          db=db,
          idSale=sale.idSale,
          transactions=changes,
        )
        
        for payment in salePayments:
          print(f"{payment.transactionType} - USD: {payment.amountUSD}$, VES: {payment.amountVES}Bs")
        for change in saleChanges:
          print(f"{change.transactionType} - USD: {change.amountUSD}$, VES: {change.amountVES}Bs")
        
        saleProducts = createManySaleProducts(
          db=db,
          products=products,
          idSale=sale.idSale,
        )
        saleCombos = createManySaleCombos(
          db=db,
          combos=combos,
          idSale=sale.idSale,
        )
        
        for register in saleProducts:
          print(f"Register: {getProductById(db, register.idProduct).name} - {register.productQuantity} {register.price}$")
        for register in saleCombos:
          print(f"Combo: {getComboById(db, register.idCombo).name} - {register.comboQuantity} {register.price}")
        
        return sale.idSale, salePayments, saleChanges, saleProducts, saleCombos
    except:
      raise
  
  def createSale(db, totalPrice: float, gain: float, ciClient: int, idUser:int):
    try:
      pass
    except:
      raise
      
saleMakerManager = SaleMakerManager()