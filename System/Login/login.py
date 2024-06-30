import flet as ft
from .customControls import CustomContainer, CustomFilledButton

class LoginForm(ft.Container):
  def __init__(self):
    super().__init__() 
    self.height = 500
    self.width = 400
    self.border_radius = ft.border_radius.all(30)
    self.padding = ft.padding.symmetric(horizontal=30, vertical=20)
    self.loginButton = ft.Row(
      controls=[
        CustomFilledButton(text="Iniciar Sesión", bgcolor="#E19E45", size=18, color="#222222", overlay="#e6b363")
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )
    self.titleLogin = ft.Row(
      controls=[
        ft.Text("Iniciar Sesión", size=42, color="#e0e0e0", weight=ft.FontWeight.BOLD),
      ],
      alignment=ft.MainAxisAlignment.CENTER,
    )
    self.createText = ft.Row(
      controls=[
        ft.Text(value="¿Eres un nuevo usuario? ¡Haz click aquí!", size=18, color="#E19E45") 
      ],
      alignment=ft.MainAxisAlignment.CENTER,
    )
    self.gradient=ft.LinearGradient(
      begin=ft.alignment.center_left,
      end=ft.alignment.center_right,
      colors=["#36240c", "#222222"]
    )
    self.content = ft.Column(
      controls=[
        self.titleLogin,
        ft.Column(
          controls=[
            ft.TextField(label="Nombre de Usuario", border_color="#e0e0e0", border_width=2),
            ft.TextField(label="Contraseña", border_color="#e0e0e0", border_width=2, password=True, can_reveal_password=True),
            ft.Row(
              controls=[
                ft.Text("Ha olvidado su contraseña?", size=18, color="#E19E45")
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
    # self.alignment=ft.alignment.center

class LoginPresentation(ft.Container):
  def __init__(self):
    super().__init__()
    self.height = 500
    self.width = 400
    self.padding = 20
    self.spacing = 10
    self.logo = ft.Image(src="../images/ks logo(only cup)edited.png", fit="contain", width=240, height=240)
    self.description = ft.Text(value="Kariña System", color="#36240C", size=18, weight=ft.FontWeight.BOLD)
    self.button = CustomFilledButton(text="Register", bgcolor="#36240C", color="#e0e0e0", size=18, overlay="#664a1d")
    self.register = ft.Row(
      controls=[
        self.button
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )
      
    self.title = ft.Text(value="Kaip'e Alimentos", size=42, color="#36240C", weight=ft.FontWeight.BOLD, )
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