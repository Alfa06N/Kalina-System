from sqlalchemy.orm import Session 
from DataBase.models import Recovery
from DataBase.errorHandling import handleDatabaseErrors
from sqlalchemy.exc import SQLAlchemyError

def createRecovery(db: Session, questionOne: str, answerOne: str, questionTwo: str, answerTwo: str, idUser: int):
  try:
    recovery = Recovery(
      questionOne=questionOne,
      answerOne=answerOne,
      questionTwo=questionTwo,
      answerTwo=answerTwo,
      idUser=idUser
    )
    
    def func():
      db.add(recovery)
      db.commit()
    
    handleDatabaseErrors(db, func)
    
    db.refresh(recovery)
    return recovery
  except Exception as e:
    raise
    
def getRecoveryByUserId(db: Session, idUser: int):
  try:
    def func():
      return db.query(Recovery).filter(Recovery.idUser == idUser).first()
    
    return handleDatabaseErrors(db, func)
    
  except Exception as e:
    raise
  
def updateRecovery(db, idUser, questionOne, answerOne, questionTwo, answerTwo):
  try:
    def func():
      return db.query(Recovery).filter(Recovery.idUser).first()
    
    recovery = handleDatabaseErrors(db, func)
    
    if not recovery:
      print("Recovery not found")
      return None
    
    if questionOne:
      recovery.questionOne = questionOne
    if answerOne:
      recovery.answerOne = answerOne
    if questionTwo:
      recovery.questionTwo = questionTwo
    if answerTwo:
      recovery.answerTwo = answerTwo
    
    db.commit()
    db.refresh(recovery)
    return recovery
  
  except SQLAlchemyError as e:
    return None
  
def removeRecovery(db, idUser):
  try:
    def func():
      recovery = db.query(Recovery).filter(Recovery.idUser)
      
      if not recovery:
        print("Recovery not found")
        return None
      else:
        db.delete(recovery)
        return recovery
    
    recovery = handleDatabaseErrors(db, func)
    
    db.commit()
    return recovery
  except Exception as e:
    return None