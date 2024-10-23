import flet as ft
import constants
from Modules.customControls import CustomAlertDialog, CustomAnimatedContainer, CustomAnimatedContainerSwitcher, CustomOperationContainer, CustomTextField, CustomDropdown, CustomImageContainer, CustomFloatingActionButton, CustomFilledButton, CustomTooltip, CustomReturnButton, CustomEditButton
from Modules.transaction_module import TransactionForm
from utils.exchangeManager import getCurrentRate


class PaymentCard(ft.Container):
  def __init__(self, page, formContainer, height=160, width=160):
    super().__init__()
    self.page = page
    self.height = height
    self.width = width
    self.formContainer = formContainer
    
    self.bgcolor = constants.WHITE
    self.border = ft.border.all(2, constants.BLACK_GRAY)
    self.border_radius = 20
    self.padding = ft.padding.all(10)
    self.ink = True
    self.ink_color = constants.WHITE_GRAY
    self.on_click = lambda e: self.clickFunction()
    
    self.selectedPayments = []
    
    self.paymentAmountText = ft.Text(
      value=0,
      size=24,
      color=constants.GREEN_TEXT,
      weight=ft.FontWeight.W_700,
      overflow=ft.TextOverflow.ELLIPSIS,
    )
    
    self.withoutPayment = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Icon(
          name=ft.icons.PAYMENT_ROUNDED,
          size=40,
          color=constants.BLACK,
        ),
        ft.Text(
          value="Pagos",
          size=18,
          color=constants.BLACK,
          text_align=ft.TextAlign.CENTER,
          overflow=ft.TextOverflow.ELLIPSIS,
        )
      ]
    )
    
    self.withPayment = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Icon(
          name=ft.icons.PAYMENTS_ROUNDED,
          size=40,
          color=constants.BLACK,  
        ),
        ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          controls=[
            # ft.Text(
            #   value="Total:",
            #   size=18,
            #   color=constants.BLACK,
            # ),
            self.paymentAmountText,
          ]
        ),
      ]
    )
    
    self.animatedContainer = CustomAnimatedContainer(
      actualContent=self.withoutPayment
    )
    
    self.content = self.animatedContainer
    
  def clickFunction(self):
    try:
      newContent = PaymentManager(
        page=self.page,
        paymentCard=self,
        formContainer=self.formContainer,
        selectedPayments=self.selectedPayments,
      )
      
      self.formContainer.changeContent(newContent)
    except:
      raise
    
  def updateCard(self, payments:list=[]):
    try:
      self.selectedPayments = payments
      totalAmount = 0
      exchangeRate = getCurrentRate()
      
      for payment in self.selectedPayments:
        amount = payment["amount"]
        if payment["currency"] == "Bs":
          if exchangeRate:
            amount = payment["amount"]/exchangeRate
          else:
            print("No se ha establecido ninguna tasa.")
            totalAmount = 0
            dialog = ft.AlertDialog(
              title=ft.Text("No se ha establecido la tasa de intercambio."),
            )
            self.page.open(dialog)
            return
        totalAmount += amount
      
      self.paymentAmountText.value = f"{round(totalAmount,2)}$"
      
      if totalAmount > 0:
        self.animatedContainer.setNewContent(self.withPayment)
      else:
        self.animatedContainer.setNewContent(self.withoutPayment)
      print(totalAmount)
    except:
      raise
  

