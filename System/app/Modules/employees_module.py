import flet as ft 
from Modules.customControls import CustomSimpleContainer, CustomFilledButton, CustomOutlinedButton, CustomCheckbox, CustomReturnButton, CustomTextField, CustomAnimatedContainerSwitcher, CustomAnimatedContainer, CustomOperationContainer, CustomDatePicker, CustomAlertDialog, CustomTextButton
from validation import evaluateForm
import time 
from exceptions import InvalidData, DataAlreadyExists
import constants
from config import getDB
from DataBase.crud.employee import createEmployee

class EmployeesForm(CustomOperationContainer):
  def __init__(self, page, employeesContent):
    self.page = page
    self.employeesContent = employeesContent
    self.title = ft.Row(
      alignment=ft.MainAxisAlignment.CENTER,
      expand=True,
      controls=[
        ft.Text(
          value="Nuevo Empleado",
          size=42, 
          color=constants.BLACK,
          weight=ft.FontWeight.BOLD,
          text_align=ft.TextAlign.CENTER,
        ),
      ]
    )
    
    self.ciField = CustomTextField(
      label="Documento",
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
    
    self.birthdateText = ft.Text(
      value="Fecha de nacimiento",
      size=20,
      color=constants.BLACK,
    )
    self.birthdateIcon = ft.Icon(
      name=ft.icons.CALENDAR_MONTH_OUTLINED,
      size=24, 
      color=constants.BLACK
    )
    self.birthdateField = ft.Container(
      padding=ft.padding.all(20),
      border_radius=ft.border_radius.all(10),
      ink=True,
      margin=ft.margin.all(10),
      on_click=self.showDatePicker,
      ink_color=constants.BLACK_INK,
      alignment=ft.alignment.center,
      content=ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          self.birthdateIcon, 
          self.birthdateText
        ]
      )
    )
    
    self.finishButton = CustomFilledButton(
      text="Crear empleado",
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
          controls=[self.birthdateField]
        ),
        ft.Row(
          expand=True,
          alignment=ft.MainAxisAlignment.CENTER,
            controls=[self.finishButton]  
        ),
      ]
    )
    super().__init__(operationContent=self.form)
  
  def showDatePicker(self, e):
    datePicker = CustomDatePicker(
      on_change=lambda e: self.updateBirthdate(datePicker.value.strftime("%Y-%m-%d")),
      on_dismiss=lambda e: self.page.close(datePicker)
    )
    self.page.open(datePicker)
    
  def updateBirthdate(self, date):
    self.birthdateText.value = date
    self.birthdateText.update()
  
  def submitForm(self, e):
    try:
      if evaluateForm(ci=[self.ciField], others=[self.nameField, self.surnameField]):
        if not self.birthdateText.value == "Fecha de nacimiento":
          self.confirmDialog = CustomAlertDialog(
            modal=True,
            title=f"Crear empleado",
            content=ft.Text(
              value=f"Se creará el empleado \"{self.nameField.value} {self.surnameField.value} {self.secondSurnameField.value}\" portador de la cédula \"V-{self.ciField.value}\"",
              size=18,
              color=constants.BLACK,
            ),
            actions=[
              CustomTextButton(text="Confirmar", on_click=self.createEmployee),
              CustomTextButton("Cancelar", on_click=lambda e: self.page.close(self.confirmDialog)),
            ]
          )
          self.page.open(self.confirmDialog)
        else:
          raise InvalidData("No se ha seleccionado una fecha válida")
    except InvalidData:
      self.actionFailed("Selecciona una fecha válida")
      time.sleep(1.5)
      self.restartContainer()
    except Exception as e:
      print(e)
    
  def createEmployee(self, e):
    self.page.close(self.confirmDialog)
    try:
      with getDB() as db:
        newEmployee = createEmployee(
          db=db,
          ciEmployee=self.ciField.value.strip(),
          name=self.nameField.value.strip(),
          surname=self.surnameField.value.strip(),
          secondSurname=self.secondSurnameField.value.strip(),
          birthdate=self.birthdateText.value,
        )
        self.actionSuccess("Empleado creado exitosamente.")
        time.sleep(1.5)
      
      self.employeesContent.resetEmployeesContainer()
      self.employeesContent.resetInfoContainer()
    except DataAlreadyExists as err:
      self.actionFailed(err)
      time.sleep(1.5)
      self.restartContainer()
    except Exception as err:
      print(err)