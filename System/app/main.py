import flet as ft 
from interface import initApp
import constants
from initialization import init_db

def main(page: ft.Page):
  page.title = "Kariña System"
  page.bgcolor = constants.WHITE
  page.vertical_alignment = ft.MainAxisAlignment.CENTER
  page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
  vertical_alignment=ft.CrossAxisAlignment.CENTER
  
  init_db()
  initApp(page)

if __name__ == "__main__":
  ft.app(target=main)