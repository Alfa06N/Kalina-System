import flet as ft
import constants
from Modules.customControls import CustomAlertDialog, CustomAnimatedContainer, CustomAnimatedContainerSwitcher, CustomOperationContainer, CustomTextField, CustomDropdown, CustomImageContainer, CustomFloatingActionButton, CustomFilledButton, CustomTooltip, CustomEditButton, CustomReturnButton, CustomDeleteButton, CustomUserIcon, CustomCheckControl, CustomAlertDialog
from Modules.clients_module import ClientForm
from Modules.Sections.ClientsSection.components import ClientSearchBar, ClientListTile, ClientContainer
from DataBase.crud.client import getClientById, getClients, getClientsOrderById
from config import getDB
from exceptions import InvalidData, DataNotFoundError, DataAlreadyExists
import threading

class ClientCard(ft.Container):
  def __init__(self, page, formContainer, height=140, width=140):
    super().__init__()
    self.page = page
    self.formContainer = formContainer
    self.expand = True
    
    self.bgcolor = constants.WHITE
    self.border = ft.border.all(2, constants.BLACK_GRAY)
    self.border_radius = 20
    self.padding = ft.padding.all(10)
    self.ink = True
    self.ink_color = constants.WHITE_GRAY
    self.on_click = lambda e: self.clickFunction()
    
    self.selectedClient = None
    
    self.withoutClient = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Icon(
          name=ft.Icons.PERSON_ADD_ROUNDED,
          size=40,
          color=constants.BLACK,
        ),
        ft.Text(
          value="Agregar cliente",
          size=20,
          color=constants.BLACK,
          # weight=ft.FontWeight.W_600,
          text_align=ft.TextAlign.CENTER,
          overflow=ft.TextOverflow.ELLIPSIS,
        )
      ]
    )
    
    self.animatedContainer = CustomAnimatedContainer(
      actualContent=self.withoutClient
    )
    
    self.content = self.animatedContainer
  
  def clickFunction(self):
    try:
      newContent = ClientSelection(
        page=self.page,
        clientCard=self,
        formContainer=self.formContainer,
        selectedClient=self.selectedClient,
      )
      
      self.formContainer.changeContent(newContent)
    except:
      raise
  
  def updateCard(self, ciClient):
    try:
      self.selectedClient = ciClient

      if self.selectedClient == None:
        self.animatedContainer.setNewContent(newContent=self.withoutClient)
      else:
        self.animatedContainer.setNewContent(newContent=self.getIconContainer(ciClient=self.selectedClient))
    except:
      raise
  
  def validateCard(self):
    try:
      if self.selectedClient:
        with getDB() as db:
          client = getClientById(db, self.selectedClient)
          return True, self.selectedClient, f"Cliente: {client.name} V-{self.selectedClient}"
      else:
        raise InvalidData("Por favor, especifica quién es el cliente de la venta.")
    except:
      raise
    
  def getIconContainer(self, ciClient):
    try:
      with getDB() as db:
        client = getClientById(db, ciClient)
        
        clientIcon = CustomUserIcon(
          initial=f"{client.name[0]}{client.surname[0]}",
          gradient=False,
          fontSize=28,
          height=70,
          width=70,
        )
        
        return ft.Container(
          expand=True,
          alignment=ft.alignment.center,
          content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
              clientIcon,
              ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                controls=[
                  ft.Text(
                    value=f"{client.name.split()[0]} {client.surname}",
                    size=18,
                    color=constants.BLACK,
                    weight=ft.FontWeight.W_600,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    text_align=ft.TextAlign.CENTER,
                  ),
                  ft.Text(
                    value=f"{client.ciClient}",
                    size=18,
                    color=constants.BLACK,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    text_align=ft.TextAlign.CENTER,
                  )
                ]
              ),
            ]
          )
        )
    except:
      raise
    
