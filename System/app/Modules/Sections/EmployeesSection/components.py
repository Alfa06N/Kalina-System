import flet as ft 
from Modules.customControls import CustomAnimatedContainer, CustomOperationContainer, CustomUserIcon, CustomCardInfo, CustomDeleteButton
import constants
from DataBase.crud.employee import getEmployeeById, removeEmployee, calculateAge
from config import getDB
import time
from exceptions import DataAlreadyExists, DataNotFoundError

class EmployeeContainer(ft.Container):
  def __init__(self, page, ciEmployee, initial, name, surname, infoContainer, principalContainer, secondSurname=""):
    super().__init__()
    self.initial = initial
    self.ciEmployee = ciEmployee
    self.name = name
    self.surname = surname
    self.secondSurname = secondSurname
    self.infoContainer = infoContainer
    self.principalContainer = principalContainer
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
    self.on_click = self.showEmployeeInfo
    
    self.employeeTitle = CustomAnimatedContainer(
      actualContent=ft.Text(
        value=f"{self.name} {self.surname} {self.secondSurname}",
        size=18,
        color=constants.BLACK,
        weight=ft.FontWeight.W_700,
        overflow=ft.TextOverflow.ELLIPSIS,
      ),
      transition=ft.AnimatedSwitcherTransition.FADE,
      duration=400,
      reverse_duration=200,
    )
    
    self.content = ft.Row(
      expand=True,
      alignment=ft.MainAxisAlignment.START,
      controls=[
        CustomUserIcon(
          initial=self.initial,
          gradient=True,
        ),
        ft.Column(
          expand=True,
          alignment=ft.MainAxisAlignment.CENTER,
          spacing=0,
          controls=[
            self.employeeTitle,
            ft.Text(
              value=f"V-{self.ciEmployee}",
              size=18,
              color=constants.BLACK,
              overflow=ft.TextOverflow.ELLIPSIS
            )
          ]
        )
      ]
    )
    
  def showEmployeeInfo(self, e):
    newContent = EmployeeInfo(
      initial=self.initial,
      ciEmployee=self.ciEmployee,
      name=self.name,
      surname=self.surname,
      secondSurname=self.secondSurname,
      page=self.page,
      employeeContainer=self,
      principalContainer=self.principalContainer
    )
    if not self.infoContainer.height == 400:
      self.infoContainer.changeStyle(height=400, width=700, shadow=ft.BoxShadow(
        blur_radius=5,
        spread_radius=1,
        color=constants.BLACK_GRAY,
      ))
    self.infoContainer.setNewContent(newContent=newContent)
    
class EmployeeInfo(ft.Stack):
  def __init__(self, page, ciEmployee, initial, name, surname, secondSurname, employeeContainer, principalContainer):
    super().__init__()
    self.initial = initial
    self.ciEmployee = ciEmployee
    self.name = name
    self.surname = surname
    self.secondSurname = secondSurname
    self.employeeContainer = employeeContainer
    self.page = page
    self.principalContainer = principalContainer
    
    self.expand = True
    
    self.employeeIcon = CustomUserIcon(
      initial=self.initial,
      width=100,
      height=100,
      fontSize=42,
      gradient=True,
    )
    
    self.employeeTitle = ft.Text(
      value=f"{self.name} {self.surname} {self.secondSurname}",
      color=constants.BLACK,
      size=24,
      weight=ft.FontWeight.W_700,
      text_align=ft.TextAlign.CENTER,
    )
    
    self.employeeCi = ft.Text(
      value=f"V-{self.ciEmployee}",
      color=constants.BLACK,
      size=24,
    )
    
    self.birthdateText = ft.Text(
      size=18,
      color=constants.BLACK,
    )
    self.ageText = ft.Text(
      size=18,
      color=constants.BLACK,
    )
    self.birthdateIcon = ft.Icon(
      name=ft.icons.CALENDAR_MONTH_OUTLINED,
      size=28, 
      color=constants.BLACK
    )
    self.birthdateField = ft.Container(
      padding=ft.padding.all(20),
      border_radius=ft.border_radius.all(10),
      margin=ft.margin.all(10),
      content=ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          self.birthdateIcon, 
          ft.Column(
            controls=[
              ft.Row(
                controls=[
                  ft.Text(
                    value="Fecha de nacimiento:",
                    size=18,
                    color=constants.BLACK,
                    weight=ft.FontWeight.BOLD,
                  ),
                  self.birthdateText
                ]
              ),
              ft.Row(
                controls=[
                  ft.Text(
                    value="Edad:",
                    size=18,
                    color=constants.BLACK,
                    weight=ft.FontWeight.BOLD,
                  ),
                  self.ageText
                ]
              ),
            ]
          ),
        ]
      )
    )
    
    self.employeeInfo = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      height=200,
      controls=[
        self.birthdateField,
        # Also add the userInfo
      ]
    )
    
    try:
      with getDB() as db:
        employee = getEmployeeById(db, self.ciEmployee)
        
        if employee:
          
          self.birthdateText.value = f"{employee.birthdate.strftime("%Y-%m-%d")}"
          self.ageText.value = f"{calculateAge(employee)} años"
          
          if employee.user:
            self.employeeInfo.controls.append(ft.Container(
              padding=10,
              content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                  ft.Icon(
                    name=ft.icons.SECURITY_ROUNDED,
                    color=constants.BLACK,
                    size=28,
                  ),
                  ft.Text(
                    value=f"Usuario:",
                    size=18,
                    color=constants.BLACK,
                    weight=ft.FontWeight.BOLD,
                  ),
                  ft.Text(
                    value=f"{employee.user.username} ({employee.user.role})",
                    size=18,
                    color=constants.BLACK,
                  )
                ]
                
              ),
            ))
          else:
            self.employeeInfo.controls.append(ft.Text(
              value=f"Este empleado no posee un usuario",
              size=18,
              color=constants.BLACK,
            ))
        else:
          raise DataNotFoundError("No se encontró el empleado")
        
    except Exception as e:
      raise
      
    self.columnContent = ft.Column(
      scroll=ft.ScrollMode.AUTO,
      expand=True,
      alignment=ft.MainAxisAlignment.START,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          expand=False,
          vertical_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            self.employeeIcon,
            ft.Column(
              alignment=ft.MainAxisAlignment.CENTER,
              controls=[
                self.employeeTitle,
                self.employeeCi,
              ]
            )
          ]
        ), 
        ft.Divider(color=constants.BLACK_GRAY),
        self.employeeInfo,
      ]
    )
    
    self.deleteButton = CustomDeleteButton(
      page=self.page,
      function=self.deleteEmployee,
    )
    
    # Stack controls
    self.controls = [
      self.columnContent,
      ft.Container(
        content=self.deleteButton,
        right=10,
        top=10,
      )
    ]
  
  def deleteEmployee(self):
    try:
      with getDB() as db:
        employee = getEmployeeById(db, self.ciEmployee)
        
        if employee:
          employee = removeEmployee(db, employee)
          self.principalContainer.resetEmployeesContainer()
          self.principalContainer.resetInfoContainer()
        else: 
          raise DataNotFoundError(f"Can't delete employee V-{self.ciEmployee}")
    except DataNotFoundError:
      raise
    except Exception as err:
      print(f"Error deleting employee V-{self.ciEmployee}: {err}")