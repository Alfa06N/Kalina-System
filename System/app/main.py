import flet as ft 
from interface import initApp, showPrincipal
import locale
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
# from DataBase.crud.user_product import getAllRegisters
from utils.imageManager import ImageManager
from utils.datetimeGlobal import getTime, syncTime, getCurrentTime
import asyncio
from DataBase.crud.transaction import getTransactions
from Modules.Sections.ClosingsSection.components.ClosingRecord import ClosingRecord
import time
from utils.pathUtils import getImagePath, getFontPath
from utils.inventoryManager import inventoryManager
from datetime import datetime

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

  setUser("Alfa06N")
  showPrincipal(page)
  # initApp(page)
  
  # Error showing sales history after scrolling between pages and trying to select another sale
  # Fixing possibility of register UserProduct record when updates stock by 0. This can't be recorded in the database.
  
if __name__ == "__main__":
  
  ft.app(target=main)