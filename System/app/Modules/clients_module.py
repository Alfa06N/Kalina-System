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
    
    self.ciField = CustomTextField(
      label="Cédula de Identidad",
      field="ci",
      submitFunction=self.submitForm,
      expand=True,
    )
    
    self.nameField = CustomTextField(
      label="Nombre",
      field="others",
      submitFunction=self.submitForm,
      expand=True
    )
    
    self.surnameField = CustomTextField(
      label="Apellido",
      field="others",
      submitFunction=self.submitForm,
      expand=True
    )
    
    self.secondSurnameField = CustomTextField(
      label="Segundo Apellido (opcional)",
      field="others",
      submitFunction=self.submitForm,
      expand=True
    )
    
    self.finishButton = CustomFilledButton(
      text="Crear cliente",
      clickFunction=self.submitForm
    )
    
    self.form = ft.Column(
      height=500,
      width=700,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        self.title,
        ft.Row(
          expand=True,
          vertical_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
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
  
  def submitForm(self, e):
    try:
      if evaluateForm(ci=[self.ciField], others=[self.nameField, self.surnameField]):
        with getDB() as db:
          newClient = createClient(
            db=db,
            ciClient=float(self.ciField.value),
            name=self.nameField.value.strip(),
            surname=self.surnameField.value.strip(),
            secondSurname=self.secondSurnameField.value.strip(),
          )
          if newClient:
            print(f"{newClient.name} {newClient.surname} {newClient.secondSurname}. V-{newClient.ciClient}")
            self.actionSuccess("Cliente creado exitosamente.")
            threading.Timer(1.5, self.mainContainer.resetInfoContainer).start()
    except Exception as err:
      raise