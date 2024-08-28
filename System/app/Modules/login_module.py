import flet as ft
from Modules.customControls import CustomFilledButton, CustomSimpleContainer, CustomTextField, CustomOperationContainer
import constants
import time
from validation import validateUsername, validatePassword, evaluateForm
from interface import showRegister, showRecovery, showPrincipal
from utils.pathUtils import getImagePath
from utils.sessionManager import setUser
from DataBase.crud.user import getUserByUsername, queryUserData
from config import getDB
from exceptions import DataNotFoundError

class LoginForm(CustomSimpleContainer):
  def __init__(self, page, containerFather):
    super().__init__(height=500, width=450, gradient=False)
    self.page = page 
    self.containerFather = containerFather
    
    self.loginButton = ft.Row(
      height=100,
      controls=[
        CustomFilledButton(text="Iniciar Sesión", bgcolor=constants.BROWN, size=18, color=constants.WHITE, overlay=constants.BROWN_OVERLAY, clickFunction=self.login)
      ],
      alignment=ft.MainAxisAlignment.CENTER,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    self.titleLogin = ft.Row(
      height=80,
      controls=[
        ft.Text("Iniciar Sesión", size=42, color=constants.BROWN, weight=ft.FontWeight.BOLD),
      ],
      alignment=ft.MainAxisAlignment.CENTER,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
  

    self.usernameInput = CustomTextField(
      label="Nombre de usuario",
      revealPassword=True,
      mode="light",
      hint_text=None,
      field="username",
      expand=False,
      submitFunction=self.login
    )

    self.passwordInput = CustomTextField(
      label="Contraseña",
      revealPassword=True,
      mode="light",
      hint_text=None,
      field="password",
      expand=False,
      submitFunction=self.login
    )

    self.passwordRecovery = ft.Row(
      controls=[
        ft.GestureDetector(
         content=ft.Text("Ha olvidado su contraseña?", size=18, color=constants.BLACK, text_align=ft.TextAlign.CENTER),
         on_tap=lambda e: showRecovery(self.page),
         mouse_cursor="click",
        )
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )
    self.content = CustomOperationContainer(
      operationContent=ft.Column(
        controls=[
          self.titleLogin,
          ft.Column(
            expand=True,
            controls=[
              self.usernameInput,
              self.passwordInput,
              self.passwordRecovery,
            ],
            spacing=10,
            height=180,
            alignment=ft.MainAxisAlignment.CENTER
          ),
          self.loginButton,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=40,
      ),
      mode="light"
    )
  
  def login(self, e):
    if evaluateForm(username=[self.usernameInput], password=[self.passwordInput]):
      try:
        with getDB() as db:
          if queryUserData(db, self.usernameInput.value, self.passwordInput.value):
            setUser(self.usernameInput.value)
            self.content.actionSuccess(f"Bienvenido {self.usernameInput.value}")
            time.sleep(1.5)
            showPrincipal(self.page)
          else:
            self.content.actionFailed("Contraseña incorrecta")
            time.sleep(1.5)
            self.content.restartContainer()
      except DataNotFoundError as e:
        self.content.actionFailed(e)
        time.sleep(1.5)
        self.content.restartContainer()
      except Exception as e:
        print("Unexpected Error:", e)

class LoginPresentation(CustomSimpleContainer):
  def __init__(self, page):
    super().__init__(height=500, width=450, gradient=True)
    self.spacing = 10
    self.page = page
    
    self.logo = ft.Image(src=getImagePath("ks logo(only cup)edited.png"), fit="contain", width=240, height=240)
    
    self.description = ft.Text(value="Kaip'e Alimentos", color=constants.WHITE, size=18, weight=ft.FontWeight.BOLD)
    
    self.button = CustomFilledButton(text="Registrarse", bgcolor=constants.ORANGE, color=constants.BLACK, size=18, overlay=constants.ORANGE_OVERLAY, clickFunction=lambda e: showRegister(self.page))
    self.register = ft.Row(
      controls=[
        self.button
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )
      
    self.title = ft.Text(value="Kariña System", size=42, color=constants.WHITE, weight=ft.FontWeight.BOLD)
    self.content = ft.Column(
      controls=[
        self.title,
        self.logo,
        self.register,
        self.description,
      ],
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
class Login(CustomOperationContainer):
  def __init__(self, page):
    super().__init__(
      operationContent=ft.Row(
        controls=[
          LoginPresentation(page),
          LoginForm(page, self)
        ]
      ),
      mode="light"
    )
    