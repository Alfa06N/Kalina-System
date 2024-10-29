import flet as ft 
from Modules.customControls import CustomAnimatedContainer, CustomOperationContainer, CustomUserIcon, CustomCardInfo, CustomDeleteButton, CustomItemsSelector, CustomAnimatedContainerSwitcher, CustomFilledButton, CustomExchangeContainer, CustomAlertDialog
import constants
from DataBase.crud.product import getProducts
from DataBase.crud.combo import getCombos
from DataBase.crud.user import getUserByUsername
from DataBase.crud.sale import calculateSaleGain
from config import getDB
import threading
from exceptions import DataAlreadyExists, DataNotFoundError, InvalidData, ErrorOperation
import re
from Modules.Sections.SalesSection.clientCard import ClientCard
from Modules.Sections.SalesSection.paymentCard import PaymentCard
from Modules.Sections.SalesSection.changeCard import ChangeCard
from Modules.Sections.SalesSection.priceCard import PriceCard
from utils.exchangeManager import exchangeRateManager
from utils.saleManager import saleMakerManager
from utils.sessionManager import getCurrentUser

class SaleItemsList(CustomAnimatedContainerSwitcher):
  def __init__(self, page):
    self.page = page
    
    self.titleText = ft.Text(
      value="Carrito",
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
    saleMakerManager.setItemSelector(self.itemsSelector)
    
    self.content = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      expand=True,
      controls=[
        # ft.Row(
        #   alignment=ft.MainAxisAlignment.CENTER,
        #   vertical_alignment=ft.CrossAxisAlignment.CENTER,
        #   controls=[
        #     ft.Icon(
        #       name=ft.icons.ADD_SHOPPING_CART_ROUNDED,
        #       size=40,
        #       color=constants.BLACK,
        #     ),
        #     self.titleText,
        #   ]
        # ),
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
  def __init__(self, page):
    self.page = page
    
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
    
    self.exchangeRate = CustomExchangeContainer(
      page=self.page,
      rate=exchangeRateManager.getRate()
    )
    exchangeRateManager.subscribe(self.paymentCard)
    exchangeRateManager.subscribe(self.changeCard)
    exchangeRateManager.subscribe(self.priceCard)
    exchangeRateManager.subscribe(self.exchangeRate)

    self.cardsContainer = ft.Container(
      alignment=ft.alignment.center,
      height=300,
      width=800,
      expand=False,
      content=ft.Column(
        expand=True,
        controls=[
          ft.Row(
            expand=True,
            controls=[
              self.clientCard,
              ft.Column(
                expand=True,
                controls=[
                  ft.Row(
                    expand=True,
                    controls=[self.paymentCard]  
                  ),
                  ft.Row(
                    expand=True,
                    controls=[self.changeCard]  
                  ),
                ]
              )
            ]
          ),
          ft.Row(
            controls=[self.priceCard]
          )
        ]
      )
    )
    
    self.cardsContent = ft.Column(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        self.exchangeRate,
        self.cardsContainer,
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
        # ft.Text(
        #   value="Datos",
        #   size=42,
        #   color=constants.BLACK,
        #   weight=ft.FontWeight.W_700,
        # ),
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
      self.itemsSelector = saleMakerManager.itemsSelector
      
      user = getCurrentUser()
      if not user:
        raise DataNotFoundError("No se encontró el usuario de la sesión.")
      
      with getDB() as db:
        user = getUserByUsername(db, user)
      
      if self.itemsSelector.validateAllItemFields():
        
        validClient, ciClient, message = self.clientCard.validateCard()
        validPayments, selectedPayments, message = self.paymentCard.validateCard()
        selectedChanges = self.changeCard.selectedChanges
        price = self.priceCard.price
        
        sale, payments, changes, products, combos = saleMakerManager.makeSale(
          price=price,
          ciClient=ciClient,
          idUser=user.idUser,
          payments=selectedPayments,
          changes=selectedChanges,
        )

        saleContainer = saleMakerManager.saleContainer
        saleContainer.saleSuccessContent()
    except ErrorOperation as err:
      dialog = CustomAlertDialog(
        title="No es posible realizar la operación",
        content=ft.Text(
          value=err,
          size=18,
          color=constants.BLACK,
        ),
        modal=False,
      )
      self.page.open(dialog)
    except InvalidData as err:
      dialog = CustomAlertDialog(
        title="Venta sin completar",
        content=ft.Text(
          value=err,
          size=18,
          color=constants.BLACK,
        ),
        modal=False,
      )
      self.page.open(dialog)
    except DataNotFoundError as err:
      dialog = CustomAlertDialog(
        title="Algo salió mal",
        content=ft.Text(
          value=err,
          size=18,
          color=constants.BLACK
        ),
        modal=False,
      )
      self.page.open(dialog)
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