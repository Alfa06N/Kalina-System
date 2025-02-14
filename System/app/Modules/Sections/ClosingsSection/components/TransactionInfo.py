from exceptions import DataAlreadyExists, DataNotFoundError
import re
import flet as ft
import constants
from Modules.customControls import CustomAnimatedContainer, CustomOperationContainer, CustomUserIcon, CustomCardInfo, CustomDeleteButton, CustomReturnButton
from config import getDB
from DataBase.crud.transaction import getTransactionById
from DataBase.crud.sale import getSaleById
from Modules.Sections.PaymentsSection.components.PaymentContainer import PaymentContainer

class TransactionInfo(ft.Container):
  def __init__(self, page, transactions, payments, changes, totalAmount, mainContainer):
    super().__init__()
    self.page = page
    self.transactions = transactions
    self.payments = payments
    self.changes = changes
    self.totalAmount = totalAmount
    self.mainContainer = mainContainer
    
    with getDB() as db:
      self.transactionObjects = [getTransactionById(db, transaction) for transaction in self.transactions]
      
      self.transactionComponents = [
        PaymentContainer(
          page=self.page,
          transactionType=transaction.transactionType,
          method=transaction.method.value,
          amount=f"{round(transaction.amountUSD, 2)}$" if transaction.amountUSD else f"{round(transaction.amountVES, 2)}Bs",
          infoContainer=None,
          mainContainer=self.mainContainer,
          idTransaction=transaction.idTransaction,
        ) for transaction in self.transactionObjects
      ]
      
      self.paymentAmount = ft.Text(
        value=f"{round(payments, 2)}$",
        size=28,
        color=constants.GREEN_TEXT,
        weight=ft.FontWeight.W_700,
      )
      
      
      self.changeAmount = ft.Text(
        value=f"{round(changes, 2)}$",
        size=28,
        color=constants.RED_TEXT,
        weight=ft.FontWeight.W_700,
      )
      
      self.content = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            controls=[
              ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                height=80,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                  ft.Text(
                    value="Efectivo:",
                    color=constants.BLACK,
                    size=28,
                    weight=ft.FontWeight.W_700,
                  ),
                  ft.Text(
                    value=f"{round(self.totalAmount["total"], 2)}$",
                    color=constants.GREEN_TEXT if round(self.totalAmount["total"], 2) >= 0 else constants.RED_TEXT,
                    size=28,
                    weight=ft.FontWeight.W_700,
                  ),
                ]
              ),
              ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                controls=self.transactionComponents
              )
            ]
          ),
        ]
      )
    
  def showFurtherInfo(self, newContent):
    self.oldContent = self.mainContainer.content.content
    
    newContent = ft.Stack(
      expand=True,
      controls=[
        newContent,
        ft.Container(
          top=0,
          left=0,
          border_radius=5,
          bgcolor=constants.WHITE,
          content=CustomReturnButton(
            function=lambda e: self.mainContainer.content.setNewContent(self.oldContent)
          ),
        )
      ]
    )
    
    self.mainContainer.content.setNewContent(newContent)
    print(self.mainContainer.content.content)