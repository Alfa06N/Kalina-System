from exceptions import DataAlreadyExists, DataNotFoundError
import re
import flet as ft
import constants
from Modules.customControls import CustomAnimatedContainer, CustomOperationContainer, CustomUserIcon, CustomCardInfo, CustomDeleteButton, CustomReturnButton, CustomFilledButton, CustomOutlinedButton
from config import getDB
from DataBase.crud.transaction import getTransactionById
from Modules.Sections.SalesSection.components import SaleRecord

class PaymentInfo(ft.Container):
  def __init__(self, page, idTransaction, mainContainer):
    super().__init__()
    self.page = page
    self.idTransaction = idTransaction
    self.expand = True
    self.mainContainer = mainContainer
    
    self.alignment = ft.alignment.center
    
    with getDB() as db:
      transaction = getTransactionById(db, self.idTransaction)
      
      self.icon = ft.Icon(
        name=constants.methodIcons[transaction.method.value],
        size=48,
        color=constants.BLACK
      )
      
      self.titleMethod = ft.Text(
        value=transaction.method.value,
        size=28,
        weight=ft.FontWeight.W_600,
        color=constants.BLACK,
      )
      
      self.subtitleAmount = ft.Text(
        value=f"{round(transaction.amountUSD, 2)}$" if transaction.amountUSD else f"{round(transaction.amountVES, 2)}Bs",
        size=24,
        weight=ft.FontWeight.W_700,
        color=constants.GREEN_TEXT if transaction.transactionType == "Pago" else constants.RED_TEXT,
      )
      
      self.exchangeText = ft.Text(
        value=f"{round(transaction.exchangeRate, 3)}Bs",
        color=constants.ORANGE_TEXT,
        weight=ft.FontWeight.W_600,
        size=20,
      )
      
      self.referenceText = ft.Text(
        value=f"{transaction.reference}" if transaction.reference else "Sin referencia",
        color=constants.BLACK if transaction.reference else constants.BLACK_GRAY,
        size=20,
      )
      
      client = transaction.sale.client
      self.clientText = ft.Text(
        value=f"{client.name} {client.surname} {client.secondSurname}",
        color=constants.BLACK,
        size=20,
      )
      
      self.header = ft.Row(
        width=700,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          self.icon,
          ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=5,
            controls=[
              self.titleMethod,
              self.subtitleAmount,
            ]  
          ),
          ft.VerticalDivider(width=1, color=constants.BLACK_GRAY),
        ]
      )
      
      self.typeText = ft.Text(
        value=f"Vuelto" if transaction.transactionType == "Cambio" else f"Pago entrante",
        color=constants.BLACK,
        size=20,
      )
      
      self.body = ft.Column(
        controls=[
          ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
              ft.Text(
                value=f"Tipo de transacción:",
                color=constants.BLACK,
                weight=ft.FontWeight.W_600,
                size=20,
              ),
              self.typeText,
            ]
          ),
          ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
              ft.Text(
                value=f"Cliente:",
                color=constants.BLACK,
                weight=ft.FontWeight.W_600,
                size=20,
              ),
              self.clientText,
            ]
          ),
          ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
              ft.Text(
                value=f"Tasa de cambio:",
                color=constants.BLACK,
                weight=ft.FontWeight.W_600,
                size=20,
              ),
              self.exchangeText,
            ]
          ),
          ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
              ft.Text(
                value=f"Referencia:",
                color=constants.BLACK,
                weight=ft.FontWeight.W_600,
                size=20,
              ),
              self.referenceText,
            ]
          ),
        ]
      )
      
      self.showSaleButton = CustomOutlinedButton(
        text="Mostrar venta",
        clickFunction=self.showSale
      )
      
      self.content = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=30,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          self.header,
          ft.Divider(color=constants.WHITE_GRAY),
          self.body,
          self.showSaleButton
        ]
      )
  
  def showSale(self, e):
    with getDB() as db:
      newContent = SaleRecord(
        page=self.page,
        idSale=getTransactionById(db, self.idTransaction).sale.idSale,
      )
      
      self.mainContainer.showSale(newContent)