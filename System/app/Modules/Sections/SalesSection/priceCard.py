import flet as ft
import constants
from Modules.customControls import CustomAlertDialog, CustomAnimatedContainer, CustomAnimatedContainerSwitcher, CustomOperationContainer, CustomTextField, CustomDropdown, CustomImageContainer, CustomFloatingActionButton, CustomFilledButton, CustomTooltip
import threading
import time

class PriceCard(ft.Container):
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
    
    # self.animate = ft.animation.Animation(200, ft.AnimationCurve.EASE_IN)
    
    self.price = 0
    self.priceText = ft.Text(
      value=f"{self.price}$",
      size=18,
      weight=ft.FontWeight.W_700,
      color=constants.BLACK,
      text_align=ft.TextAlign.CENTER,
      overflow=ft.TextOverflow.ELLIPSIS,
    )
    
    self.priceContent = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Icon(
          name=ft.icons.ATTACH_MONEY_ROUNDED,
          size=32,
          color=constants.BLACK,
        ),
        ft.Text(
          value=f"Precio",
          size=18,
          text_align=ft.TextAlign.CENTER,
          overflow=ft.TextOverflow.ELLIPSIS,
          color=constants.BLACK,
        ),
        self.priceText,
      ]
    )
    
    self.content = self.priceContent
    
  def updatePriceText(self, newPrice):
    try:
      self.price = newPrice
      self.priceText.value = f"{self.price}$"
      self.update()
    except:
      pass
    
  def clickFunction(self):
    try:
      pass
    except:
      pass