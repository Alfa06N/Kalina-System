from exceptions import DataAlreadyExists, DataNotFoundError
import re
import flet as ft
import constants
from Modules.Sections.PaymentsSection.components.PaymentInfo import PaymentInfo

class PaymentContainer(ft.Container):
  def __init__(self, page, idTransaction, transactionType, method, amount:str , infoContainer, mainContainer):
    super().__init__()
    self.page = page
    self.idTransaction = idTransaction
    self.transactionType = transactionType
    self.method = method
    self.amount = amount
    self.infoContainer = infoContainer
    self.mainContainer = mainContainer
    
    self.shadow = ft.BoxShadow(
      spread_radius=1,
      blur_radius=1,
      color=constants.WHITE_GRAY,
    )
    self.padding = ft.padding.all(10)
    self.bgcolor = constants.WHITE
    self.border_radius = ft.border_radius.all(30)
    self.ink = True
    self.ink_color = constants.BLACK_INK
    self.on_click = self.showPaymentInfo
  
    self.transactionMethodIcon = ft.Icon(
      name=constants.methodIcons[self.method],
      size=40,
      color=constants.BLACK
    )
    
    self.transactionAmount = ft.Text(
      value=self.amount,
      size=24,
      color=constants.GREEN_TEXT if self.transactionType == "Payment" else constants.RED_TEXT,
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
  
  def showPaymentInfo(self, e):
    newContent = PaymentInfo(
      page=self.page,
      idTransaction=self.idTransaction,
    )
    
    if self.infoContainer.height <= 150:
      self.infoContainer.changeStyle(
        height=300,
        width=700,
        shadow=ft.BoxShadow(
          blur_radius=5,
          spread_radius=1,
          color=constants.WHITE_GRAY,
        )
      )
    self.infoContainer.setNewContent(
      newContent=newContent
    )