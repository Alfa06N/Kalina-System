import flet as ft 
from Modules.customControls import CustomAnimatedContainer, CustomOperationContainer, CustomUserIcon, CustomCardInfo, CustomDeleteButton, CustomReturnButton
import constants
from DataBase.crud.client import getClientById, getClients, removeClient
from config import getDB
import threading
from exceptions import DataAlreadyExists, DataNotFoundError
import re

class ClientContainer(ft.Container):
  def __init__(self, page, ciClient, documentType, initial, fullname, infoContainer, mainContainer):
    super().__init__()
    self.initial = initial
    self.ciClient = ciClient
    self.fullname = fullname
    self.documentType = documentType
    self.infoContainer = infoContainer
    self.mainContainer = mainContainer
    self.page = page

    self.padding = ft.padding.all(10)
    self.bgcolor = constants.WHITE
    self.border_radius = ft.border_radius.all(30)
    self.border = ft.border.all(2, constants.BLACK_INK)
    self.on_click = self.showClientInfo
    self.animate = ft.animation.Animation(
      300, ft.AnimationCurve.EASE
    )
    
    self.clientTitle = CustomAnimatedContainer(
      actualContent=ft.Text(
        value=self.fullname,
        size=20,
        color=constants.BLACK,
        weight=ft.FontWeight.W_700,
        overflow=ft.TextOverflow.ELLIPSIS,
      )
    )
    
    self.clientCI = ft.Text(
      value=f"{self.ciClient}",
      size=20,
      color=constants.BLACK,
      overflow=ft.TextOverflow.ELLIPSIS,
    )
    
    self.content = ft.Row(
      expand=True,
      alignment=ft.MainAxisAlignment.START,
      controls=[
        CustomUserIcon(
          initial=self.initial,
          gradient=False,
        ),
        ft.Column(
          expand=True,
          alignment=ft.MainAxisAlignment.CENTER,
          spacing=0,
          controls=[
            self.clientTitle,
            self.clientCI,
          ]
        )
      ]
    )
    
  def showClientInfo(self, e):
    try:
      if not self.mainContainer.controlSelected == self:
        newContent = ClientInfo(
          page=self.page,
          ciClient=self.ciClient,
          initial=self.initial,
          documentType=self.documentType,
          fullname=self.fullname,
          mainContainer=self.mainContainer,
          clientContainer=self,
        )
        
        self.mainContainer.showContentInfo(newContent, self)
    except Exception as err:
      raise 
  
  def select(self):
    self.border = ft.border.all(2, constants.BLACK_GRAY)
    self.bgcolor = constants.ORANGE
    self.update()
  
  def deselect(self):
    self.border = ft.border.all(2, constants.BLACK_INK)
    self.bgcolor = constants.WHITE
    
    self.update()

class ClientInfo(ft.Container):
  def __init__(self, page, ciClient, documentType, initial, fullname, clientContainer, mainContainer):
    super().__init__()
    self.page = page
    self.initial = initial
    self.ciClient = ciClient
    self.fullname = fullname
    self.documentType = documentType
    self.clientContainer = clientContainer
    self.mainContainer = mainContainer
    
    self.expand = True
    
    self.clientIcon = CustomUserIcon(
      initial=self.initial,
      width=100,
      height=100,
      fontSize=42,
      gradient=False,
    )
    
    self.clientCI = ft.Text(
      value=f"{self.ciClient}",
      color=constants.BLACK,
      size=24,
    )
    
    self.clientTitle = ft.Text(
      value=f"{fullname}",
      color=constants.BLACK,
      size=24,
      weight=ft.FontWeight.W_700,
      overflow=ft.TextOverflow.ELLIPSIS,
    )
    
    self.activityText = ft.Text(
      value="Actividad",
      color=constants.BLACK,
      size=24,
      weight=ft.FontWeight.W_700,
    )
    
    self.activityList = ft.Column(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      scroll=ft.ScrollMode.ALWAYS,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=self.getSaleContainers()
    )
    
    self.deleteButton = CustomDeleteButton(
      page=self.page,
      function=self.deleteClient,
    )
    
    self.columnContent = ft.Column(
      expand=True,
      alignment=ft.MainAxisAlignment.START,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          expand=False,
          vertical_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            self.clientIcon,
            ft.Column(
              alignment=ft.MainAxisAlignment.CENTER,
              controls=[
                self.clientTitle,
                self.clientCI
              ]
            ),
          ]
        ),
        ft.Divider(color=constants.WHITE_GRAY),
        ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          controls=[
            ft.Icon(
              name=ft.icons.ANALYTICS_ROUNDED,
              size=28,
              color=constants.BLACK,
            ),
            self.activityText,
          ]
        ),
        self.activityList,
      ]
    )
    
    self.returnButton = CustomReturnButton(
      function=lambda e: self.switchMainContent(content=self.infoContent)
    )
    
    self.infoContent = ft.Stack(
      expand=True,
      controls=[
        self.columnContent,
      ]
    )
    
    self.animatedContainer = CustomAnimatedContainer(
      actualContent=self.infoContent
    )
    
    self.content = self.animatedContainer
  
  def deleteClient(self):
    try:
      with getDB() as db:
        client = getClientById(db, self.ciClient)

        if client:
          client = removeClient(db, client)
          self.mainContainer.resetAll()
    except:
      raise
  
  def getSaleContainers(self):
    from Modules.Sections.SalesSection.history_components import SaleContainer
    from Modules.Sections.SalesSection.components import SaleRecord
    try:
      containers = []
      with getDB() as db:
        client = getClientById(db, ciClient=self.ciClient)
        if client.sales:
          for sale in client.sales:
            container = SaleContainer(
              page=self.page,
              idSale=sale.idSale,
              infoContainer=None,
              mainContainer=None,
            )
            
            def customizedClickFunction():
              saleRecord = SaleRecord(
                page=self.page,
                idSale=sale.idSale,
              )
              newContent = ft.Stack(
                expand=True,
                controls=[
                  saleRecord,
                  ft.Container(
                    left=10,
                    top=10,
                    border_radius=5,
                    bgcolor=constants.WHITE,
                    content=self.returnButton,
                  )
                ]
              )
              self.switchMainContent(newContent)
            
            container.on_click = lambda e: customizedClickFunction()
            container.margin = ft.margin.all(4)
            containers.append(container)
        else: 
          containers.append(ft.Text(
            value="Este cliente no ha realizado ninguna compra",
            size=32,
            color=constants.BLACK,
            weight=ft.FontWeight.W_700,
            text_align=ft.TextAlign.CENTER,
          ))
      return containers
    except:
      raise
  
  def switchMainContent(self, content):
    self.animatedContainer.setNewContent(content)
    
class ClientSearchBar(ft.SearchBar):
  def __init__(self, page, controls:list=[], on_submit=None, expand=False):
    super().__init__()
    self.view_elevation = 4
    self.expand=expand
    self.bar_hint_text = "Buscar clientes..."
    self.view_hint_text = "Escribe o selecciona la CI deseada..."
    self.controls = controls
    self.page = page
    
    self.on_submit = on_submit

class ClientListTile(ft.ListTile):
  def __init__(self, title:str, on_click=None):
    super().__init__()
    self.title = ft.Text(
      value=title,
      size=24,
      color=constants.BLACK,
    )
    self.on_click = on_click if not on_click == None else None