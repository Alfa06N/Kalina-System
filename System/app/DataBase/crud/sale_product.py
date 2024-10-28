from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from DataBase.models import SaleProduct
from DataBase.errorHandling import handleDatabaseErrors
from DataBase.crud.product import getProductById, calculatePrice
from DataBase.crud.sale import getSaleById
from exceptions import DataAlreadyExists, DataNotFoundError, InvalidData

def createSaleProduct(db: Session, idSale: int, idProduct: int, productQuantity: int, price: float):
  try:
    record = SaleProduct(
      idSale=idSale,
      idProduct=idProduct,
      productQuantity=productQuantity,
      price=price
    )
    
    def func():
      db.add(record)
      db.commit()
      
    handleDatabaseErrors(db, func)
    
    updatedProduct = updateProductStock(
      db=db,
      idProduct=idProduct,
      quantity=productQuantity,
    )
    db.refresh(record)
    return record
  except Exception:
    raise

def createManySaleProducts(db:Session, products, idSale:int):
  try:
    productsList = []
    for product in products:
      saleProduct = createSaleProduct(
        db=db,
        idSale=idSale,
        idProduct=product["id"],
        productQuantity=product["quantity"],
        price=product["price"],
      )
      productsList.append(saleProduct)
    return productsList
  except:
    raise
  
def updateProductStock(db: Session, idProduct, quantity: int):
  try:
    product = getProductById(db, idProduct)
    
    def func():
      product.stock -= quantity
      db.commit()
    
    handleDatabaseErrors(db, func)
    db.refresh(product)
    return product
  except:
    raise
  
def getAllSaleProduct(db: Session):
  try:
    def func():
      return db.query(SaleProduct).all()
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def getSaleProductById(db: Session, idSaleProduct):
  try:
    def func():
      return db.query(SaleProduct).filter(SaleProduct.idSaleProduct == idSaleProduct).first()
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def removeAllSaleProduct(db: Session):
  try:
    def func():
      db.query(SaleProduct).delete()
      db.commit()
    
    handleDatabaseErrors(db, func)
    return True
  except Exception:
    raise