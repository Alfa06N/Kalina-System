import flet as ft 
from interface import initApp
import locale
import constants
from initialization import init_db
from utils.pathUtils import getFontPath, getImagePath

locale.setlocale(locale.LC_TIME, 'es_ES')
def main(page: ft.Page):
  page.title = "Kariña System"
  page.fonts = {
    "Scripter": getFontPath("Scripter-Regular.ttf")
  }
  page.theme = ft.Theme(
    scrollbar_theme=ft.ScrollbarTheme(
      track_color={
        ft.ControlState.DEFAULT: constants.BLACK_GRAY,
      },
      thumb_color={
        ft.ControlState.DEFAULT: constants.BLACK_GRAY,
      }
    )
  )
  
  page.theme_mode = ft.ThemeMode.LIGHT
  page.bgcolor = constants.WHITE
  page.vertical_alignment = ft.MainAxisAlignment.CENTER
  page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
  page.padding = 0 
  init_db() 

  initApp(page)
  
if __name__ == "__main__":
  
  ft.app(target=main)