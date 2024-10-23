import flet as ft
import constants
from Modules.customControls import CustomAlertDialog, CustomAnimatedContainer, CustomAnimatedContainerSwitcher, CustomOperationContainer, CustomTextField, CustomDropdown, CustomImageContainer, CustomFloatingActionButton, CustomFilledButton, CustomTooltip

class ChangeCard(ft.Container):
  def __init__(self, page, formContainer, height=160, width=160):
    super().__init__()
    self.page = page
    self.height = height
    self.width = width
    self.formContainer = formContainer
    
    self.bgcolor = constants.WHITE
    self.border = ft.border.all(2, constants.BLACK_GRAY)
    self.border_radius = 20
    self.padding = ft.padding.all(10)
    self.ink = True
    self.ink_color = constants.WHITE_GRAY
    self.on_click = lambda e: self.clickFunction()
    
    self.price = 0
    
    self.changeContent = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Icon(
          name=ft.icons.CURRENCY_EXCHANGE_ROUNDED,
          size=32,
          color=constants.BLACK,
        ),
        ft.Text(
          value=f"Cambio",
          size=18,
          color=constants.BLACK,
          text_align=ft.TextAlign.CENTER,
          overflow=ft.TextOverflow.ELLIPSIS,  
        ),
        ft.Text(
          value=f"{self.price}$",
          size=18,
          color=constants.BLACK,
          weight=ft.FontWeight.W_700,
          text_align=ft.TextAlign.CENTER,
          overflow=ft.TextOverflow.ELLIPSIS,
        )
      ]
    )
    
    self.content = self.changeContent
    
  def clickFunction(self):
    try:
      pass
    except:
      pass