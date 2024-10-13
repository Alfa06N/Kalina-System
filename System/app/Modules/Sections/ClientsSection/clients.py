import flet as ft
import constants
from Modules.customControls import CustomAnimatedContainerSwitcher, CustomNavigationOptions, CustomAnimatedContainer, CustomFloatingActionButton, CustomGridView, CustomUserIcon, CustomAutoComplete
from Modules.clients_module import ClientForm
from Modules.Sections.ClientsSection.components import ClientContainer, ClientListTile, ClientSearchBar, ClientInfo
from config import getDB
from DataBase.crud.client import getClientById, getClients, getClientsOrderById
from exceptions import InvalidData, DataAlreadyExists, DataNotFoundError

class Clients(ft.Stack):
  def __init__(self, page):
    super().__init__()
    self.expand = True
    self.page = page
    
    self.infoContainer = CustomAnimatedContainerSwitcher(
      content=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          self.textForEmptyContainer(message="Selecciona un cliente para ver más información.")
        ]  
      ),
      expand=True,
      col={"sm": 12, "md": 12, "lg": 8, "xl": 8}
    )
    
    self.clientSearchBar = ClientSearchBar(
      controls=self.getClientsCI(),
      page=self.page,
      on_submit=lambda e: self.showClientInfo(e.control.value)
    )
    
    self.clientsContainer = CustomAnimatedContainerSwitcher(
      padding=0,
      alignment=ft.alignment.top_center,
      shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=5,
        color=constants.BLACK_INK,
      ),
      content=ft.Column(
        alignment=ft.MainAxisAlignment.START,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          self.clientSearchBar,
          ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            controls=self.getClientsContainers()
          )
        ],
      ),
      height=None,
      width=None,
      expand=True,
      col={"sm": 12, "md": 9, "lg": 4, "xl": 4}
    )
    
    self.addClientButton = CustomFloatingActionButton(
      on_click=self.addClientForm,
    )
    
    self.controls = [
      ft.ResponsiveRow(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        run_spacing=10,
        controls=[
          self.clientsContainer,
          self.infoContainer,
        ]
      ),
      ft.Container(
        content=self.addClientButton,
        right=10,
        bottom=10,
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
  
  def addClientForm(self, e):
    if not self.infoContainer.height >= 500:
      self.infoContainer.changeStyle(
        height=500, width=700, shadow=ft.BoxShadow(
          blur_radius=5,
          spread_radius=1,
          color=constants.BLACK_INK,
        )
      )
    
    self.infoContainer.setNewContent(
      newContent=ClientForm(
        page=self.page,
        mainContainer=self,
      )
    )
  
  def getClientsCI(self):
    try:
      ciList = []
      with getDB() as db:
        clients = getClientsOrderById(db)
        if clients:
          for client in clients:
            ci = client.ciClient
            ciList.append(ClientListTile(
              title=ci,
              on_click=lambda e: self.showClientInfo(int(e.control.title.value))
            ))
      return ciList
    except:
      raise
  
  def showClientInfo(self, ciClient):
    try:
      if not str(ciClient).isdigit():
        raise InvalidData("Ingrese un número válido.")
      with getDB() as db:
        client = getClientById(db, ciClient)
        
        if not client:
          raise DataNotFoundError("No se encontró el cliente con la CI proporcionada.")
        newContent = ClientInfo(
          page=self.page,
          ciClient=client.ciClient,
          initial=f"{client.name[0]}{client.surname[0]}",
          fullname=f"{client.name} {client.surname} {client.secondSurname}",
          clientContainer=None,
          mainContainer=self,
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
        
        self.infoContainer.setNewContent(newContent)
        self.clientSearchBar.close_view(text=f"{ciClient}")
        self.clientSearchBar.update()
    except InvalidData as err:
      self.page.open(ft.AlertDialog(
        title=ft.Text(value="Datos inesperados"),
        content=ft.Text(value=err, size=18),
      ))
    except DataNotFoundError as err:
      self.page.open(ft.AlertDialog(
        title=ft.Text(value="Cliente no encontrado"),
        content=ft.Text(value=err, size=18),
      ))
    except Exception as err:
      raise
  
  def getClientsContainers(self):
    try:
      containers = []
      with getDB() as db:
        clients = getClients(db)
        if clients:
          for client in clients:
            initial = client.name[0] + client.surname[0]
            
            fullname = f"{client.name} {client.surname} {client.secondSurname}"
            
            container = ClientContainer(
              page=self.page,
              ciClient=client.ciClient,
              initial=initial,
              fullname=fullname,
              infoContainer=self.infoContainer,
              mainContainer=self,
            )   
            containers.append(container)  
      return containers
    except:
      raise
  
  def resetClientsContainer(self):
    try:
      self.clientSearchBar.controls = self.getClientsCI()
      
      newContent = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          self.clientSearchBar,
          ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            controls=self.getClientsContainers()
          )
        ],
      )
      self.clientsContainer.setNewContent(newContent)
    except:
      raise
  
  def resetInfoContainer(self):
    try:
      if not self.infoContainer.height == 150:
        self.infoContainer.changeStyle(height=150, width=300, shadow=None)
      self.infoContainer.setNewContent(
        newContent=ft.Column(
          alignment=ft.MainAxisAlignment.CENTER,
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            self.textForEmptyContainer(message="Selecciona un cliente para ver más información.")
          ]  
        )
      )
    except Exception as err:
      raise
  
  def resetAll(self):
    try:
      self.resetInfoContainer()
      # Here goes more logic for clientsContainer
      self.resetClientsContainer()
    except:
      raise