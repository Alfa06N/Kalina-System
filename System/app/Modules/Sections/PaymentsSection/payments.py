import flet as ft
import constants
from Modules.customControls import CustomAnimatedContainer, CustomAnimatedContainerSwitcher,CustomNavigationOptions
from Modules.Sections.PaymentsSection.components.PaymentContainer import PaymentContainer
from DataBase.crud.transaction import getTransactions, getTransactionsFiltered
from DataBase.models import MethodEnum
from config import getDB
from Modules.Sections.PaymentsSection.components.MethodContainer import MethodContainer

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
        spacing=0,
        controls=[
          self.textForEmptyContainer("Selecciona un método de pago para ver los detalles")
        ]
      ),
      expand=True,
      col={"sm": 12, "md": 12, "lg": 8, "xl": 8}
    )
    
    self.paymentsContainer = CustomAnimatedContainerSwitcher(
      padding=ft.padding.symmetric(horizontal=5),
      alignment=ft.alignment.center,
      content=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=self.getMethodContainers()
      ),
      height=None,
      width=None,
      expand=True,
      col={"sm": 12, "md": 9, "lg": 4, "xl": 4}
    )
    
    self.selected = None
    
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

  def getMethodContainers(self):
    containers = []
    for method in MethodEnum:
      container = MethodContainer(
        page=self.page,
        method=method.value,
        on_click=lambda e, method=method.value: self.selectMethod(e.control, method)
      )
      containers.append(container)
    
    additionalContainer = MethodContainer(
      page=self.page,
      method="All",
      on_click=lambda e, method="All": self.selectMethod(e.control, method)
    )
    additionalContainer.margin = ft.margin.only(bottom=30)
    
    containers.insert(0, additionalContainer)
    return containers
  
  def selectMethod(self, container, method):
    if not self.selected == container:
      container.selectContainer()
      if self.selected:
        self.selected.deselectContainer()
        self.selected = container
      else:
        self.selected = container
    
      self.showDataFiltered(method)

  def showDataFiltered(self, method):
    containers = []
    
    with getDB() as db:
      transactions = getTransactionsFiltered(db, method)

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

    newContent = ft.Column(
      scroll=ft.ScrollMode.AUTO,
      spacing=0,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=containers if len(containers) > 0 else [self.textForEmptyContainer(f"No hay pagos por este método registrados en el sistema")],
    )
    
    if self.infoContainer.height < 800:
      self.infoContainer.changeStyle(
        height=800,
        width=700,
        shadow=ft.BoxShadow(
          blur_radius=5,
          spread_radius=1,
          color=constants.BLACK_INK,
        )
      )
    self.infoContainer.setNewContent(
      newContent=newContent
    )
  
  def showFurtherInfo(self, content):
    self.oldContent = self.infoContainer.content.content
    self.infoContainer.setNewContent(
      newContent=content
    )
  
  def showLessInfo(self):
    self.infoContainer.setNewContent(
      newContent=self.oldContent
    )