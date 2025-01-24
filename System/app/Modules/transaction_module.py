import flet as ft
from Modules.customControls import CustomPrincipalContainer, CustomSimpleContainer, CustomOperationContainer, CustomAnimatedContainer, CustomOutlinedButton, CustomImageSelectionContainer, CustomNumberField, CustomTooltip, CustomFilledButton, CustomTextField, CustomAutoComplete, CustomDropdown, CustomAlertDialog, CustomReturnButton, CustomItemsSelector, CustomNumberField
import constants
from config import getDB
from validation import evaluateForm
from DataBase.crud.client import createClient, getClientById, getClients
import threading
from exceptions import DataAlreadyExists, InvalidData, DataNotFoundError
from DataBase.models import MethodEnum
from utils.exchangeManager import exchangeRateManager

# Without save the transaction
class TransactionForm(CustomOperationContainer):
  def __init__(self, page, previousContainer, formContainer, transactionType:str="Payment", calculateChange=None):
    self.page = page
    self.previousContainer = previousContainer
    self.transactionType = transactionType
    self.formContainer = formContainer
    
    self.titleText = ft.Text(
      value="Crear Pago",
      size=42, 
      color=constants.BLACK,
      weight=ft.FontWeight.W_700,
      text_align=ft.TextAlign.CENTER,
    )
    
    self.amountUSDField = CustomTextField(
      label="Monto del pago (Dólares)",
      field="number",
      suffix_text="$",
      submitFunction=None,
      expand=True,
      on_changeFunction=self.onChangeFunctionUSD if self.transactionType == "Change" else None,
    )
    
    self.amountVESField = CustomTextField(
      label="Monto del pago (Bolívares)",
      field="number",
      suffix_text="Bs",
      submitFunction=None,
      expand=True,
      on_changeFunction=self.onChangeFunctionVES if self.transactionType == "Change" else None,
    )
    
    self.amountFieldContainer = ft.Container(
      expand=True,
      content=self.amountVESField,
    )
    
    self.methodField = CustomDropdown(
      label="Método",
      expand=True,
      options=[ft.dropdown.Option(method.value) for method in MethodEnum],
    )
    
    self.changeFieldButton = ft.IconButton(
      icon=ft.icons.CURRENCY_EXCHANGE_ROUNDED,
      icon_color=constants.BLACK,
      icon_size=32,
      on_click=lambda e: self.switchField(),
      tooltip="Cambiar moneda",
    )
    
    self.setChangeButton = ft.IconButton(
      icon=ft.Icons.FILE_UPLOAD_ROUNDED,
      icon_color=constants.BLACK,
      icon_size=32,
      on_click=lambda e: self.setChange(),
      tooltip="Establecer monto",
    )
    
    self.referenceField = CustomTextField(
      label="Referencia (Opcional)",
      field="others",
      hint_text=None,
      submitFunction=None,
      expand=True,
    )
    
    self.finishButton = CustomFilledButton(
      text="Finalizar",
      clickFunction=lambda e: self.submitFunction(),
    )
    
    self.operationContent = ft.Column(
      height=500,
      width=500,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        self.titleText,
        ft.Row(
          expand=True,
          vertical_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            self.amountFieldContainer,
            self.changeFieldButton,
            self.setChangeButton,
          ] if self.transactionType == "Change" else [
            self.amountFieldContainer,
            self.changeFieldButton,
          ]
        ),
        ft.Row(
          expand=True,
          vertical_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            self.methodField,
            self.referenceField,
          ]
        ),
        ft.Row(
          expand=True,
          alignment=ft.MainAxisAlignment.CENTER,
          controls=[
            self.finishButton
          ]
        )
      ]
    )
    super().__init__(operationContent=self.operationContent)
  
  def switchField(self):
    try:
      field = self.amountFieldContainer.content
      field.value = "0.00"
      self.amountFieldContainer.content = self.amountVESField if self.amountFieldContainer.content == self.amountUSDField else self.amountUSDField
      self.amountFieldContainer.update()
    except:
      raise
    
  def submitFunction(self):
    try:
      if evaluateForm(numbers=[self.amountFieldContainer.content], others=[self.methodField]):
        paymentInfo = {
          "currency": "$" if self.amountFieldContainer.content == self.amountUSDField else "Bs",
          "method": self.methodField.value,
          "amount": float(self.amountFieldContainer.content.value),
          "reference": None if self.referenceField.value == "" else self.referenceField.value,
          "transactionType": self.transactionType ,
        }
        
        self.previousContainer.showPayments(paymentInfo)
        return True
    except:
      raise
    
  def onChangeFunctionUSD(self):
    try:
      field = self.amountUSDField
      changePrice = round(self.formContainer.paymentCard.price - self.formContainer.priceCard.price - self.previousContainer.calculateTotal(), 2)
      if float(field.value) > changePrice:
        field.value = changePrice
        field.update()
    except:
      raise
  
  def onChangeFunctionVES(self):
    try:
      field = self.amountVESField
      changePrice = round((self.formContainer.paymentCard.price - self.formContainer.priceCard.price - self.previousContainer.calculateTotal()) * exchangeRateManager.getRate(), 2)
      if float(field.value) > changePrice:
        field.value = changePrice
        field.update()
    except:
      raise
  
  def setChange(self):
    try:
      field = self.amountFieldContainer.content
      price = self.formContainer.paymentCard.price - self.formContainer.priceCard.price - self.previousContainer.calculateTotal()
      field.value = round(price, 2) if field == self.amountUSDField else round(price * exchangeRateManager.getRate(), 2)
    
      self.amountFieldContainer.update()
    except:
      raise