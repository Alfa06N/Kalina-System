import flet as ft
import constants
from Modules.customControls import CustomAlertDialog, CustomAnimatedContainer, CustomAnimatedContainerSwitcher, CustomOperationContainer, CustomTextField, CustomDropdown, CustomImageContainer, CustomFloatingActionButton, CustomFilledButton, CustomTooltip, CustomReturnButton, CustomEditButton, CustomExchangeDialog
from Modules.transaction_module import TransactionForm
from utils.exchangeManager import exchangeRateManager
from Modules.Sections.SalesSection.paymentCard import TransactionManager
from exceptions import InvalidData

class ChangeCard(ft.Container):
  def __init__(self, page, formContainer, height=140, width=140):
    super().__init__()
    self.page = page
    self.formContainer = formContainer
    self.expand = True
    
    self.bgcolor = constants.WHITE
    self.border = ft.border.all(2, constants.BLACK_GRAY)
    self.border_radius = 20
    self.padding = ft.padding.all(10)
    self.ink = True
    self.ink_color = constants.WHITE_GRAY
    self.on_click = lambda e: self.clickFunction()
    
    self.price = 0
    
    self.selectedChanges = []
    
    self.changeAmountText = ft.Text(
      value=0,
      size=20,
      color=constants.RED_TEXT,
      weight=ft.FontWeight.W_700,
      overflow=ft.TextOverflow.ELLIPSIS,
    )
    
    self.withoutChange = ft.Row(
      alignment=ft.MainAxisAlignment.CENTER,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Icon(
          name=ft.Icons.CHANGE_CIRCLE_OUTLINED,
          size=32,
          color=constants.RED_TEXT,
        ),
        ft.Text(
          value=f"Agregar vueltos",
          size=20,
          color=constants.BLACK,
          text_align=ft.TextAlign.CENTER,
          overflow=ft.TextOverflow.ELLIPSIS,  
        ),
      ]
    )
    
    self.withChange = ft.Row(
      alignment=ft.MainAxisAlignment.CENTER,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Icon(
          name=ft.Icons.OUTPUT_OUTLINED,
          size=32,
          color=constants.RED_TEXT,
        ),
        ft.Text(
          value="Monto total:",
          color=constants.BLACK,
          size=20,
        ),
        self.changeAmountText,
      ]
    )
    
    self.animatedContainer = CustomAnimatedContainer(
      actualContent=self.withoutChange
    )
    
    self.content = ft.Column(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      controls=[
        self.animatedContainer
      ]  
    )
    
  def clickFunction(self):
    try:
      if self.formContainer.priceCard.price >= self.formContainer.paymentCard.price:
        raise InvalidData("El monto de la venta es mayor o igual al monto de los pagos entrantes.")
      exchangeRate = exchangeRateManager.getRate()
      
      if exchangeRate:
        newContent = TransactionManager(
          page=self.page,
          paymentCard=self,
          formContainer=self.formContainer,
          selectedPayments=self.selectedChanges,
          transactionType="Cambio"
        )
        
        self.formContainer.changeContent(newContent)
      else:
        dialog = CustomExchangeDialog(page=self.page)
        self.page.open(dialog)
    except InvalidData as e:
      dialog = CustomAlertDialog(
        title="No hay necesidad de agregar vueltos",
        content=ft.Text(
          value=str(e),
          color=constants.BLACK,
          size=20,
        ),
        modal=False
      )
      self.page.open(dialog)
    except:
      raise
    
  def calculateTotal(self):
    try:
      exchangeRate = exchangeRateManager.getRate()
      self.price = 0
      if exchangeRate:
        for change in self.selectedChanges:
          amount = change["amount"]
          if change["currency"] == "Bs":
            amount = change["amount"]/exchangeRate
          self.price += amount
      self.price = round(self.price, 2)
      return self.price
    except:
      raise
    
  def calculateChange(self):
    try:
      total = self.calculateTotal()
      print(f"Total: {self.calculateTotal()}")
      print(f"Now: {round(self.formContainer.calculateTotalChange(), 2) - total}")
      return round(self.formContainer.calculateTotalChange(), 2) - total
    except:
      raise
    
  def resetChangeCard(self):
    try:
      self.selectedChanges = []
      self.updateCard()
    except:
      raise
    
  def updateCard(self, transactions:list=[]):
    try:
      self.calculateTotal()
      
      self.changeAmountText.value = f"{round(self.price, 2)}$"
      
      if self.price > 0:
        self.animatedContainer.setNewContent(self.withChange)
      else:
        self.animatedContainer.setNewContent(self.withoutChange)
    except:
      raise
    
  def updateAboutRate(self, newRate):
    try:
      self.updateCard(self.selectedChanges)
    except:
      raise