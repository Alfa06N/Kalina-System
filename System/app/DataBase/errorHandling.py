from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def handleDatabaseErrors(db: Session, func):
  try:
    return func()
  except SQLAlchemyError as e:
    db.rollback()
    print(f"Database Error: {e}")
    raise
  except IntegrityError as e:
    db.rollback()
    print(f"Integrity Error: {e}")
    raise
  except ValueError as e:
    db.rollback()
    print(f"Value Error: {e}")
    raise
  except Exception as e:
    db.rollback()
    print(f"Unexpected Error: {e}")
    raise
  # finally:
  #   db.close()