from datetime import datetime, time, timezone
from tzlocal import get_localzone
import pytz
import calendar

def convertToLocalTz(utcDate: datetime) -> datetime:
  localTz = get_localzone()
  date = utcDate
  if date.tzinfo == None:
    date = utcDate.replace(tzinfo=pytz.utc)
  
  return date.astimezone(localTz)

def convertToUTC(localDate: datetime) -> datetime:
  if localDate.tzinfo is None:
    localTz = get_localzone()
    localDate = localTz.localize(localDate)

  return localDate.astimezone(pytz.utc)
  
def getUTC():
  return datetime.now(timezone.utc)

def getLocal():
  return convertToLocalTz(getUTC())

def numberToMonth(number):
  monthsInSpanish = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
  if number > 0 and number <= 12:
    return monthsInSpanish[number-1]
  return None