class PaymentManager(ft.Container):
  def __init__(self, page, paymentCard, formContainer, selectedPayments=[]):
    super().__init__()
    self.page = page
    self.paymentCard = paymentCard
    self.formContainer = formContainer
    self.selectedPayments = selectedPayments
    
    self.alignment = ft.alignment.center
    self.expand = True
    
    self.titleText = ft.Text(
      value="Pagos de la venta",
      size=32,
      color=constants.BLACK,
      weight=ft.FontWeight.W_700,
      text_align=ft.TextAlign.CENTER,
    )
    
    self.createPaymentButton = CustomEditButton(
      function=lambda e: self.showTransactionForm(),
    )
    self.createPaymentButton.content.name = ft.icons.ADD_CARD_ROUNDED
    
    self.paymentDefaultContainer = ft.Column(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Icon(
          name=ft.icons.CREDIT_CARD_OFF_OUTLINED,
          size=24,
          color=constants.BLACK,
        ),
        ft.Text(
          value="No se ha registrado ningún pago",
          size=18,
          color=constants.BLACK,
          text_align=ft.TextAlign.CENTER,
          overflow=ft.TextOverflow.ELLIPSIS,
        )
      ]
    )
    
    self.finishButton = CustomFilledButton(
      text="Finalizar",
      clickFunction=lambda e: self.finishFunction(),
    )
  
    self.animatedPaymentContainer = ft.Container(
      border=ft.border.all(2, constants.BLACK),
      padding=ft.padding.symmetric(horizontal=5, vertical=10),
      expand=True,
      border_radius=20,
      alignment=ft.alignment.center,
      content=CustomAnimatedContainer(
        actualContent=self.getPaymentsList() if len(self.selectedPayments) > 0 else self.paymentDefaultContainer
      )
    )
    
    self.columnMainContent = ft.Column(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      spacing=40,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          controls=[
            ft.Text(
              value="Agregar pago",
              size=18,
              color=constants.BLACK,
            ),
            self.createPaymentButton,
          ]
        ),
        self.animatedPaymentContainer,
        self.finishButton,
      ]
    )
    
    self.managerContent = ft.Column(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      spacing=40,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        self.titleText,
        self.columnMainContent,
      ]
    )
    
    self.animatedMainContainer = CustomAnimatedContainer(
      actualContent=self.managerContent,
    )
    
    self.content = self.animatedMainContainer
    
  def showTransactionForm(self):
    try:
      form = TransactionForm(
        page=self.page,
        previousContainer=self,
        transactionType="Payment",
      )
      
      form = ft.Stack(
        expand=True,
        controls=[
          form,
          ft.Container(
            left=10,
            top=10,
            content=CustomReturnButton(
              function=lambda e: self.returnToManager()
            )
          )
        ]
      )
      
      self.animatedMainContainer.setNewContent(form)
    except:
      raise
  
  def returnToManager(self):
    self.animatedMainContainer.setNewContent(self.managerContent)
  
  def getPaymentRecord(self, paymentInfo):
    try:
      paymentRecord = PaymentRecord(
        page=self.page,
        paymentInfo=paymentInfo,
        deleteFunction=self.removePaymentFromList,
      )
      
      return paymentRecord
    except:
      raise
  
  def addPaymentToList(self, paymentInfo):
    try:
      self.selectedPayments.append(paymentInfo)
    except:
      raise
  
  def removePaymentFromList(self, paymentInfo, paymentRecord):
    try:
      
      self.selectedPayments.remove(paymentInfo)
      self.animatedPaymentContainer.content.content.controls.remove(paymentRecord)
      
      if len(self.animatedPaymentContainer.content.content.controls) == 0:
        self.animatedPaymentContainer.content.setNewContent(self.paymentDefaultContainer)
      else:
        self.animatedPaymentContainer.content.update()
    except:
      raise
    
  def getPaymentsList(self):
    try:
      newContent = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        scroll=ft.ScrollMode.ALWAYS,
        controls=[]
      )
      
      for paymentInfo in self.selectedPayments:
        record = self.getPaymentRecord(paymentInfo)
        newContent.controls.append(record)
      
      return newContent
    except:
      raise
    
  def showPayments(self, paymentInfo=None):
    try:
      self.returnToManager()
        
      if paymentInfo:
        self.addPaymentToList(paymentInfo)
        
      self.animatedPaymentContainer.content.setNewContent(self.getPaymentsList())
    except:
      raise
    
  def finishFunction(self):
    try:
      self.formContainer.returnToBegin() 
      self.paymentCard.updateCard(payments=self.selectedPayments)
    except:
      raise
    
class PaymentRecord(ft.Container):
  def __init__(self, page, paymentInfo, deleteFunction=None):
    super().__init__()
    self.page = page
    self.paymentInfo = paymentInfo
    self.method = self.paymentInfo["method"]
    self.amount = self.paymentInfo["amount"]
    self.currency = self.paymentInfo["currency"]
    self.reference = self.paymentInfo["reference"]
    self.transactionType = self.paymentInfo["transactionType"]
    self.deleteFunction = deleteFunction
    
    self.shadow = ft.BoxShadow(
      spread_radius=1,
      blur_radius=1,
      color=constants.WHITE_GRAY,
    )
    self.bgcolor = constants.WHITE
    self.padding = ft.padding.symmetric(horizontal=10, vertical=20)
    self.border_radius = ft.border_radius.all(30)
    
    self.methodText = ft.Text(
      value=self.method,
      size=24,
      color=constants.BLACK,
      weight=ft.FontWeight.W_500,
      overflow=ft.TextOverflow.ELLIPSIS,
    )
    
    self.methodRow = ft.Row(
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Icon(
          name=constants.methodIcons[self.method],
          size=32,
          color=constants.BLACK
        ),
        self.methodText,
      ]
    )
    
    self.amountText = ft.Text(
      value=f"{self.amount}{self.currency}",
      size=28,
      weight=ft.FontWeight.W_700,
      color=constants.GREEN_TEXT if self.transactionType == "Payment" else constants.BLACK,
      overflow=ft.TextOverflow.ELLIPSIS,
    )
    
    if self.deleteFunction:
      self.deleteButton = CustomEditButton(
        function=lambda e: self.deleteFunction(paymentInfo=self.paymentInfo, paymentRecord=self),
      )
      self.deleteButton.content.name = ft.icons.DELETE_ROUNDED
    
    self.content = ft.Row(
      alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      expand=True,
      controls=[
        # ft.Column(
        #   controls=[
        #     self.methodText,
        #     self.transactionTypeText,
        #   ]
        # ),
        self.methodRow,
        ft.Row(
          vertical_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[self.amountText] if not self.deleteFunction else [self.amountText, self.deleteButton]
        ),
      ]
    )