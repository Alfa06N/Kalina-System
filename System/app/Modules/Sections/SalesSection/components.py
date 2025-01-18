import flet as ft 
from Modules.customControls import CustomAnimatedContainer, CustomOperationContainer, CustomUserIcon, CustomCardInfo, CustomDeleteButton, CustomItemsSelector, CustomAnimatedContainerSwitcher, CustomFilledButton, CustomExchangeContainer, CustomAlertDialog, CustomExpansionTile, CustomListTile, CustomTextButton
import constants
from DataBase.crud.product import getProducts
from DataBase.crud.combo import getCombos
from DataBase.crud.user import getUserByUsername
from DataBase.crud.sale import calculateSaleGain, getSaleById
from config import getDB
from utils.dateConversions import convertToLocalTz
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
from datetime import datetime
from utils.inventoryManager import inventoryManager

class SaleItemsList(CustomAnimatedContainerSwitcher):
  def __init__(self, page):
    self.page = page
    
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
    
    exchangeRateManager.subscribe([self.paymentCard, self.changeCard, self.priceCard, self.exchangeRate])
    # exchangeRateManager.subscribe(self.paymentCard)
    # exchangeRateManager.subscribe(self.changeCard)
    # exchangeRateManager.subscribe(self.priceCard)
    # exchangeRateManager.subscribe(self.exchangeRate)

    self.cardsContainer = ft.Container(
      alignment=ft.alignment.center,
      height=250,
      width=800,
      expand=False,
      content=ft.Column(
        expand=True,
        controls=[
          ft.Row(
            expand=2,
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
            expand=1,
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
      clickFunction=lambda e: self.ConfirmToMakeSale(),
    )
    
    self.formContent = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      expand=True,
      controls=[
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
    
  def ConfirmToMakeSale(self):
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
        
        self.dialog = CustomAlertDialog(
          title="Confirmar acción",
          content=ft.Text(
            value="¿Estás seguro de concretar esta venta?",
            size=18,
            color=constants.BLACK,
          ),
          modal=True,
          actions=[
            CustomTextButton(text="Confirmar", on_click=lambda e: self.makeSale(ciClient=ciClient, selectedPayments=selectedPayments, idUser=user.idUser)),
            CustomTextButton(text="Cancelar", on_click=lambda e: self.page.close(self.dialog))
          ]
        )
        
        self.page.open(self.dialog)
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
    
  def makeSale(self, ciClient, selectedPayments, idUser):
    try:
      self.page.close(self.dialog)

      selectedChanges = self.changeCard.selectedChanges
      price = self.priceCard.price
        
      idSale, payments, changes, products, combos = saleMakerManager.makeSale(
        price=price,
        ciClient=ciClient,
        idUser=idUser,
        payments=selectedPayments,
        changes=selectedChanges,
      )

      saleContainer = saleMakerManager.saleContainer
      saleContainer.saleSuccessContent(idSale=idSale)
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

class SaleSuccess(ft.Container):
  def __init__(self):
    super().__init__()

class SaleRecord(ft.Container):
  def __init__(self, page, idSale):
    super().__init__()
    self.idSale = idSale
    self.border_radius = 20
    self.padding = ft.padding.symmetric(horizontal=10, vertical=20)
    self.expand = True
    
    with getDB() as db:
      sale = getSaleById(db, self.idSale)
      
      payments = [transaction for transaction in sale.transactions if transaction.transactionType == "Payment"]
      changes = [transaction for transaction in sale.transactions if transaction.transactionType == "Changes"]
      products = [register.product for register in sale.products]
      combos = [register.combo for register in sale.combos]
      client = sale.client
      user = sale.user
      exchangeRate = sale.transactions[0].exchangeRate
      
      self.titleText = ft.Text(
        value="Datos de Venta",
        size=32,
        color=constants.BLACK,
        weight=ft.FontWeight.W_700,
        text_align=ft.TextAlign.CENTER,
      )
      
      self.priceText = ft.Container(
        padding=ft.padding.symmetric(vertical=20, horizontal=10),
        width=500,
        border_radius=20,
        bgcolor=constants.WHITE,
        border=ft.border.all(4, constants.BLACK_GRAY),
        alignment=ft.alignment.center,
        content=ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          vertical_alignment=ft.CrossAxisAlignment.CENTER,
          spacing=40,
          controls=[
            ft.Text(
              value=f"{round(sale.totalPrice, 2)} $",
              color=constants.GREEN_TEXT,
              weight=ft.FontWeight.W_700,
              size=24,
            ),
            ft.Text(
              value=f"{round(sale.totalPrice * exchangeRate, 2)} Bs",
              color=constants.ORANGE_TEXT,
              weight=ft.FontWeight.W_700,
              size=24,
            )
          ]
        )
      )
      
      self.dateText = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          ft.Text(
            value="Fecha:",
            color=constants.BLACK,
            weight=ft.FontWeight.W_600,
            size=20,
          ),
          ft.Text(
            value=convertToLocalTz(sale.date).strftime("%d/%m/%Y"),
            color=constants.BLACK,
            size=20,
          ),
        ]
      )
      
      self.operationText = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          ft.Text(
            value="Número de operación:",
            color=constants.BLACK,
            weight=ft.FontWeight.W_600,
            size=20,
          ),
          ft.Text(
            value=sale.idSale,
            color=constants.BLACK,
            size=20,
          ),
        ]
      )
      
      self.clientText = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          ft.Text(
            value="Documento de cliente:",
            color=constants.BLACK,
            weight=ft.FontWeight.W_600,
            size=20,
          ),
          ft.Text(
            value=f"V-{client.ciClient}",
            color=constants.BLACK,
            size=20,
          ),
        ]
      )
      
      self.userText = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          ft.Text(
            value="Usuario a cargo:",
            color=constants.BLACK,
            weight=ft.FontWeight.W_600,
            size=20,
          ),
          ft.Text(
            value=user.username,
            color=constants.BLACK,
            size=20,
          ),
        ]
      )
      
      self.productsListTiles = []
      for register in sale.products:
        self.productsListTiles.append(CustomListTile(
          title=register.product.name,
          subtitle=ft.Text(
            value=f"Cantidad vendida: {register.productQuantity} unidades.",
            color=constants.BLACK,
            size=18,
          ),
          leading=None,
        ))
      self.productsText = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        controls=[
          ft.Row(
            controls=[
              ft.Text(
                value="Productos:",
                color=constants.BLACK,
                weight=ft.FontWeight.W_600,
                size=20,
              ),
            ]
          ),
          ft.Column(
            controls=[ft.Text(
              value=f"◆ {register.product.name} • {register.productQuantity} unidades",
              color=constants.BLACK,
              size=20,
            ) for register in sale.products] if sale.products else [ft.Text(
              value=f"No se vendieron productos",
              color=constants.BLACK_GRAY,
              size=20,
            )],
          )
        ]
      )
      
      self.combosText = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        controls=[
          ft.Row(
            controls=[
              ft.Text(
                value="Combos:",
                color=constants.BLACK,
                weight=ft.FontWeight.W_600,
                size=20,
              )
            ]  
          ),
          ft.Column(
            controls=[ft.Text(
              value=f"◆ {register.combo.name} • {register.comboQuantity} unidades",
              color=constants.BLACK,
              size=20,
            ) for register in sale.combos] if sale.combos else [ft.Text(
              value=f"No se vendieron combos",
              color=constants.BLACK_GRAY,
              size=20,
            )]
          )
        ]
      )
      
      self.paymentsText = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        controls=[
          ft.Row(
            controls=[
              ft.Text(
                value="Pagos:",
                color=constants.BLACK,
                weight=ft.FontWeight.W_600,
                size=20,
              )
            ]  
          ),
          ft.Column(
            controls=[ft.Row(
              controls=[
                ft.Icon(
                  name=constants.methodIcons[payment.method.value],
                  color=constants.BLACK,
                  size=24,
                ),
                ft.Text(
                  value=f"{payment.method.value}: {round(payment.amountUSD, 2)} $" if payment.amountUSD else f"{payment.method.value}: {round(payment.amountVES, 2)} Bs",
                  color=constants.BLACK,
                  size=20,
                )
              ]
            ) for payment in payments]  
          ),
        ]
      )
      
      self.changesText = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        controls=[
          ft.Row(
            controls=[
              ft.Text(
                value="Vueltos:",
                color=constants.BLACK,
                weight=ft.FontWeight.W_600,
                size=20,
              )
            ]  
          ),
          ft.Column(
            controls=[ft.Row(
              controls=[
                ft.Icon(
                  name=constants.methodIcons[payment.method.value],
                  color=constants.BLACK,
                  size=24,
                ),
                ft.Text(
                  value=f"{payment.method.value}: {round(payment.amountUSD, 2)} $" if payment.amountUSD else f"{payment.method.value}: {round(payment.amountVES, 2)} Bs",
                  color=constants.BLACK,
                  size=20,
                )
              ]
            ) for payment in changes] if changes else [ft.Text(
              value="No se registró ningún vuelto",
              color=constants.BLACK_GRAY,
              size=20,
            )]
          ),
        ]
      )

    self.content = ft.Column(
      expand=True,
      scroll=ft.ScrollMode.AUTO,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      spacing=25,
      controls=[
        self.titleText,
        self.priceText,
        ft.Container(
          content=ft.Column(
            expand=True,
            spacing=20,
            controls=[
              self.dateText,
              self.operationText,
              self.clientText,
              self.userText,
              self.productsText,
              self.combosText,
              self.paymentsText,
              self.changesText,
            ]  
          ), 
        ),
      ]
    )