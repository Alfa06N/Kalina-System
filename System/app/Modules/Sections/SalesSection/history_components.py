import flet as ft
import constants
from Modules.customControls import CustomAlertDialog, CustomAnimatedContainer, CustomAnimatedContainerSwitcher, CustomOperationContainer, CustomTextField, CustomDropdown, CustomImageContainer, CustomFloatingActionButton, CustomFilledButton, CustomTooltip, CustomNavigationOptions
from Modules.Sections.SalesSection.components import SaleItemsList, SaleForm, SaleRecord
from utils.saleManager import saleMakerManager
from DataBase.crud.sale import getSaleById, getSales, removeSale
from config import getDB
import threading
from exceptions import DataAlreadyExists, DataNotFoundError 
from datetime import datetime
from utils.dateConversions import convertToLocalTz

class SaleContainer(ft.Container):
  def __init__(self, page, idSale, infoContainer, mainContainer):
    super().__init__()
    self.page = page
    self.idSale = idSale
    self.infoContainer = infoContainer
    self.mainContainer = mainContainer
    
    self.border = ft.border.all(2, constants.BLACK_INK)
    self.padding = ft.padding.all(10)
    self.bgcolor = constants.WHITE
    self.border_radius = ft.border_radius.all(30)
    self.on_click = lambda e: self.showSaleInfo()
    self.animate = ft.animation.Animation(
      duration=300,
      curve=ft.AnimationCurve.EASE,
    )
    
    with getDB() as db:
      sale = getSaleById(db, self.idSale)
      
      self.titleText = ft.Text(
        value=f"{round(sale.totalPrice, 2)}$",
        size=24,
        color=constants.GREEN_TEXT,
        weight=ft.FontWeight.W_700,
        overflow=ft.TextOverflow.ELLIPSIS,
      )
      
      self.clientText = ft.Row(
        controls=[
          ft.Text(
            value=f"Cliente:",
            size=20,
            color=constants.BLACK,
            weight=ft.FontWeight.W_600,
            overflow=ft.TextOverflow.ELLIPSIS,
          ),
          ft.Text(
            value=f"{sale.client.name.split()[0]} {sale.client.surname}",
            size=20,
            color=constants.BLACK,
            overflow=ft.TextOverflow.ELLIPSIS,
          )
        ]
      )
      
      self.dateText = ft.Text(
        value=f"{convertToLocalTz(sale.date).strftime("%d/%m/%Y")}",
        color=constants.BLACK,
        size=20,
        weight=ft.FontWeight.W_600,
      )
      
      self.content = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
        controls=[
          ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
              self.titleText,
              self.dateText
            ]
          ),
          self.clientText
        ]
      )
      
  def showSaleInfo(self):
    try:
      if not self.mainContainer.controlSelected == self:
        newContent = SaleRecord(
          page=self.page,
          idSale=self.idSale,
        )
        
        self.mainContainer.showContentInfo(newContent, self)
    except:
      raise
  
  def select(self):
    self.border = ft.border.all(2, constants.BLACK_GRAY)
    self.bgcolor = constants.ORANGE
    self.update()
  
  def deselect(self):
    self.border = ft.border.all(2, constants.BLACK_INK)
    self.bgcolor = constants.WHITE
    
    self.update()