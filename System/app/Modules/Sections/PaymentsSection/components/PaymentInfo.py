from exceptions import DataAlreadyExists, DataNotFoundError
import re
import flet as ft
import constants
from Modules.customControls import CustomAnimatedContainer, CustomOperationContainer, CustomUserIcon, CustomCardInfo, CustomDeleteButton, CustomReturnButton
from config import getDB
from DataBase.crud.transaction import getTransactionById

class PaymentInfo(ft.Container):
  def __init__(self, page, idTransaction):
    super().__init__()
    self.page = page
    self.idTransaction = idTransaction
    self.expand = True
    
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
        weight=ft.FontWeight.W_700,
        color=constants.BLACK,
      )
      
      self.subtitleAmount = ft.Text(
        value=f"{round(transaction.amountUSD, 2)}$" if transaction.amountUSD else f"{round(transaction.amountVES, 2)}Bs",
        size=24,
        weight=ft.FontWeight.W_700,
        color=constants.GREEN_TEXT if transaction.transactionType == "Payment" else constants.RED_TEXT,
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
        ]
      )
      
      self.typeText = ft.Text(
        value=f"Tipo de transacción: Vuelto" if transaction.transactionType == "Change" else f"Tipo de transacción: Pago entrante",
        color=constants.BLACK,
        size=20,
      )
      
      self.body = ft.Column(
        
      )
      
      self.content = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          self.header,
          ft.Divider(color=constants.WHITE_GRAY),
          self.typeText
          # ft.Row(
          #   alignment=ft.MainAxisAlignment.CENTER,
          #   controls=[
          #     ft.Icon(
          #       name=ft.Icons.QUESTION_MARK,
          #       color=constants.BLACK,
          #       size=24,
          #     ),
          #     self.typeText,
          #   ]
          # )
        ]
      )