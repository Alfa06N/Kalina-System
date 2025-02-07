from datetime import datetime, time, timezone
from tzlocal import get_localzone
import pytz
import calendar
from zoneinfo import ZoneInfo
from dateutil import parser

def convertToLocalTz(utcDate: datetime) -> datetime:
  # Convertir string a datetime si es necesario
  if isinstance(utcDate, str):
    try:
      utcDate = datetime.strptime(utcDate, "%Y-%m-%d %H:%M:%S")  # Intenta formato estándar
    except ValueError:
      try:
        utcDate = datetime.strptime(utcDate, "%d/%m/%Y")  # Intenta otro formato
      except ValueError:
        raise ValueError("Formato de fecha no soportado")
    
    # Asignar zona horaria UTC si no tiene una
  if utcDate.tzinfo is None:
    utcDate = utcDate.replace(tzinfo=ZoneInfo("UTC"))
    
  # Convertir a zona horaria local
  localTz = ZoneInfo("America/Caracas")
  localDate = utcDate.astimezone(localTz)
    
  return localDate

def convertToUTC(localDate: datetime) -> datetime:
  if localDate.tzinfo is None:
    localTz = ZoneInfo("America/Caracas")
    localDate = localDate.replace(tzinfo=localTz)

  return localDate.astimezone(ZoneInfo("UTC"))
  
def getUTC():
  return datetime.now(timezone.utc)

def getLocal():
  return convertToLocalTz(getUTC())

def numberToMonth(number):
  monthsInSpanish = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
  if number > 0 and number <= 12:
    return monthsInSpanish[number-1]
  return None