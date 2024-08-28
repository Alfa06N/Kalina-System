from datetime import datetime, date, time, timezone
from tzlocal import get_localzone

# Hacen lo mismo
print(f"datetime.today(): {datetime.today()}, type: {type(datetime.now().tzinfo)}")

print(f"datetime.now(): {datetime.now()}, type: {type(datetime.now())}")

print(f"datetime.now(timezone.utc): {datetime.now(tz=timezone.utc)}")

print(f"get_localzone(): {get_localzone()}")

from app.utils.dateConversions import getUTC, convertToLocalTz, getLocal, convertToUTC

utcDate = getUTC()
print(f"utcDate type: {utcDate.tzinfo} {utcDate}")
localDate = convertToLocalTz(utcDate)
print(f"localDate type: {localDate.tzinfo} {localDate}")


from datetime import timedelta

# Definir la fecha inicial
fecha_inicial = datetime(2024, 5, 14)

# Definir el número de días a sumar
dias_a_sumar = 105

# Crear un objeto timedelta con el número de días
delta = timedelta(days=dias_a_sumar)

# Sumar los días a la fecha inicial
fecha_final = fecha_inicial + delta

# Mostrar el resultado
print("Fecha Inicial:", fecha_inicial.strftime("%Y-%m-%d"))
print("Fecha Final:", fecha_final.strftime("%Y-%m-%d"))

horaInicio = datetime(2024, 8, 7, 8, 0, 0)
print(horaInicio)

delta = timedelta(minutes=4320)

horafinal = horaInicio + delta
print(horafinal)
print(4320/60)