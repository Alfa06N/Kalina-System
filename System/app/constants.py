import flet as ft 
BROWN = "#36240C"
BROWN_OVERLAY = "#664a1d"
ORANGE = "#E19E45"
ORANGE_LIGHT = "#efd098"
ORANGE_OVERLAY = "#e6b363"
ORANGE_TEXT = "#bf5d20"
BLACK = "#222222"
BLACK_GRAY = "#666666"
BLACK_INK = "#888888"
BLUE = "#0077ce"
BLUE_CAKE = "#6BAAB9"
WHITE = "#ededed"
# WHITE = "#f7f7f7"
WHITE_GRAY = "#999999"
GREEN_TEXT = "#049116"
GREEN_PRICE = "#00b916"
GREEN_SUCCESS = "#33f54a"
GREEN_LIGHT = "#b2ffba"
RED_TEXT = "#c11414"
RED_FAILED = "#ff6666"
RED_FAILED_LIGHT = "#ffa0a0"
WHITE_INK = "888888"
WHITE_HIGHLIGHT = "BBBBBB" 

# Dropdowns 
dropdownOne = [
  ft.dropdown.Option("¿Cuál es tu comida favorita?"),
  ft.dropdown.Option("¿Cuál es tu mayor miedo?"),
  ft.dropdown.Option("¿Cuál es tu libro favorito?"),
  ft.dropdown.Option("¿Cuál es tu película favorita?"),
  ft.dropdown.Option("¿Cuál es tu color favorito?"),
]

dropdownTwo = [
  ft.dropdown.Option("¿Cuál es tu deporte favorito?"),
  ft.dropdown.Option("¿Cuál fue el modelo de tu primer coche?"),
  ft.dropdown.Option("¿Cuál es el nombre de tu profesor favorito?"),
  ft.dropdown.Option("¿Cuál es tu canción favorita?"),
  ft.dropdown.Option("¿En qué ciudad naciste?"),
]

methodIcons = {
  "Pago Móvil": ft.icons.PHONE_ANDROID_ROUNDED,
  "Punto de Venta": ft.icons.POINT_OF_SALE_ROUNDED,
  "Cripto Activo": ft.icons.CURRENCY_BITCOIN_ROUNDED,
  "Efectivo": ft.icons.MONEY_ROUNDED,
  "Biopago": ft.icons.BIOTECH_ROUNDED,
  "Transferencia": ft.icons.SEND_ROUNDED,
}