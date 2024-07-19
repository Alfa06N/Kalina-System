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
  def animateContainer(e):
    container.width = 300 if container.width == 100 else 100
    container.height = 300 if container.height == 100 else 100
    container.update()
    
  container = ft.Container(
    width=100,
    height=100,
    bgcolor="blue",
    animate=ft.animation.Animation(duration=1000, curve=ft.AnimationCurve.ELASTIC_OUT),
  )
  
  # page.add(ft.Column(
  #   controls=[
  #     container,
  #     ft.ElevatedButton("Animate", on_click=animateContainer),
  #   ],
  #   alignment=ft.MainAxisAlignment.CENTER,
  #   horizontal_alignment=ft.CrossAxisAlignment.CENTER
  # ))
  
  initApp(page)
ft.app(target=main)