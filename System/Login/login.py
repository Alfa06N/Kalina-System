import flet as ft
from .customControls import CustomContainer, CustomFilledButton, CustomGradientContainer, CustomWhiteContainer
import constants

class LoginForm(CustomGradientContainer):
  def __init__(self):
    super().__init__() 
    self.loginButton = ft.Row(
      controls=[
        CustomFilledButton(text="Iniciar Sesión", bgcolor=constants.ORANGE, size=18, color=constants.BLACK, overlay=constants.ORANGE_OVERLAY)
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )
    self.titleLogin = ft.Row(
      controls=[
        ft.Text("Iniciar Sesión", size=42, color=constants.WHITE, weight=ft.FontWeight.BOLD),
      ],
      alignment=ft.MainAxisAlignment.CENTER,
    )
    self.createText = ft.Row(
      controls=[
        ft.Text(value="¿Eres un nuevo usuario? ¡Haz click aquí!", size=18, color=constants.ORANGE) 
      ],
      alignment=ft.MainAxisAlignment.CENTER,
    )
    self.content = ft.Column(
      controls=[
        self.titleLogin,
        ft.Column(
          controls=[
            ft.TextField(label="Nombre de Usuario", border_color=constants.WHITE_GRAY, border_width=2, focused_border_color=constants.ORANGE_LIGHT, label_style=ft.TextStyle(
              color=constants.ORANGE_LIGHT
            )),
            ft.TextField(label="Contraseña", border_color=constants.WHITE_GRAY, border_width=2, password=True, can_reveal_password=True, focused_border_color=constants.ORANGE_LIGHT, label_style=ft.TextStyle(
              color=constants.ORANGE_LIGHT
            )),
            ft.Row(
              controls=[
                ft.Text("Ha olvidado su contraseña?", size=18, color=constants.ORANGE,)
              ],
              alignment=ft.MainAxisAlignment.CENTER
            )
          ],
          spacing=10,
        ),
        self.loginButton,
      ],
      alignment=ft.MainAxisAlignment.CENTER,
      spacing=40,
    )

class LoginPresentation(CustomWhiteContainer):
  def __init__(self):
    super().__init__()
    self.spacing = 10
    self.logo = ft.Image(src="../images/ks logo(only cup)edited.png", fit="contain", width=240, height=240)
    self.description = ft.Text(value="Kariña System", color=constants.BLACK, size=18, weight=ft.FontWeight.BOLD)
    self.button = CustomFilledButton(text="Registrarse", bgcolor=constants.BROWN, color=constants.WHITE, size=18, overlay=constants.BROWN_OVERLAY)
    self.register = ft.Row(
      controls=[
        self.button
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )
      
    self.title = ft.Text(value="Kaip'e Alimentos", size=42, color=constants.BROWN, weight=ft.FontWeight.BOLD, )
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

class Login(CustomContainer):
  def __init__(self):
    super().__init__()
    self.content = ft.Row(
      controls=[
        LoginPresentation(),
        LoginForm(),
      ]
    )