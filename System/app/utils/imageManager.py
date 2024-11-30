import flet as ft 
import shutil
import os
import time
from utils.pathUtils import getFolderDataPath
from exceptions import InvalidData

class ImageManager():
  def __init__(self):
    self.storage_path = getFolderDataPath()
  
  @staticmethod
  def validFileExtension(filePath):
    fileExtension = os.path.splitext(filePath)[1].lower()
    print(fileExtension)
    
    return fileExtension in [".jpeg", ".jpg", ".png", ".jfif"]
  
  def storageImage(self, idData, filePath):
    try:
      if not self.validFileExtension(filePath):
        raise InvalidData("Extensión de archivo inválida. Solo .jpeg, .jpg and .png son permitidos.")
      
      fileExtension = os.path.splitext(filePath)[1].lower()
      currentTimeStamp = int(time.time())
      destinationPath = os.path.join(self.storage_path, f"{idData}{currentTimeStamp}{fileExtension}")
      
      if os.path.exists(destinationPath):
        os.remove(destinationPath)
        print("Archivo ya existente eliminado")
      
      shutil.copy2(filePath, destinationPath)
      print(f"Imagen guardada en: {destinationPath}")
      return f"{idData}{currentTimeStamp}{fileExtension}"
    except shutil.SameFileError:
      print("El ruta de origen y destino apuntan al mismo archivo")
      return None
    except PermissionError:
      print("Permiso denegado. Verifica los permisos del archivo o carpeta.")
      return None
    except InvalidData as err:
      raise
      return None
    except Exception as err:
      raise
      return None
  
  def getImagePath(self, filePath):
    try:
      if filePath:
        destinationPath = os.path.join(self.storage_path, filePath)
        return destinationPath
      else:
        return None
    except Exception as err:
      raise
      return None

  def removeOldImage(self, filePath):
    try:
      destinationPath = os.path.join(self.storage_path, filePath)
      os.remove(destinationPath)
      return destinationPath
    except Exception as err:
      print(err)
      return None
  
  def updateImage(self, idData, oldImage, newImage):
    try:
      oldPath = self.getImagePath(oldImage)
      
      # Guardar nueva:
      newPath = self.storageImage(idData, newImage)
      
      # Eliminar vieja
      if oldPath:
        if os.path.exists(oldPath):
          os.remove(oldPath)
          print(f"Vieja imagen eliminada: {oldPath}")
      
      return newPath
        
    except Exception as err:
      print(err)
      return None