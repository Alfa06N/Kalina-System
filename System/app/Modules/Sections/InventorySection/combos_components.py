import flet as ft 
import constants
from Modules.customControls import CustomUserIcon, CustomOperationContainer, CustomTextField, CustomAnimatedContainer, CustomNavigationOptions, CustomFilledButton, CustomDropdown, CustomDeleteButton, CustomAlertDialog
from config import getDB

class ComboInfo(ft.Stack):
  def __init__(self, page):
    super().__init__()
    self.page = page
    
    self.controls = [
      ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          ft.Text(
            value="Selecciona un combo para ver más información",
            color=constants.BLACK,
            size=32,
            weight=ft.FontWeight.W_700,
            text_align=ft.TextAlign.CENTER,
          )
        ]
      )
    ]