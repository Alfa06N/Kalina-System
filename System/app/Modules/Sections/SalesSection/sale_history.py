import flet as ft
import constants
from Modules.customControls import CustomAlertDialog, CustomAnimatedContainer, CustomAnimatedContainerSwitcher, CustomOperationContainer, CustomTextField, CustomDropdown, CustomImageContainer, CustomFloatingActionButton, CustomFilledButton, CustomTooltip, CustomNavigationOptions
from Modules.Sections.SalesSection.components import SaleItemsList, SaleForm
from utils.saleManager import saleMakerManager
from Modules.Sections.SalesSection.history_components import SaleContainer
from config import getDB
from DataBase.crud.sale import getSales

class SaleHistory(ft.Stack):
  def __init__(self, page):
    super().__init__()
    self.expand = True
    self.page = page
    
    self.currentPage = 1
    
    self.upButton = ft.Container(
      padding=ft.padding.symmetric(vertical=10),
      content=ft.IconButton(
        icon=ft.icons.ARROW_CIRCLE_UP,
        icon_color=constants.BLACK,
        icon_size=48,
        tooltip="Página anterior",
        on_click=lambda e: self.updatePage(-1),
      )
    )
    
    self.downButton = ft.Container(
      padding=ft.padding.symmetric(vertical=10),
      content=ft.IconButton(
        icon=ft.icons.ARROW_CIRCLE_DOWN,
        icon_color=constants.BLACK,
        icon_size=48,
        tooltip="Página siguiente",
        on_click=lambda e: self.updatePage(1)
      )
    )
    
    self.infoContainer = CustomAnimatedContainerSwitcher(
      content=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          self.textForEmptyContainer("Selecciona un registro para ver más información de la venta.")
        ]
      ),
      expand=True,
      col={"sm": 12, "md": 12, "lg": 8, "xl": 8}
    )
    
    self.salesContainer = CustomAnimatedContainerSwitcher(
      padding=0,
      alignment=ft.alignment.center,
      shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=5,
        color=constants.BLACK_INK,
      ),
      content=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        controls=self.getSaleContainers()
      ),
      height=None,
      width=None,
      expand=True,
      col={"sm": 12, "md": 9, "lg": 4, "xl": 4},
    )
    
    self.controls = [
      ft.ResponsiveRow(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        run_spacing=10,
        controls=[
          self.salesContainer,
          self.infoContainer,
        ]
      )
    ]
    
  def textForEmptyContainer(self, message):
    return ft.Text(
      value=message,
      size=32,
      color=constants.BLACK,
      weight=ft.FontWeight.W_700,
      text_align=ft.TextAlign.CENTER,
    )
    
  def getSaleContainers(self):
    try:
      containers = []
      with getDB() as db:
        sales = getSales(db, self.currentPage)
        if sales:
          if self.currentPage > 1:
            containers.append(self.upButton)
          for sale in sales:
            container = SaleContainer(
              page=self.page,
              idSale=sale.idSale,
              infoContainer=self.infoContainer,
              mainContainer=self,
            )
            containers.append(container)
          if getSales(db, self.currentPage + 1):
            containers.append(self.downButton)
        else:
          containers.append(self.textForEmptyContainer("No se han realizado ventas"))
      return containers
    except:
      raise
  
  def updatePage(self, number:int):
    self.currentPage += number
    self.updateSaleContainers()
  
  def updateSaleContainers(self):
    try:
      newContent = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        controls=self.getSaleContainers()
      )
      
      self.salesContainer.setNewContent(newContent)
    except:
      raise