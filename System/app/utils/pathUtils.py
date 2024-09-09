from pathlib import Path
import os

def getProjectRoot() -> Path:
  return Path(__file__).resolve().parent.parent

def getImagePath(imageName: str) -> Path:
  return getProjectRoot() / "images" / imageName

def getFolderDataPath():
  try:
    folderPath = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Kariña System")
    
    os.makedirs(folderPath, exist_ok=True)
    return folderPath
  except Exception as err:
    raise
  
def getProductFolderPath():
  try:
    folderPath = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Kariña System", "Products")
    os.makedirs(folderPath, exist_ok=True)
    return folderPath
  except Exception as err:
    raise

def getComboFolderPath():
  try:
    folderPath = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Kariña System", "Combos")
    os.makedirs(folderPath, exist_ok=True)
    return folderPath
  except Exception as err:
    raise
  
def getCategoryFolderPath():
  try:
    folderPath = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Kariña System", "Category")
    os.makedirs(folderPath, exist_ok=True)
    return folderPath
  except Exception as err:
    raise