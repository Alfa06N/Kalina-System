import flet as ft
import constants
from Modules.customControls import CustomAnimatedContainer, CustomAnimatedContainerSwitcher,CustomNavigationOptions
from Modules.Sections.PaymentsSection.components.PaymentContainer import PaymentContainer
from DataBase.crud.transaction import getTransactions
from config import getDB

class Payments(ft.ResponsiveRow):
  def __init__(self, page):
    super().__init__()
    self.expand = True
    self.page = page
    self.alignment = ft.MainAxisAlignment.CENTER
    self.vertical_alignment = ft.CrossAxisAlignment.CENTER
    self.run_spacing=10
    
    self.infoContainer = CustomAnimatedContainerSwitcher(
      content=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          self.textForEmptyContainer("There's nothing to show you here either")
        ]
      ),
      expand=True,
      col={"sm": 12, "md": 12, "lg": 8, "xl": 8}
    )
    
    self.paymentsContainer = CustomAnimatedContainerSwitcher(
      padding=0,
      alignment=ft.alignment.center,
      shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=5,
        color=constants.BLACK_INK,
      ),
      content=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=self.getPaymentContainers()
      ),
      height=None,
      width=None,
      expand=True,
      col={"sm": 12, "md": 9, "lg": 4, "xl": 4}
    )
    
    self.controls = [
      self.paymentsContainer,
      self.infoContainer
    ]
    
  def textForEmptyContainer(self, message):
    return ft.Text(
      value=message,
      size=32,
      color=constants.BLACK,
      weight=ft.FontWeight.W_700,
      text_align=ft.TextAlign.CENTER,
    )
  
  def getPaymentContainers(self):
    containers = []
    with getDB() as db:
      transactions = getTransactions(db)
      if transactions:
        for transaction in transactions:
          container = PaymentContainer(
            page=self.page,
            transactionType=transaction.transactionType,
            idTransaction=transaction.idTransaction,
            method=transaction.method.value,
            amount=f"{round(transaction.amountUSD, 2)}$" if transaction.amountUSD else f"{round(transaction.amountVES, 2)}Bs",
            infoContainer=self.infoContainer,
            mainContainer=self
          )
          
          containers.append(container)
    return containers
  