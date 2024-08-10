from sqlalchemy.orm import Session
from DataBase.models import Product

from DataBase.errorHandling import handleDatabaseErrors
from sqlalchemy.exc import SQLAlchemyError
from exceptions import DataNotFoundError

def createProduct(db: Session, name: str, description: str, stock: int, minStock: int, cost: float, gain: float, iva: float, idCategory: int ):
  pass