import flet as ft
import constants
from Modules.customControls import CustomAlertDialog, CustomAnimatedContainer, CustomAnimatedContainerSwitcher, CustomOperationContainer, CustomTextField, CustomDropdown, CustomImageContainer, CustomFloatingActionButton, CustomFilledButton, CustomTooltip
import threading
import time
from utils.exchangeManager import exchangeRateManager
from exceptions import InvalidData

class PriceCard(ft.Container):
  def __init__(self, page, formContainer, height=80):
    super().__init__()
    self.page = page
    self.height = height
    self.formContainer = formContainer
    self.expand = True
    
    self.bgcolor = constants.WHITE
    self.border = ft.border.all(2, constants.BLACK_GRAY)
    self.border_radius = 20
    self.padding = ft.padding.all(10)
    self.ink = True
    self.ink_color = constants.WHITE_GRAY
    self.on_click = None
    
    self.price = 0.0
    self.exchange = 0.0
    
    self.priceText = ft.Text(
      value=f"{self.price}$",
      size=24,
      weight=ft.FontWeight.W_700,
      color=constants.GREEN_TEXT,
      text_align=ft.TextAlign.CENTER,
      overflow=ft.TextOverflow.ELLIPSIS,
    )
    
    self.exchangeText = ft.Text(
      value=f"{self.exchange}Bs",
      size=24,
      weight=ft.FontWeight.W_700,
      color=constants.ORANGE_TEXT,
      text_align=ft.TextAlign.CENTER,
      overflow=ft.TextOverflow.ELLIPSIS,
    )
    
    self.priceContent = ft.Row(
      alignment=ft.MainAxisAlignment.CENTER,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Icon(
          name=ft.icons.ATTACH_MONEY_ROUNDED,
          size=32,
          color=constants.BLACK,
        ),
        ft.Text(
          value=f"Dólares:",
          size=20,
          text_align=ft.TextAlign.CENTER,
          overflow=ft.TextOverflow.ELLIPSIS,
          color=constants.BLACK,
          weight=ft.FontWeight.W_600,
        ),
        self.priceText,
      ]
    )
    
    self.exchangeContent = ft.Row(
      alignment=ft.MainAxisAlignment.CENTER,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Icon(
          name=ft.icons.CURRENCY_EXCHANGE_ROUNDED,
          size=32,
          color=constants.BLACK,
        ),
        ft.Text(
          value="Bolívares:",
          size=20,
          text_align=ft.TextAlign.CENTER,
          overflow=ft.TextOverflow.ELLIPSIS,
          color=constants.BLACK,
          weight=ft.FontWeight.W_600,
        ),
        self.exchangeText,
      ]
    )
    
    self.content = ft.Row(
      alignment=ft.MainAxisAlignment.CENTER,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      spacing=50,
      controls=[
        self.priceContent,
        self.exchangeContent,
      ]
    )
    
  def updatePriceText(self, newPrice):
    try:
      self.price = float(newPrice)
      self.priceText.value = f"{self.price}$"
      if exchangeRateManager.getRate():
        self.exchange = float(exchangeRateManager.getRate())
        self.exchangeText.value = f"{round(self.exchange * self.price, 2)}Bs"
      self.update()
    except:
      raise
  
  def updateAboutRate(self, newRate):
    try:
      self.updatePriceText(self.price)
    except:
      raise