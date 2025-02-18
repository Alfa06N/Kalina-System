import flet as ft
from Modules.customControls import CustomPrincipalContainer, CustomSimpleContainer, CustomOperationContainer, CustomAnimatedContainer, CustomOutlinedButton, CustomImageSelectionContainer, CustomNumberField, CustomTooltip, CustomFilledButton, CustomTextField, CustomAutoComplete, CustomDropdown, CustomAlertDialog, CustomReturnButton, CustomItemsSelector
import constants
from config import getDB
from validation import evaluateForm
from DataBase.crud.client import createClient, getClientById, getClients
import threading
from exceptions import DataAlreadyExists, InvalidData, DataNotFoundError

class ClientForm(CustomOperationContainer):
  def __init__(self, page, mainContainer):
    self.page = page
    self.mainContainer = mainContainer
    
    self.title = ft.Row(
      alignment=ft.MainAxisAlignment.CENTER,
      controls=[
        ft.Text(
          value="Nuevo Cliente",
          size=42,
          color=constants.BLACK,
          weight=ft.FontWeight.W_700,
          text_align=ft.TextAlign.CENTER,
        )
      ]
    )
    
    self.documentTypeField = CustomDropdown(
      label="Tipo de documento",
      expand=True,
      options=[ft.dropdown.Option(value) for value in list(constants.documentTypes.keys())],
      value="Venezolano",
      on_change=self.changeDocument
    )
    
    self.ciField = CustomTextField(
      label="Documento",
      field="ci",
      submitFunction=lambda e:self.submitForm(),
      expand=True,
    )
    
    self.nameField = CustomTextField(
      label="Nombre",
      field="others",
      submitFunction=lambda e:self.submitForm(),
      expand=True
    )
    
    self.surnameField = CustomTextField(
      label="Apellido",
      field="others",
      submitFunction=lambda e:self.submitForm(),
      expand=True
    )
    
    self.secondSurnameField = CustomTextField(
      label="Segundo Apellido (opcional)",
      field="others",
      submitFunction=lambda e:self.submitForm(),
      expand=True
    )
    
    self.finishButton = CustomFilledButton(
      text="Crear cliente",
      clickFunction=lambda e: self.submitForm()
    )
    
    self.form = ft.Column(
      height=400,
      width=700,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        self.title,
        ft.Row(
          expand=True,
          vertical_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            self.documentTypeField,
            self.ciField,
            self.nameField,
          ]
        ),
        ft.Row(
          expand=True,
          vertical_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            self.surnameField,
            self.secondSurnameField,
          ]
        ),
        ft.Row(
          expand=True,
          alignment=ft.MainAxisAlignment.CENTER,
            controls=[self.finishButton]  
        ),
      ]
    )
    super().__init__(operationContent=self.form)
    
  def changeDocument(self, value):
    try:
      newPrefix = constants.documentTypes[value]
      self.ciField.prefix_text = newPrefix
      self.ciField.update()
    except:
      raise
  
  def submitForm(self):
    try:
      nameFields = [self.nameField, self.surnameField] if len(self.secondSurnameField.value.strip()) == 0 else [self.nameField, self.surnameField, self.secondSurnameField]

      if evaluateForm(ci=[self.ciField], name=nameFields):
        with getDB() as db:
          newClient = createClient(
            db=db,
            documentType=self.documentTypeField.value,
            ciClient=self.ciField.prefix_text+self.ciField.value,
            name=self.nameField.value.strip(),
            surname=self.surnameField.value.strip(),
            secondSurname=self.secondSurnameField.value.strip(),
          )
          if newClient:
            self.actionSuccess("Cliente creado exitosamente.")
            if self.mainContainer:
              threading.Timer(1.5, self.mainContainer.resetAll).start()
            return True
    except DataAlreadyExists as err:
      self.actionFailed(err)
      threading.Timer(1.5, self.restartContainer).start()
    except Exception as err:
      raise