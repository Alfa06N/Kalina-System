import flet as ft 
from Login.login import Login
from interface import showLogin
from Login.register import Register

def main(page: ft.Page):
  page.fonts = {
    "Grotesk": "fonts/CabinetGrotesk/CabinetGrotesk-Regular.otf",
    "GroteskBold": "fonts/CabinetGrotesk/CabinetGrotesk-Bold.otf"
  }

  # page.theme = ft.Theme(font_family="Grotesk")
  page.title = "Kariña System"
  page.bgcolor = "#e0e0e0"
  page.vertical_alignment = ft.MainAxisAlignment.CENTER
  page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

  showLogin(page)
  # page.add(Register())
ft.app(target=main)