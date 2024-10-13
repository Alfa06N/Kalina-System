import flet as ft 
from Modules.customControls import CustomAnimatedContainer, CustomOperationContainer, CustomUserIcon, CustomCardInfo, CustomDeleteButton
import constants
from DataBase.crud.client import getClientById, getClients, removeClient
from config import getDB
import threading
from exceptions import DataAlreadyExists, DataNotFoundError
import re

class ClientContainer(ft.Container):
  def __init__(self, page, ciClient, initial, fullname, infoContainer, mainContainer):
    super().__init__()
    self.initial = initial
    self.ciClient = ciClient
    self.fullname = fullname
    self.infoContainer = infoContainer
    self.mainContainer = mainContainer
    self.page = page

    self.shadow = ft.BoxShadow(
      spread_radius=1,
      blur_radius=1,
      color=constants.WHITE_GRAY,
    )
    self.padding = ft.padding.all(10)
    self.bgcolor = constants.WHITE
    self.border_radius = ft.border_radius.all(30)
    self.ink = True
    self.ink_color = constants.BLACK_INK
    self.on_click = self.showClientInfo
    
    self.clientTitle = CustomAnimatedContainer(
      actualContent=ft.Text(
        value=self.fullname,
        size=18,
        color=constants.BLACK,
        weight=ft.FontWeight.W_700,
        overflow=ft.TextOverflow.ELLIPSIS,
      )
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
            ft.Text(
              value=f"V-{self.ciClient}",
              size=18,
              color=constants.BLACK,
              overflow=ft.TextOverflow.ELLIPSIS,
            )
          ]
        )
      ]
    )
    
  def showClientInfo(self, e):
    try:
      newContent = ClientInfo(
        page=self.page,
        ciClient=self.ciClient,
        initial=self.initial,
        fullname=self.fullname,
        mainContainer=self.mainContainer,
        clientContainer=self,
      )
      
      if self.infoContainer.height <=150:
        self.infoContainer.changeStyle(
          height=800,
          width=700,
          shadow=ft.BoxShadow(
          blur_radius=5,
          spread_radius=1,
          color=constants.WHITE_GRAY,
          )
        )
      self.infoContainer.setNewContent(newContent=newContent)
    except Exception as err:
      raise 

class ClientInfo(ft.Stack):
  def __init__(self, page, ciClient, initial, fullname, clientContainer, mainContainer):
    super().__init__()
    self.page = page
    self.initial = initial
    self.ciClient = ciClient
    self.fullname = fullname
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
      value=f"V-{self.ciClient}",
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
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Text(
          value="No hay movimientos aún",
          color=constants.BLACK,
          size=24,
          text_align=ft.TextAlign.CENTER,
          overflow=ft.TextOverflow.ELLIPSIS,
        )
      ]
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
    
    self.controls = [
      self.columnContent,
      ft.Container(
        right=10,
        top=10,
        content=self.deleteButton
      )
    ]
  
  def deleteClient(self):
    try:
      with getDB() as db:
        client = getClientById(db, self.ciClient)

        if client:
          client = removeClient(db, client)
          self.mainContainer.resetAll()
    except:
      raise
    
class ClientSearchBar(ft.SearchBar):
  def __init__(self, page, controls:list=[], on_submit=None):
    super().__init__()
    self.view_elevation = 4
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