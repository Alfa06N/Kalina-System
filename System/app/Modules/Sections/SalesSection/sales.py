import flet as ft
import constants
from Modules.customControls import CustomAlertDialog, CustomAnimatedContainer, CustomAnimatedContainerSwitcher, CustomOperationContainer, CustomTextField, CustomDropdown, CustomImageContainer, CustomFloatingActionButton, CustomFilledButton, CustomTooltip, CustomNavigationOptions
from Modules.Sections.SalesSection.components import SaleItemsList, SaleForm, SaleRecord
from utils.saleManager import saleMakerManager
from utils.exchangeManager import exchangeRateManager
from Modules.Sections.SalesSection.sale_history import SaleHistory
import threading

class Sales(ft.Column):
  def __init__(self, page):
    super().__init__()
    self.expand = True
    self.page = page
    self.alignment = ft.MainAxisAlignment.CENTER
    self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    self.spacing = 0
    
    self.newSaleButton = CustomNavigationOptions(
      icon=ft.Icons.NEW_LABEL_ROUNDED,
      text="Nueva Venta",
      function=lambda e: self.selectView(self.newSaleButton),
      color="#666666",
      focusedColor=constants.BLACK,
      opacityInitial=1,
      highlightColor=None,
      contentAlignment=ft.MainAxisAlignment.CENTER,
      default=True,
    )
    
    self.historySaleButton = CustomNavigationOptions(
      icon=ft.Icons.HISTORY_ROUNDED,
      text="Historial",
      function=lambda e: self.selectView(self.historySaleButton),
      color="#666666",
      focusedColor=constants.BLACK,
      opacityInitial=1,
      highlightColor=None,
      contentAlignment=ft.MainAxisAlignment.CENTER,
    )
    
    self.topNavigationBar = ft.Container(
      margin=ft.margin.symmetric(horizontal=20, vertical=10),
      bgcolor=ft.Colors.TRANSPARENT,
      height=60,
      width=600,
      content=ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        spacing=20,
        controls=[
          self.newSaleButton,
          self.historySaleButton,
        ]
      )
    )
    
    self.selected = self.newSaleButton
    
    self.itemsList, self.saleForm, self.registerContent = self.createRegisterForm()
    
    self.mainContainer = CustomAnimatedContainerSwitcher(
      content=self.registerContent,
      shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=5,
        color=constants.WHITE_GRAY,
      ),
      padding=None,
      expand=True,
      height=None,
      width=None
    )
    
    self.controls = [
      self.topNavigationBar,
      self.mainContainer,
    ]
    
    saleMakerManager.setSaleContainer(self)
    
  def selectView(self, button):
    if not self.selected == button:
      self.selected.deselectOption()
      self.selected = button
      self.selected.selectOption()
      self.showViewSelected()
    
  def showViewSelected(self):
    try:
      if self.selected == self.historySaleButton:
        newContent = SaleHistory(
          page=self.page
        )
        
        self.mainContainer.setNewContent(newContent)
      else:
        self.itemsList, self.saleForm, self.registerContent = self.createRegisterForm()
        self.mainContainer.setNewContent(self.registerContent)
    except:
      raise
  
  def createRegisterForm(self):
    try:
      exchangeRateManager.clearSubscribers()

      self.itemsList = SaleItemsList(
        page=self.page,
      )
      
      self.saleForm = SaleForm(
        page=self.page,
        mainContainer=self,
      )
      
      saleMakerManager.setItemSelector(self.itemsList.itemsSelector)
      
      self.itemsList.itemsSelector.priceCard = self.saleForm.priceCard
      
      self.registerContent = ft.Row(
        expand=True,
        controls=[
          self.itemsList,
          self.saleForm
        ]
      )
      
      return self.itemsList, self.saleForm, self.registerContent
    except:
      raise
  
  def resetRegisterForm(self):
    try:
      exchangeRateManager.clearSubscribers()
      self.itemsList, self.saleForm, self.registerContent = self.createRegisterForm()
    except:
      raise
  
  def saleSuccessContent(self, idSale):
    try:
      saleRecord = SaleRecord(
        page=self.page,
        idSale=idSale,
      )
      
      def finishAction():
        self.showViewSelected()
        self.resetRegisterForm()
      
      newContent = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Row(
          expand=True,
          alignment=ft.MainAxisAlignment.CENTER,
          vertical_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            ft.Column(
              expand=True,
              alignment=ft.MainAxisAlignment.CENTER,
              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
              spacing=20,
              controls=[
                ft.Text(
                  value="¡Venta realizada!",
                  color=constants.BLACK,
                  weight=ft.FontWeight.W_700,
                  size=42,
                ),
                CustomFilledButton(
                  text="Finalizar",
                  clickFunction=lambda e: finishAction(),
                )
              ]
            ),
            saleRecord,
          ]
        )
      )
      
      self.mainContainer.setNewContent(newContent)
    except:
      raise