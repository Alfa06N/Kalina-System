import flet as ft 
import constants
from Modules.customControls import CustomPrincipalContainer, CustomFilledButton, CustomSimpleContainer
from interface import showLogin

class RecoveryForm(CustomSimpleContainer):
  def __init__(self, page):
    super().__init__(width=450, height=500, gradient=True)
    self.spacing = 10
    self.page = page
    
class RecoveryPresentation(CustomSimpleContainer):
  def __init__(self, page):
    super().__init__(width=450, height=500, gradient=False)
    self.spacing = 10
    self.page = page
    
    self.title = ft.Text(
      value="Recupera tu acceso",
      size=42,
      text_align=ft.TextAlign.CENTER,
      weight=ft.FontWeight.BOLD,
      color=constants.BROWN
    )
    
    self.button = CustomFilledButton(
      text="Iniciar Sesión",
      size=18,
      color=constants.WHITE,
      bgcolor=constants.BROWN,
      overlay=constants.BROWN_OVERLAY,
      clickFunction=lambda e: showLogin(self.page)
    )
    
    self.content = ft.Column(
      controls=[
        self.title, 
        self.button
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )
    
class Recovery(ft.Row):
  def __init__(self, page):
    super().__init__()
    self.page = page
    
    self.controls = [
      RecoveryForm(self.page),
      RecoveryPresentation(self.page),
    ]
  