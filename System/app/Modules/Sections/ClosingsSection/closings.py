import flet as ft
import constants
from Modules.customControls import CustomAnimatedContainerSwitcher, CustomFloatingActionButton, CustomReturnButton, CustomAlertDialog, CustomTextButton
from Modules.Sections.ClosingsSection.components.ClosingRecord import ClosingRecord
from DataBase.crud.closing import getSalesWithoutClosing, createClosing, getClosings
from config import getDB
from exceptions import DataAlreadyExists, DataNotFoundError
from Modules.Sections.ClosingsSection.components.ClosingContainer import ClosingContainer
from datetime import datetime
from utils.dateConversions import convertToLocalTz

class Closings(ft.Stack):
  def __init__(self, page):
    super().__init__()
    self.page = page
    self.expand = True
    self.controlSelected = None
    
    self.closingsContainer = CustomAnimatedContainerSwitcher(
      col={"sm": 12, "md": 6, "xl": 4},
      margin=ft.margin.symmetric(horizontal=20, vertical=20),
      expand=True,
      padding=0,
      height=800,
      alignment=ft.alignment.top_left,
      border_radius=ft.border_radius.all(30),
      bgcolor=constants.WHITE,
      shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=5,
        color=constants.BLACK_INK
      ),
      content=ft.Column(
        alignment=ft.MainAxisAlignment.START,
        expand=True,
        controls=self.getClosings()
      )
    )
    
    self.infoContainer = CustomAnimatedContainerSwitcher(
      content=ft.Column(
        controls=[
          self.textForEmptyContainer("Selecciona un cierre para ver mas información")
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
      ),
      col={"sm": 12, "md": 6, "xl": 8},
    )
    
    self.closingsView = ft.ResponsiveRow(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      run_spacing=10,
      controls=[
        self.closingsContainer,
        self.infoContainer,
      ]
    )
    
    self.addUserButton = CustomFloatingActionButton(
      on_click=lambda e: self.showPartialClosing(),
      icon=ft.Icons.PREVIEW_ROUNDED
    )
    
    self.controls = [
      self.closingsView,
      ft.Container(
        content=self.addUserButton,
        right=10,
        bottom=10
      )
    ]
  
  def textForEmptyContainer(self, value):
    return ft.Text(
      value=value,
      color=constants.BLACK,
      size=32,
      weight=ft.FontWeight.BOLD,
      text_align=ft.TextAlign.CENTER,
    )
    
  def closeInfoContainer(self):
    self.infoContainer.setNewContent(self.textForEmptyContainer("Selecciona un cierre para ver más información."))
    self.infoContainer.changeStyle(
      height=300,
      width=800,
      shadow=None
    )
  
  def resetAll(self):
    self.closeInfoContainer()
    
  def createClosing(self, sales, generalPrice, totals, gain):
    try:
      def confirmClosing():
        try:
          with getDB() as db:
            self.page.close(self.dialog)
            closing = createClosing(db, sales=sales, generalPrice=generalPrice, totals=totals, gain=gain)
            print("Closing creado exitosamente")
            print(closing.idClosing)
    
            self.closeInfoContainer()
            self.resetClosingContainers()
        except DataAlreadyExists as e:
          dialog = CustomAlertDialog(
            title=e,
            modal=False
          )
      
          self.page.open(dialog)
          
    
      self.dialog = CustomAlertDialog(
        title="Confirmar creación de cierre",
        content=ft.Text(
          value="Solo puedes crear un cierre al día",
          color=constants.BLACK,
          size=20,
        ),
        actions=[
          CustomTextButton(
            text="Crear",
            on_click=lambda e: confirmClosing()
          ),
          CustomTextButton(
            text="Cancelar",
            on_click=lambda e: self.page.close(self.dialog)  
          ),
        ]
      )
      
      self.page.open(self.dialog)
    except DataAlreadyExists as e:
      dialog = CustomAlertDialog(
        title=e,
        modal=False
      )
      
      self.page.open(dialog)
    except:
      raise
    
  def resetClosingContainers(self):
    newContent = ft.Column(
      alignment=ft.MainAxisAlignment.START,
      expand=True,
      controls=self.getClosings()
    )
    
    self.closingsContainer.setNewContent(newContent)
    
  def getClosings(self):
    containers = []
    
    with getDB() as db:
      closings = getClosings(db)
      if closings and len(closings) > 0:
        for closing in closings:
          print(closing.idClosing)
          container = ClosingContainer(
            page=self.page,
            idClosing=closing.idClosing,
            amount=round(closing.amount, 2),
            date=closing.date.strftime("%d/%m/%Y"),
            mainContainer=self,
          )
          containers.append(container)
      else:
        return containers

    return containers
  
  def showPartialClosing(self):
    with getDB() as db:
      sales, generalPrice, totals, gain = getSalesWithoutClosing(db)
      newContent = ClosingRecord(
        page=self.page,
        sales=sales,
        amount=generalPrice,
        totals=totals,
        gain=gain,
        date=None,
        partial=True,
        createFunction=lambda e: self.createClosing(sales=sales, generalPrice=generalPrice, totals=totals, gain=gain),
      )
      
      newContent = ft.Stack(
        expand=True,
        controls=[
          newContent,
        ]
      )
      if self.infoContainer.height != 700:
        self.infoContainer.changeStyle(
          height=700,
          width=800,
          shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=4,
            color=constants.BLACK_INK
          )
        )
        
      if self.controlSelected:
        self.controlSelected.deselect()
        self.controlSelected = None
      self.infoContainer.setNewContent(newContent)
    
  def showClosing(self, content, container):
    if self.controlSelected:
      self.controlSelected.deselect()
    self.controlSelected = container
    self.controlSelected.select()
    
    if not self.infoContainer.height == 700:
      self.infoContainer.changeStyle(
        height=700,
        width=800,
        shadow=ft.BoxShadow(
        blur_radius=5,
        spread_radius=1,
        color=constants.WHITE_GRAY,
        )
      )
    
    self.infoContainer.setNewContent(content)