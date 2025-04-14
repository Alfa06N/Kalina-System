import flet as ft
import constants
from Modules.customControls import CustomAnimatedContainer
from utils.dateConversions import getLocal
from datetime import datetime
  
def initApp(page: ft.Page):
  from Modules.customControls import CustomPrincipalContainer
  from Modules.login_module import Login
  
  login = Login(page)
  
  container = CustomPrincipalContainer(containerContent=login)
  
  page.add(
    ft.Column(expand=True),
    container,
    ft.Column(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      controls=[
        ft.Text(f"© {getLocal().strftime("%Y")} Kaip'e Alimentos y Equipo Desarrollador. Todos los derechos reservados", color="#222222", size=16, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_600)
      ]
    )
  )
  
  # Referencia al contenedor
  page.customContainer = container
  
def showRegister(page: ft.Page):
  from Modules.register_module import Register
  
  register = Register(page)
  updateContainerContent(page, register)

def showLogin(page: ft.Page):
  from Modules.login_module import Login
  
  login = Login(page)
  updateContainerContent(page, login)
  
def showRecovery(page: ft.Page):
  from Modules.recovery_module import Recovery
  
  recovery = Recovery(page)
  updateContainerContent(page, recovery)
  
def showPrincipal(page: ft.Page):
  from Modules.customControls import CustomAppBar, CustomSidebar, CustomAnimatedContainer, CustomMainContainer, CustomExchangeDialog
  from Modules.Sections.SalesSection.sales import Sales
  from config import getDB
  from DataBase.crud.user import getUserByUsername
  from utils.sessionManager import getCurrentUser
  from utils.exchangeManager import exchangeRateManager
  
  user = None
  initial = ""
  exchangeRateManager.clearSubscribers()
  
  with getDB() as db:
    try:
      user = getUserByUsername(db, getCurrentUser())
      if user:
        initial = f"{user.employee.name[0]}{user.employee.surname[0]}"
    except Exception as err:
      print(f"Error {err}")
  
  appBar = CustomAppBar("Kariña System", page, initial)
  sideBar = CustomSidebar(page)
  mainContainer = CustomMainContainer(Sales(page))
  
  page.mainContainer = mainContainer
  page.sideBar = sideBar
  
  page.controls.clear()
  page.add(
    appBar,
    ft.Row(
      expand=True,
      spacing=0,
      controls=[
        sideBar,
        ft.Stack(
          expand=True,
          controls=[
            ft.Column(
              expand=True,
              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
              controls=[
                mainContainer,
              ]
            ),
            ft.Container(
              bottom=0,
              left=0,
              right=0,
              expand=True,
              alignment=ft.alignment.center,
              content=ft.Text(f"© {getLocal().strftime("%Y")} Kaip'e Alimentos y Equipo Desarrollador. Todos los derechos reservados", color="#222222", size=16, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_600),
            )
          ]
        ),
        
        
      ]
    )
  )
  
def logout(page: ft.Page):
  page.controls.clear()
  initApp(page)
  
def updateContainerContent(page: ft.Page, newContent):
  if hasattr(page, "customContainer"):
    page.customContainer.updateContent(newContent)