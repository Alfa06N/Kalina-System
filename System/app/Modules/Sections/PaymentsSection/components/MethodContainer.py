from exceptions import DataAlreadyExists, DataNotFoundError
import re
import flet as ft
import constants
from Modules.Sections.PaymentsSection.components.PaymentInfo import PaymentInfo

class MethodContainer(ft.Container):
  def __init__(self, page, method, on_click=None):
    super().__init__()
    self.page = page
    

    self.margin = ft.margin.symmetric( vertical=4)
    self.padding = ft.padding.all(10)
    self.bgcolor = constants.WHITE
    self.border_radius = ft.border_radius.all(30)
    self.ink = True
    self.ink_color = constants.BLACK_INK
    self.on_click = on_click
    
    self.methodIcon = ft.Icon(
      name=constants.methodIcons[method],
      size=40,
      color=constants.BLACK,
    )
    
    self.methodText = ft.Text(
      value=method,
      size=20,
      color=constants.BLACK,
      weight=ft.FontWeight.W_700,
      overflow=ft.TextOverflow.ELLIPSIS,
    )
    
    self.content = ft.Row(
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        self.methodIcon,
        self.methodText,
      ]
    )
  
  def selectContainer(self):
    self.shadow = ft.BoxShadow(
      spread_radius=1,
      blur_radius=1,
      color=constants.WHITE_GRAY,
    )
    self.update()
  
  def deselectContainer(self):
    self.shadow = None
    self.update()