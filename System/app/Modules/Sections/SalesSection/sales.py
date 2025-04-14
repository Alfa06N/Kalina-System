import flet as ft
import constants
from Modules.customControls import CustomAlertDialog, CustomAnimatedContainer, CustomAnimatedContainerSwitcher, CustomOperationContainer, CustomTextField, CustomDropdown, CustomImageContainer, CustomFloatingActionButton, CustomFilledButton, CustomTooltip, CustomNavigationOptions, CustomLowStockDialog, CustomTextButton
from Modules.Sections.SalesSection.components import SaleItemsList, SaleForm, SaleRecord
from utils.saleManager import saleMakerManager
from utils.exchangeManager import exchangeRateManager
from Modules.Sections.SalesSection.sale_history import SaleHistory
from utils.inventoryManager import inventoryManager
import threading
from utils.pathUtils import getImagePath

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
      saleMakerManager.setItemSelector(self.itemsList.itemsSelector)
    except:
      raise
    
  def openStockDialog(self):
    try:
      self.dialog = CustomLowStockDialog(
        page=self.page
      )
      
      self.page.open(self.dialog)
    except:
      raise
  
  def saleSuccessContent(self, idSale):
    try:
      saleRecord = SaleRecord(
        page=self.page,
        idSale=idSale,
      )
      
      products, recentlyAdded = inventoryManager.checkLowStock()
      isLowStock = len(products) > 0
      stockText = ft.Text(
        value="",
        size=22,
        color=constants.BLACK,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.W_500,
      )
      
      if recentlyAdded:
        stockText.value = f"Hay nuevos productos a punto de agotarse"
        stockText.color = constants.RED_TEXT
      elif len(products) > 0:
        stockText.value = f"Hay {len(products)} producto{"s" if len(products) > 1 else ""} con bajo inventario"
      else:
        stockText.value = f"El inventario está actualizado y bien abastecido"
      
      if isLowStock:
        inventoryContextInfo = ft.Column(
          expand=1,
          alignment=ft.MainAxisAlignment.CENTER,
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          spacing=5,
          controls=[
            ft.Row(
              alignment=ft.MainAxisAlignment.CENTER,
              vertical_alignment=ft.CrossAxisAlignment.CENTER,
              controls=[
                CustomTextButton(
                  text="Ver inventario",
                  on_click=lambda e: self.openStockDialog(),
                ),
                ft.Image(
                  src=getImagePath("inventory new low.png") if recentlyAdded else getImagePath("inventory low.png"),
                  width=120,
                  height=120,
                  fit=ft.ImageFit.CONTAIN,
                )
              ]
            ),
            stockText,
          ]
        )
      else:
        inventoryContextInfo = ft.Column(
          expand=1,
          alignment=ft.MainAxisAlignment.CENTER,
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          spacing=5,
          controls=[
          CustomTextButton(
            text="Ver inventario",
            on_click=lambda e: self.openStockDialog(),
          ) if isLowStock else ft.Image(
            src=getImagePath("Inventory up to date.png"),
            width=120,
            height=120,
            fit=ft.ImageFit.CONTAIN,
          ),
          stockText,
        ]
      )
      
      newContent = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Row(
          expand=True,
          alignment=ft.MainAxisAlignment.CENTER,
          vertical_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            ft.Column(
              expand=1,
              alignment=ft.MainAxisAlignment.CENTER,
              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
              controls=[
                ft.Column(
                  expand=1,
                  alignment=ft.MainAxisAlignment.CENTER,
                  horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                  spacing=20,
                  controls=[
                    ft.Text(
                      value="¡Venta realizada!",
                      color=constants.BLACK,
                      weight=ft.FontWeight.W_700,
                      size=36,
                    ),
                    CustomFilledButton(
                      text="Finalizar",
                      clickFunction=lambda e: self.showViewSelected(),
                    )
                  ]
                ),
                ft.Divider(color=constants.BLACK_GRAY),
                inventoryContextInfo,
              ]
            ),
            ft.Container(
              expand=1,
              alignment=ft.alignment.center,
              content=saleRecord,
              shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=constants.WHITE_GRAY,
              ),
              bgcolor=constants.WHITE,
              border_radius=30,
            ),
          ]
        )
      )
      
      self.mainContainer.setNewContent(newContent)
    except:
      raise