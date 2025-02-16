import flet as ft 
from interface import initApp, showPrincipal
import constants
from initialization import init_db
from Modules.customControls import CustomAppBar, CustomUserIcon, CustomSidebar, CustomCardInfo, CustomDatePicker, CustomFilledButton, CustomAnimatedContainer, CustomAutoComplete, CustomNumberField, CustomTooltip, CustomTextField, CustomDropdown, CustomItemsSelector, CustomItemCard, CustomImageContainer, CustomFilePicker
from utils.sessionManager import getCurrentUser, setUser
from config import getDB
from DataBase.crud.user import getUsers, getUserByUsername, updateUser
from DataBase.crud.product import getProductByName, getProducts
from DataBase.crud.category import getCategories, removeCategory
from DataBase.crud.closing import removeClosing
from DataBase.crud.closing import getSalesWithoutClosing
from utils.imageManager import ImageManager
import time
from utils.datetimeGlobal import getTime, syncTime, getCurrentTime
import asyncio
from DataBase.crud.transaction import getTransactions
from Modules.Sections.ClosingsSection.components.ClosingRecord import ClosingRecord
import time

def main(page: ft.Page):
  page.title = "Kariña System"
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
  
  with getDB() as db:
    sales, products, combos, generalPrice, totals, gain = getSalesWithoutClosing(db)
    print(f"Combos: {combos}")
    print(f"Products: {products}")

  setUser("Alfa06N")
  showPrincipal(page)
  # initApp(page)

 
if __name__ == "__main__":
  
  ft.app(target=main)