import flet as ft 
from interface import initApp
import constants

def main(page: ft.Page):
  page.fonts = {
    "Grotesk": "fonts/CabinetGrotesk/CabinetGrotesk-Regular.otf",
    "GroteskBold": "fonts/CabinetGrotesk/CabinetGrotesk-Bold.otf"
  }

  # page.theme = ft.Theme(font_family="Grotesk")
  page.title = "Kariña System"
  page.bgcolor = constants.WHITE
  page.vertical_alignment = ft.MainAxisAlignment.CENTER
  page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
  
  initApp(page)
ft.app(target=main)