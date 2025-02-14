import ntplib
from datetime import datetime, timezone, timedelta
from utils.dateConversions import convertToLocalTz, getLocal
import time

lastSync = None

def getTime():
  try:
    client = ntplib.NTPClient()
    response = client.request("pool.ntp.org")
    time = convertToLocalTz(datetime.fromtimestamp(response.tx_time, tz=timezone.utc))
    return time
  except Exception as err:
    print(f"Error al obtener la hora: {err}")
    return None

def saveLastSync(data):
  global lastSync
  lastSync = data
  return lastSync

def getLastSync():
  return lastSync

def syncTime():
  ntpTime = getTime()
  
  if ntpTime:
    data = {
      "ntp": ntpTime,
      "local": time.time()
    }
    
    newSync = saveLastSync(data)

    print("Tiempo sincronizado (Local):", ntpTime.strftime("%d-%m-%Y, %H:%M:%S"))
    print("Valor de ultima sincronizacion:", lastSync)
    return newSync
  else:
    print("No se puedo sincronizar la hora.")

def getCurrentTime():
  global lastSync
  
  def cleanDatetime():
    ntpTime = lastSync["ntp"]
    local = lastSync["local"]
    timeElapsed = time.time() - local
    currentTime = ntpTime + timedelta(seconds=timeElapsed)
    return currentTime
  
  if lastSync:
    return cleanDatetime()
  else:
    lastSync = syncTime()
    if lastSync:
      return cleanDatetime()
    else:
      print("No se ha podido sincronizar la hora. En cambio, se usara el reloj del dispositivo")
      return None