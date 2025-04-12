import flet as ft
import constants
from Modules.customControls import CustomAnimatedContainerSwitcher, CustomNavigationOptions, CustomAnimatedContainer, CustomFloatingActionButton, CustomGridView, CustomUserIcon, CustomAutoComplete, CustomAlertDialog, CustomDropdown
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
    
    self.currentPage = 1
    self.controlSelected = None
    self.clientSelected = None
    
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
          self.textForEmptyContainer(message="Selecciona un cliente para ver más información.")
        ]  
      ),
      expand=True,
      col={"sm": 12, "md": 12, "lg": 8, "xl": 8}
    )
    
    self.clientSearchBar = ClientSearchBar(
      controls=self.getClientsCI(),
      page=self.page,
      expand=True,
      on_submit=lambda e: self.showClientInfo(e.control.value)
    )
    
    self.documentTypeField = CustomDropdown(
      label="Tipo",
      options=[ft.dropdown.Option(value) for value in list(constants.documentTypes.keys())],
      value="Venezolano",
      expand=True,
      on_change=None
    )
    
    self.clientsList = CustomAnimatedContainerSwitcher(
      content=ft.Column(
        alignment=ft.MainAxisAlignment.START,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
        scroll=ft.ScrollMode.AUTO,
        controls=self.getClientsContainers()
      ),
      alignment=ft.alignment.top_center,
      expand=True,
      width=None,
      padding=0,
      margin=0,
    )
    
    self.clientsContainer = CustomAnimatedContainerSwitcher(
      padding=0,
      alignment=ft.alignment.center,
      shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=5,
        color=constants.BLACK_INK,
      ),
      content=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          ft.Container(
            padding=ft.padding.symmetric(horizontal=10, vertical=10),
            content=ft.Row(
              controls=[
                self.documentTypeField,
                self.clientSearchBar,
              ]
            ), 
          ),
          self.clientsList,
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
    
    self.controlSelected = None
    
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
    
  def updateClientsContainers(self):
    try:
      newContent = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        controls=self.getClientsContainers()
      )
      self.clientsList.setNewContent(newContent)
      
    except:
      raise
    
  def updatePage(self, number: int):
    self.currentPage += number
    self.updateClientsContainers()
    self.controlSelected = None
    
    if self.clientSelected:
      for container in self.clientsList.content.content.controls:
        if hasattr(container, "ciClient") and container.ciClient == self.clientSelected:
          container.select()
          self.clientSelected = container.ciClient
          self.controlSelected = container
          break
  
  def addClientForm(self, e):
    if not self.infoContainer.height >= 500:
      self.infoContainer.changeStyle(
        height=500, width=700, shadow=ft.BoxShadow(
          blur_radius=5,
          spread_radius=1,
          color=constants.BLACK_INK,
        )
      )
    
    if self.controlSelected:
      self.controlSelected.deselect()
      self.controlSelected = None
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
        client = getClientById(db, f"{constants.documentTypes[self.documentTypeField.value]}{ciClient}")
        
        if not client:
          raise DataNotFoundError("No se encontró el cliente con la CI proporcionada.")
        newContent = ClientInfo(
          page=self.page,
          ciClient=client.ciClient,
          documentType=client.documentType,
          initial=f"{client.name[0]}{client.surname[0]}",
          fullname=f"{client.name} {client.surname} {client.secondSurname}",
          clientContainer=None,
          mainContainer=self,
        )

        for control in self.clientsList.content.content.controls:
          if hasattr(control, "ciClient") and control.ciClient == self.clientSelected:
            control.deselect()
            break
        self.clientSelected = client.ciClient
        
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
        
        columnContainers = self.clientsList.content.content.controls
        for control in columnContainers:
          if hasattr(control, "ciClient") and control.ciClient == client.ciClient:
            containerSelected = control
            if self.controlSelected:
              self.controlSelected.deselect()
            self.controlSelected = containerSelected
            self.controlSelected.select()
    except InvalidData as err:
      self.page.open(CustomAlertDialog(
        modal=False,
        title="Datos inesperados",
        content=ft.Text(value=err, size=18),
      ))
    except DataNotFoundError as err:
      self.page.open(CustomAlertDialog(
        modal=False,
        title="Cliente no encontrado",
        content=ft.Text(value=err, size=18),
      ))
    except Exception as err:
      raise
  
  def getClientsContainers(self):
    try:
      containers = []
      with getDB() as db:
        clients = getClients(db, self.currentPage)
        if clients:
          if self.currentPage > 1:
            containers.append(self.upButton)
          for client in clients:
            initial = client.name[0] + client.surname[0]
            
            fullname = f"{client.name} {client.surname} {client.secondSurname}"
            
            container = ClientContainer(
              page=self.page,
              ciClient=client.ciClient,
              initial=initial,
              fullname=fullname,
              documentType=client.documentType,
              infoContainer=self.infoContainer,
              mainContainer=self,
            )   
            containers.append(container)  
          if getClients(db, self.currentPage + 1):
            containers.append(self.downButton)
      return containers
    except:
      raise
  
  def resetClientsContainer(self):
    try:
      self.clientSearchBar.controls = self.getClientsCI()
      
      self.clientsList = CustomAnimatedContainerSwitcher(
        content=ft.Column(
          alignment=ft.MainAxisAlignment.START,
          expand=True,
          horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
          scroll=ft.ScrollMode.AUTO,
          controls=self.getClientsContainers()
        ),
        expand=True,
        width=None,
        padding=0,
        margin=0,
      )
      
      newContent = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          ft.Container(
            padding=ft.padding.symmetric(horizontal=10, vertical=10),
            content=ft.Row(
              controls=[
                self.documentTypeField,
                self.clientSearchBar,
              ]
            ), 
          ),
          self.clientsList,
        ],
      )
      self.clientsContainer.setNewContent(newContent)
      self.controlSelected = None
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
      self.controlSelected = None
    except Exception as err:
      raise
  
  def showContentInfo(self, content, container):
    if self.controlSelected:
      self.controlSelected.deselect()
    self.controlSelected = container
    self.clientSelected = container.ciClient
    self.controlSelected.select()
    
    if not self.infoContainer.height == 800:
      self.infoContainer.changeStyle(
        height=800,
        width=700,
        shadow=ft.BoxShadow(
        blur_radius=5,
        spread_radius=1,
        color=constants.WHITE_GRAY,
        )
      )
    
    self.infoContainer.setNewContent(content)
  
  def resetAll(self):
    try:
      self.resetInfoContainer()
      self.resetClientsContainer()
    except:
      raise