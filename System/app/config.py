import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Obtener la URL
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
  raise ValueError("No se ha encontrado la URL de la base de datos en las variables de entorno")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, bind=engine)

# Función para obtener una sesión de base de datos
@contextmanager
def getDB():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
    
# SQLITE
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(TEST_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@contextmanager
def getTestDB():
  db = TestSessionLocal()
  try:
    yield db
  finally:
    db.close()