class ClientSelection(ft.Container):
  def __init__(self, page, clientCard, formContainer, selectedClient=None):
    super().__init__()
    self.page = page
    self.clientCard = clientCard
    self.formContainer = formContainer
    self.selectedClient = selectedClient
    
    self.alignment = ft.alignment.center
    self.expand = True
    
    self.titleText = ft.Text(
      value="¿Quién es el cliente?",
      size=32,
      color=constants.BLACK,
      weight=ft.FontWeight.W_700,
      text_align=ft.TextAlign.CENTER,
    )
    
    self.documentTypeField = CustomDropdown(
      label="Tipo",
      options=[ft.dropdown.Option(value) for value in list(constants.documentTypes.keys())],
      value="Venezolano",
      expand=True,
      on_change=None
    )
    
    self.searchBar = ClientSearchBar(
      page=self.page,
      controls=self.getAllClientsCI(),
      expand=True,
      on_submit=lambda e: self.showClientContainer(e.control.value),
    )
    self.createClientButton = CustomEditButton(
      function=lambda e: self.showClientForm(),
    )
    self.createClientButton.content.name = ft.Icons.PERSON_ADD_ROUNDED
    
    self.clientDefaultContainer = ft.Container(
      alignment=ft.alignment.center,
      content=ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          ft.Icon(
            name=ft.Icons.PERSON_OFF_ROUNDED,
            size=32,
            color=constants.BLACK,
          ),
          ft.Text(
            value="No se ha seleccionado ningún cliente",
            size=20,
            color=constants.BLACK,
            text_align=ft.TextAlign.CENTER,
            overflow=ft.TextOverflow.ELLIPSIS,
          ),
        ]
      )
    )
    
    self.finishButton = CustomFilledButton(
      text="Finalizar",
      clickFunction=lambda e: self.finishFunction(),
    )
    
    self.animatedClientContainer = ft.Container(
      border=ft.border.all(2, constants.BLACK),
      height=100,
      border_radius=20,
      alignment=ft.alignment.center,
      content=CustomAnimatedContainer(
        actualContent=self.getClientContainer(ciClient=self.selectedClient) if self.selectedClient else self.clientDefaultContainer
      )
    )
    
    self.columnMainContent = ft.Column(
      expand=True,
      alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
      spacing=20,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          controls=[
            ft.Text(
              value="¿Nuevo cliente?",
              size=20,
              color=constants.BLACK,
            ),
            self.createClientButton,
          ]  
        ),
        ft.Container(
          padding=ft.padding.symmetric(vertical=10),
          content=ft.Row(
            controls=[
              self.documentTypeField,
              self.searchBar,
            ]
          )
        ),
        self.animatedClientContainer,
        self.finishButton
      ]
    )
    
    self.selectionContent = ft.Column(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        self.titleText,
        self.columnMainContent,
      ]
    )
    
    self.animatedMainContainer = CustomAnimatedContainer(
      actualContent=self.selectionContent,
    )
    
    self.content = self.animatedMainContainer
  
  def getAllClientsCI(self):
    try:
      ciList = []
      with getDB() as db:
        clients = getClientsOrderById(db)
        if clients:
          for client in clients:
            ci = client.ciClient
            ciList.append(ClientListTile(
              title=ci,
              on_click=lambda e: self.showClientContainer(int(e.control.title.value))
            ))
      return ciList
    except:
      raise
    
  def getClientContainer(self, ciClient):
    try:
      with getDB() as db:
        client = getClientById(db, ciClient)
        
        if not client:
          raise DataNotFoundError("No se encontró el cliente con la CI proporcionada.")
        
        newContent = ClientContainer(
          page=self.page,
          ciClient=ciClient,
          documentType=client.documentType,
          initial=f"{client.name[0]}{client.surname[0]}",
          fullname=f"{client.name} {client.surname} {client.secondSurname}",
          infoContainer=None,
          mainContainer=None
        )
        
        newContent.on_click = None
        newContent.shadow = None
        newContent.border = None
        
        removeClientButton = CustomEditButton(
          function=lambda e: self.removeClient()
        )
        
        removeClientButton.content.name = ft.Icons.DELETE_ROUNDED
        
        newContent = ft.Stack(
          controls=[
            newContent,
            ft.Container(
              right=20,
              top=10,
              content=removeClientButton
            )
          ]
        )
        
        return newContent
    except:
      raise
        
    
  def showClientContainer(self, ciClient):
    try:
      if not str(ciClient).isdigit():
        raise InvalidData("Ingrese un número válido.")
      
      newContent = self.getClientContainer(f"{constants.documentTypes[self.documentTypeField.value]}{ciClient}")
      
      self.animatedClientContainer.content.setNewContent(newContent=newContent)
      self.selectedClient = f"{constants.documentTypes[self.documentTypeField.value]}{ciClient}"
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
    except:
      raise
  
  def removeClient(self):
    try:
      self.selectedClient = None
      self.animatedClientContainer.content.setNewContent(self.clientDefaultContainer)
    except:
      raise
  
  def showClientForm(self):
    try:
      form = ClientForm(
        page=self.page,
        mainContainer=None
      )
      
      def customSubmitForm():
        try:
          result = form.submitForm()
          if result:
            self.selectedClient = f"{constants.documentTypes[form.documentTypeField.value]}{int(form.ciField.value)}"
            threading.Timer(1, self.finishFunction).start()
        except:
          raise
        
      form.finishButton.on_click = lambda e: customSubmitForm()
      form.ciField.on_submit = lambda e: customSubmitForm()
      form.nameField.on_submit = lambda e: customSubmitForm()
      form.surnameField.on_submit = lambda e: customSubmitForm()
      form.secondSurnameField.on_submit = lambda e: customSubmitForm()
      
      newForm = ft.Stack(
        expand=True,
        controls=[
          ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[form,]
          ),
          ft.Container(
            left=10,
            top=10,
            content=CustomReturnButton(
              function=lambda e: self.returnToSelection()
            )
          )
        ]
      )
      
      self.animatedMainContainer.setNewContent(newForm)
    except:
      raise
  
  def finishFunction(self):
    try:
      self.formContainer.returnToBegin()
      self.clientCard.updateCard(ciClient=self.selectedClient)
    except:
      raise
    
  def returnToSelection(self):
    try:
      self.animatedMainContainer.setNewContent(self.selectionContent)
    except:
      raise