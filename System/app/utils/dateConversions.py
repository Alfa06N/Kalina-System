from datetime import datetime, time, timezone
from tzlocal import get_localzone
import pytz
import calendar
from zoneinfo import ZoneInfo
from dateutil import parser

def convertToLocalTz(utcDate: datetime) -> datetime:
  if isinstance(utcDate, str):
    utcDate = datetime.strptime(utcDate, "%d/%m/%Y")
  
  if utcDate.tzinfo == None:
    date = utcDate.replace(tzinfo=ZoneInfo("UTC"))
  
  localTz = ZoneInfo("America/Caracas")
  
  return utcDate.astimezone(localTz)

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