import flet as ft
import constants
from Modules.customControls import CustomAlertDialog, CustomAnimatedContainer, CustomAnimatedContainerSwitcher, CustomOperationContainer, CustomTextField, CustomDropdown, CustomImageContainer, CustomFloatingActionButton, CustomFilledButton, CustomTooltip, CustomNavigationOptions
from Modules.Sections.SalesSection.components import SaleItemsList, SaleForm
from utils.saleManager import saleMakerManager
from utils.exchangeManager import exchangeRateManager
from Modules.Sections.SalesSection.history_components import SaleHistory
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
      icon=ft.icons.NEW_LABEL_ROUNDED,
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
      icon=ft.icons.HISTORY_ROUNDED,
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
      bgcolor=ft.colors.TRANSPARENT,
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
    
    # self.itemsList = SaleItemsList(
    #   page=self.page,
    # )
    
    # self.saleForm = SaleForm(
    #   page=self.page,
    # )
    
    # # Reference to priceCard from saleForm to itemsList:
    # self.itemsList.itemsSelector.priceCard = self.saleForm.priceCard
    
    # self.registerContent = ft.Row(
    #   expand=True,
    #   controls=[
    #     self.itemsList,
    #     self.saleForm
    #   ]
    # )
    
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
        newContent = SaleHistory()
        
        self.mainContainer.setNewContent(newContent)
      else:
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
      )
      
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
      self.itemsList, self.saleForm, self.registerContent = self.createRegisterForm()
    except:
      raise
  
  def saleSuccessContent(self):
    try:
      newContent = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Text(
          value="¡Venta realizada!",
          color=constants.BLACK,
          weight=ft.FontWeight.W_700,
          size=42,
        )
      )
      self.mainContainer.setNewContent(newContent)
      
      self.resetRegisterForm()
      
      threading.Timer(1.5, self.showViewSelected).start()
    except:
      raise
  