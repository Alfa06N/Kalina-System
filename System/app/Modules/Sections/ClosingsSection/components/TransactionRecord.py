from exceptions import DataAlreadyExists, DataNotFoundError
import re
import flet as ft
import constants
from DataBase.crud.transaction import getTransactionById
from Modules.customControls import CustomReturnButton
from Modules.Sections.ClosingsSection.components.TransactionInfo import TransactionInfo

class TransactionRecord(ft.Container):
  def __init__(self, page, transactions, transactionType, method, amount:str , mainContainer, payments, changes):
    super().__init__()
    self.page = page
    self.transactionType = transactionType
    self.transactions = transactions
    self.payments = payments
    self.changes = changes
    self.method = method
    self.amount = amount
    self.mainContainer = mainContainer
    
    self.shadow = ft.BoxShadow(
      spread_radius=1,
      blur_radius=1,
      color=constants.WHITE_GRAY,
    )
    self.padding = ft.padding.all(10)
    self.margin = ft.margin.symmetric(horizontal=10, vertical=4)
    self.bgcolor = constants.WHITE
    self.border_radius = ft.border_radius.all(30)
    self.ink = True
    self.ink_color = constants.BLACK_INK
    self.on_click = lambda e: self.showNewContent()
    
    self.transactionMethodIcon = ft.Icon(
      name=constants.methodIcons[self.method],
      size=40,
      color=constants.BLACK
    )
    
    self.transactionAmount = ft.Text(
      value=f"{round(self.amount["total"], 2)}$",
      size=24,
      color=constants.GREEN_TEXT if round(self.amount["total"], 2) >= 0 else constants.RED_TEXT,
      weight=ft.FontWeight.W_500,
      overflow=ft.TextOverflow.ELLIPSIS,
      text_align=ft.TextAlign.START,
    )
    
    self.transactionMethodText = ft.Text(
      value=self.method,
      size=20,
      color=constants.BLACK,
      weight=ft.FontWeight.W_500,
      overflow=ft.TextOverflow.ELLIPSIS,
      text_align=ft.TextAlign.START,
    )
    
    self.content = ft.Row(
      alignment=ft.MainAxisAlignment.START,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      expand=True,
      controls=[
        self.transactionMethodIcon,
        ft.Column(
          alignment=ft.MainAxisAlignment.CENTER,
          horizontal_alignment=ft.CrossAxisAlignment.START,
          spacing=0,
          controls=[
            self.transactionAmount,
            self.transactionMethodText,
          ]
        )
      ]
    )
    
  def showNewContent(self):
    newContent = TransactionInfo(
      page=self.page,
      transactions=self.transactions,
      payments=self.payments,
      changes=self.changes,
      totalAmount=self.amount,
      mainContainer=self.mainContainer
    )
    
    self.mainContainer.changeContent(newContent, self.method)