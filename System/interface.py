import flet as ft
import constants
  
def initApp(page: ft.Page):
  from Modules.customControls import CustomContainer
  from Modules.login_module import Login
  
  login = Login(page)
  
  container = CustomContainer(width=900, height=500, containerContent=login)
  
  page.add(
    ft.Row(height=60),
    container,
    ft.Row(
      height = 60,
      controls=[
        ft.Text("© 2024 Kariña System. Todos los derechos reservados.", color="#222222", size=16)
      ],
      alignment=ft.MainAxisAlignment.CENTER
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
  
def updateContainerContent(page: ft.Page, newContent):
  if hasattr(page, "customContainer"):
    page.customContainer.updateContent(newContent)