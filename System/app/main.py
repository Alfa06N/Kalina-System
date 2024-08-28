import flet as ft 
from interface import initApp, showPrincipal
import constants
from initialization import init_db
from Modules.customControls import CustomAppBar, CustomUserIcon, CustomSidebar
from config import getDB
from DataBase.crud.user import getUsers

def main(page: ft.Page):
  page.title = "Kariña System"
  page.theme_mode = ft.ThemeMode.LIGHT
  page.bgcolor = constants.WHITE
  page.vertical_alignment = ft.MainAxisAlignment.CENTER
  page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
  page.padding = 0
  
  init_db()
  showPrincipal(page)
  
  # initApp(page)
  

if __name__ == "__main__":
  ft.app(target=main)