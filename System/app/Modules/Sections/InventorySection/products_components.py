import flet as ft 
import constants
from Modules.customControls import CustomUserIcon, CustomOperationContainer, CustomTextField, CustomAnimatedContainer, CustomNavigationOptions, CustomFilledButton, CustomDropdown, CustomDeleteButton, CustomAlertDialog
from config import getDB

class ProductInfo(ft.Stack):
  def __init__(self, page):
    super().__init__()
    self.page = page
    
    self.controls = [
      ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        controls=[
          ft.Text(
            value="Selecciona un producto para ver más información",
            color=constants.BLACK,
            size=32,
            weight=ft.FontWeight.W_700,
            text_align=ft.TextAlign.CENTER,
          )
        ]
      )
    ]