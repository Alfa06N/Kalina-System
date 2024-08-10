import flet as ft
import constants
  
def initApp(page: ft.Page):
  from Modules.customControls import CustomPrincipalContainer
  from Modules.login_module import Login
  
  login = Login(page)
  
  container = CustomPrincipalContainer(width=900, height=500, containerContent=login)
  
  page.add(
    ft.Column(expand=True),
    container,
    ft.Column(
      expand=True,
      controls=[
        ft.Text("© 2024 Kariña System. Todos los derechos reservados.", color="#222222", size=16)
      ],
      alignment=ft.MainAxisAlignment.END,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER
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
  
def updateContainerContent(page: ft.Page, newContent):
  if hasattr(page, "customContainer"):
    page.customContainer.updateContent(newContent)