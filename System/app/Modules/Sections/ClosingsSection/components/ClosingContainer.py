import flet as ft
import constants
from Modules.customControls import CustomUserIcon, CustomOperationContainer, CustomTextField, CustomAnimatedContainer, CustomNavigationOptions, CustomFilledButton, CustomDropdown, CustomDeleteButton, CustomAlertDialog, CustomReturnButton, CustomOutlinedButton
from config import getDB
from Modules.Sections.ClosingsSection.components.ClosingRecord import ClosingRecord
from Modules.Sections.ClosingsSection.components.TransactionRecord import TransactionRecord
from DataBase.crud.sale import getSaleById
from DataBase.crud.transaction import getTransactionById
from utils.dateConversions import getLocal, convertToLocalTz
from datetime import datetime
from DataBase.crud.closing import getClosings, getClosingById, getSalesByClosing

class ClosingContainer(ft.Container):
  def __init__(self, page, idClosing, amount, date, mainContainer):
    super().__init__()
    self.page = page
    self.amount = amount
    self.date = date
    self.idClosing = idClosing
    self.mainContainer = mainContainer
    
    self.border = ft.border.all(2, constants.BLACK_INK)
    self.padding = ft.padding.all(10)
    self.bgcolor = constants.WHITE
    self.border_radius = ft.border_radius.all(30)
    self.on_click = self.showClosing
    self.animate = ft.animation.Animation(
      duration=300,
      curve=ft.AnimationCurve.EASE,
    )
      
    self.amountText = ft.Text(
      value=f"{round(self.amount, 2)}$",
      size=24,
      color=constants.GREEN_TEXT,
      weight=ft.FontWeight.W_700,
      overflow=ft.TextOverflow.ELLIPSIS,
    )
    
    self.dateText = ft.Text(
      value=self.date,
      size=20,
      color=constants.BLACK,
      overflow=ft.TextOverflow.ELLIPSIS,
    )
      
    self.content = ft.Column(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      spacing=0,
      controls=[
        ft.Row(
          alignment=ft.MainAxisAlignment.START,
          vertical_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            self.amountText,
          ]
        ),
        ft.Row(
          alignment=ft.MainAxisAlignment.START,
          vertical_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            self.dateText,
          ]
        ),
      ]      
    )
  
  def showClosing(self, e):
    if not self.mainContainer.controlSelected == self:
      with getDB() as db:
        closing = getClosingById(db, self.idClosing)
        sales, products, combos, generalPrice, totals, gain = getSalesByClosing(db, closing.idClosing)
      content = ClosingRecord(
        page=self.page,
        sales=sales,
        amount=self.amount,
        totals=totals,
        date=self.date,
        gain=gain,
        combosName=combos,
        productsName=products,
        idClosing=closing.idClosing,
        partial=False,
      )
      
      self.mainContainer.showClosing(content, self)
    
  def select(self):
    self.border = ft.border.all(2, constants.BLACK_GRAY)
    self.bgcolor = constants.ORANGE
    self.update()
  
  def deselect(self):
    self.border = ft.border.all(2, constants.BLACK_INK)
    self.bgcolor = constants.WHITE
    
    self.update()