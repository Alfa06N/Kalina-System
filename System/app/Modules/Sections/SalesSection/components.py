import flet as ft 
from Modules.customControls import CustomAnimatedContainer, CustomOperationContainer, CustomUserIcon, CustomCardInfo, CustomDeleteButton, CustomItemsSelector, CustomAnimatedContainerSwitcher, CustomFilledButton
import constants
from DataBase.crud.product import getProducts
from DataBase.crud.combo import getCombos
from config import getDB
import threading
from exceptions import DataAlreadyExists, DataNotFoundError, InvalidData
import re
from Modules.Sections.SalesSection.clientCard import ClientCard
from Modules.Sections.SalesSection.paymentCard import PaymentCard
from Modules.Sections.SalesSection.changeCard import ChangeCard
from Modules.Sections.SalesSection.priceCard import PriceCard

class SaleItemsList(CustomAnimatedContainerSwitcher):
  def __init__(self, page):
    self.page = page
    
    self.titleText = ft.Text(
      value="Selección",
      size=42,
      color=constants.BLACK,
      weight=ft.FontWeight.W_700,
      text_align=ft.TextAlign.CENTER,
      overflow=ft.TextOverflow.ELLIPSIS,
    )
    
    self.itemsSelector = CustomItemsSelector(
      page=self.page,
      products=True,
      combos=True,
      sale=True,
    )
    
    self.content = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      expand=True,
      controls=[
        self.titleText,
        self.itemsSelector
      ]
    )
    
    super().__init__(
      content=self.content,
      expand=True,
      height=None,
      width=None,
      margin=None,
    )

class SaleForm(CustomAnimatedContainerSwitcher):
  def __init__(self, page, itemsSelector=None):
    self.page = page
    self.itemsSelector = itemsSelector
    
    self.clientCard = ClientCard(
      page=self.page,
      formContainer=self,
    )
    
    self.paymentCard = PaymentCard(
      page=self.page,
      formContainer=self,
    )
    
    self.changeCard = ChangeCard(
      page=self.page,
      formContainer=self,
    )
    
    self.priceCard = PriceCard(
      page=self.page,
      formContainer=self,
    )
    
    self.cardsContent = ft.Column(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          controls=[
            self.clientCard,
            self.paymentCard,
          ]
        ),
        ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          controls={
            self.priceCard,
            self.changeCard,
          }
        ),
      ]
    )
    
    self.finishButton = CustomFilledButton(
      text="Realizar Venta",
      clickFunction=lambda e: self.makeSale()
    )
    
    self.formContent = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      expand=True,
      controls=[
        ft.Text(
          value="Datos",
          size=42,
          color=constants.BLACK,
          weight=ft.FontWeight.W_700,
        ),
        self.cardsContent,
        self.finishButton,
      ]
    )
    
    super().__init__(
      content=self.formContent,
      alignment=ft.alignment.center,
      expand=True,
      height=None,
      width=None,
      margin=None,
      padding=ft.padding.symmetric(horizontal=20, vertical=30)
    )
    
  def makeSale(self):
    try:
      if not self.itemsSelector:
        print("self.itemsSelector isn't defined to make a sale.")
        return
      
      if self.itemsSelector.validateAllItemFields():
        print("Sale validated.")
    except InvalidData as err:
      print(err)
    except:
      raise
    
  def changeContent(self, newContent):
    try:
      self.setNewContent(newContent)
    except:
      raise
    
  def returnToBegin(self):
    try:
      self.setNewContent(self.formContent)
    except:
      raise

class SaleSearchBar(ft.SearchBar):
  def __init__(self, page, controls:list=[], on_submit=None):
    super().__init__()
    self.view_elevation = 4
    self.bar_hint_text = "Buscar producto o combo..."
    self.view_hint_text = "Escribe o selecciona el producto/combo deseado..."
    self.controls = controls
    self.page = page
    
    self.on_submit = on_submit