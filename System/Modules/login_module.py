import flet as ft
from Modules.customControls import CustomFilledButton, CustomSimpleContainer
import constants
import time
from validation import validateUsername, validatePassword, evaluateForm
from interface import showRegister, showRecovery

class LoginForm(CustomSimpleContainer):
  def __init__(self, page):
    super().__init__(height=500, width=450, gradient=True)
    self.page = page 
    self.loginButton = ft.Row(
      controls=[
        CustomFilledButton(text="Iniciar Sesión", bgcolor=constants.ORANGE, size=18, color=constants.BLACK, overlay=constants.ORANGE_OVERLAY, clickFunction=self.validateLogin)
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )
    self.titleLogin = ft.Row(
      controls=[
        ft.Text("Iniciar Sesión", size=42, color=constants.WHITE, weight=ft.FontWeight.BOLD),
      ],
      alignment=ft.MainAxisAlignment.CENTER,
    )
  

    self.usernameInput = ft.TextField(
      label="Nombre de Usuario", border_color=constants.WHITE_GRAY,
      border_width=2,
      focused_border_color=constants.ORANGE_LIGHT, 
      label_style=ft.TextStyle(
        color=constants.ORANGE_LIGHT
      ),
      on_change=lambda e: validateUsername(self.usernameInput)
    )

    self.passwordInput = ft.TextField(
      label="Contraseña", 
      border_color=constants.WHITE_GRAY, 
      border_width=2, 
      password=True, 
      can_reveal_password=True, 
      focused_border_color=constants.ORANGE_LIGHT, 
      label_style=ft.TextStyle(
        color=constants.ORANGE_LIGHT
      ),
      on_change=lambda e: validatePassword(self.passwordInput)
    )

    self.passwordRecovery = ft.Row(
      controls=[
        ft.GestureDetector(
         content=ft.Text("Ha olvidado su contraseña?", size=18, color=constants.ORANGE_LIGHT, text_align=ft.TextAlign.CENTER),
         on_tap=lambda e: showRecovery(self.page),
         mouse_cursor="click",
        )
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )

    self.content = ft.Column(
      controls=[
        self.titleLogin,
        ft.Column(
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
    )
  
  def validateLogin(self, e):
    isValid = evaluateForm(username=[self.usernameInput], password=[self.passwordInput])
    
    if isValid:
      print("Inicio de sesión exitoso")
    else:
      print("Inicio de sesión rechazado")

class LoginPresentation(CustomSimpleContainer):
  def __init__(self, page):
    super().__init__(height=500, width=450, gradient=False)
    self.spacing = 10
    self.page = page
    
    self.logo = ft.Image(src="../images/ks logo(only cup)edited.png", fit="contain", width=240, height=240)
    self.description = ft.Text(value="Kaip'e Alimentos", color=constants.BLACK, size=18, weight=ft.FontWeight.BOLD)
    self.button = CustomFilledButton(text="Registrarse", bgcolor=constants.BROWN, color=constants.WHITE, size=18, overlay=constants.BROWN_OVERLAY, clickFunction=lambda e: showRegister(self.page))
    self.register = ft.Row(
      controls=[
        self.button
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )
      
    self.title = ft.Text(value="Kariña System", size=42, color=constants.BROWN, weight=ft.FontWeight.BOLD, )
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

class Login(ft.Row):
  def __init__(self, page):
    super().__init__()
    self.page = page
    self.spacing = 0
    
    self.controls = [
      LoginPresentation(self.page),
      LoginForm(self.page),
    ]