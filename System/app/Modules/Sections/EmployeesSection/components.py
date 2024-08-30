import flet as ft 
from Modules.customControls import CustomAnimatedContainer, CustomOperationContainer, CustomUserIcon, CustomCardInfo
import constants
from DataBase.crud.employee import getEmployeeById
from config import getDB
import time
from exceptions import DataAlreadyExists, DataNotFoundError

class EmployeeContainer(ft.Container):
  def __init__(self, ciEmployee, initial, name, surname, infoContainer, secondSurname=""):
    super().__init__()
    self.initial = initial
    self.ciEmployee = ciEmployee
    self.name = name
    self.surname = surname
    self.secondSurname = secondSurname
    self.infoContainer = infoContainer
    
    self.padding = ft.padding.all(10)
    self.bgcolor = ft.colors.TRANSPARENT
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
      employeeContainer=self,
    )
    if not self.infoContainer.height == 400:
      self.infoContainer.changeStyle(height=400, width=700, shadow=ft.BoxShadow(
        blur_radius=5,
        spread_radius=1,
        color=constants.BLACK_GRAY,
      ))
      time.sleep(0.3)
    self.infoContainer.setNewContent(newContent=newContent)
    
    
class EmployeeInfo(ft.Column):
  def __init__(self, ciEmployee, initial, name, surname, secondSurname, employeeContainer):
    super().__init__()
    self.initial = initial
    self.ciEmployee = ciEmployee
    self.name = name
    self.surname = surname
    self.secondSurname = secondSurname
    self.employeeContainer = employeeContainer
    
    self.scroll = ft.ScrollMode.AUTO 
    self.expand = True
    self.alignment = ft.MainAxisAlignment.START
    self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
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
    
    self.userInfo = None
    
    try:
      with getDB() as db:
        employee = getEmployeeById(db, self.ciEmployee)
        
        if employee:
          if employee.user:
            self.userInfo = ft.Column(
              alignment=ft.MainAxisAlignment.CENTER,
              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
              height=200,
              controls=[
                ft.Text(
                  value=f"Usuario de {self.name}",
                  color=constants.BLACK,
                  size=18,
                ),
                CustomCardInfo(
                  icon=ft.icons.SECURITY_ROUNDED,
                  title=employee.user.username,
                  subtitle=employee.user.role,
                  containerClickFunction=None,
                  variant=ft.CardVariant.OUTLINED,
                )
              ]
            )
            print("Si tiene usuario")
          else:
            self.userInfo = ft.Column(
              alignment=ft.MainAxisAlignment.CENTER,
              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
              height=200,
              controls=[
                ft.Text(
                  value=f"El empleado no posee un usuario",
                  size=18,
                  color=constants.BLACK,
                ),
              ]
            )
            print("No tiene usuario")
        else:
          raise DataNotFoundError("No se encontró el empleado")
        
    except Exception as e:
      print(e)
      # raise
    self.controls = [
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
      self.userInfo,
    ]