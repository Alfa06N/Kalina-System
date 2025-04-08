import flet as ft 
BROWN = "#36240C"
BROWN_OVERLAY = "#664a1d"
ORANGE = "#D19D4B"
ORANGE_LIGHT = "#efd098"
ORANGE_OVERLAY = "#e6b363"
ORANGE_TEXT = "#bf5d20"
SANDY_BROWN = "#dd9a4c"
BLACK = "#222222"
BLACK_GRAY = "#444444"
BLACK_INK = "#888888"
BLUE = "#0077ce"
BLUE_CAKE = "#6BAAB9"
POWDER_BLUE = "#8E9EB5"
WHITE = "#DCDCDC"
WHITE_BACKGROUND = "#CBCBCB"
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
  ft.dropdown.Option("Modelo de tu primer coche"),
  ft.dropdown.Option("Nombre de tu profesor favorito"),
  ft.dropdown.Option("¿Cuál es tu canción favorita?"),
  ft.dropdown.Option("¿En qué ciudad naciste?"),
]

methodIcons = {
  "All": ft.Icons.WALLET_ROUNDED,
  "Pago Móvil": ft.Icons.PHONE_ANDROID_ROUNDED,
  "Punto de Venta": ft.Icons.CREDIT_CARD_ROUNDED,
  "Cripto Activo": ft.Icons.CURRENCY_BITCOIN_ROUNDED,
  "Efectivo": ft.Icons.POINT_OF_SALE_ROUNDED,
  "Biopago": ft.Icons.FINGERPRINT,
  "Transferencia": ft.Icons.COMPARE_ARROWS_ROUNDED,
}

transactionType = {
  "Payment": "Pago",
  "Change": "Cambio"
}

companyInfo = {
  "email": "kaipe.contacto@gmail.com",
  "phone": "+58 412-8945511",
  "rif": "J-50457264-0",
}

documentTypes = {
  "Jurídico": "J-",
  "Extranjero": "E-",
  "Venezolano": "V-",
  "Gubernamental": "G-",
}

aboutUs = {
  "essence": "En Kaip’e Alimentos, creemos en la conexión entre la cultura, la tradición y el café. Nuestro propósito es más que solo ofrecer productos; es compartir una historia, una identidad y un legado que une a las personas a través de cada taza.",
  "mission": "Brindar productos de alta calidad que representen la riqueza cultural de nuestros orígenes. Buscamos fomentar el consumo consciente y responsable, destacando el valor del café como símbolo de tradición y comunidad.",
  "vision": "Ser una empresa referente en el mercado, reconocida por su compromiso con la autenticidad, la innovación y el impacto positivo en la comunidad, manteniendo siempre la esencia de nuestras raíces."
}