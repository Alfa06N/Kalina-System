import flet as ft
import constants
from Modules.customControls import CustomAnimatedContainer
  
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
        ft.Text("© 2024 Kariña System. Todos los derechos reservados.", color="#222222", size=16)
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
  from Modules.customControls import CustomAppBar, CustomSidebar, CustomAnimatedContainer, CustomMainContainer
  from Modules.Sections.HomeSection.home import Home
  from config import getDB
  from DataBase.crud.user import getUserByUsername
  from utils.sessionManager import getCurrentUser
  
  user = None
  initial = ""
  
  with getDB() as db:
    try:
      user = getUserByUsername(db, getCurrentUser())
      if user:
        initial = f"{user.employee.name[0]}{user.employee.surname[0]}"
    except Exception as err:
      print(f"Error {err}")
  
  appBar = CustomAppBar("Kariña System", page, initial)
  sideBar = CustomSidebar(page)
  mainContainer = CustomMainContainer(Home(page))
  
  page.mainContainer = mainContainer
  
  page.controls.clear()
  page.add(
    appBar,
    ft.Row(
      expand=True,
      spacing=0,
      controls=[
        sideBar,
        mainContainer,
      ]
    )
  )
  
def logout(page: ft.Page):
  page.controls.clear()
  initApp(page)
  
def updateContainerContent(page: ft.Page, newContent):
  if hasattr(page, "customContainer"):
    page.customContainer.updateContent(newContent)