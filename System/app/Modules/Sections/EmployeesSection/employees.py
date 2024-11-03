import flet as ft
import constants
from config import getDB
from Modules.customControls import CustomAnimatedContainer, CustomAnimatedContainerSwitcher, CustomFloatingActionButton
from Modules.Sections.EmployeesSection.components import EmployeeContainer
from Modules.employees_module import EmployeesForm
import time

from DataBase.crud.employee import getEmployees

class Employees(ft.Stack):
  def __init__(self, page):
    super().__init__()
    self.expand = True
    self.page = page
    self.employees = None
    
    self.employeesContainer = ft.Container(
      col={"sm": 12, "md": 6, "xl": 4},
      margin=ft.margin.symmetric(horizontal=20, vertical=20),
      expand=True,
      alignment=ft.alignment.top_left,
      border_radius=ft.border_radius.all(30),
      bgcolor=constants.WHITE,
      shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=5,
        color=constants.BLACK_INK,
      ),
      content=ft.Column(
        scroll=ft.ScrollMode.AUTO,
        alignment=ft.MainAxisAlignment.START,
        expand=True
      )
    )
    
    self.infoContainer = CustomAnimatedContainerSwitcher(
      col={"sm": 12, "md":6, "xl": 8},
      content=ft.Column(
        controls=[
          ft.Text(value="Selecciona un empleado para ver más información", color=constants.BLACK, size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
      ),
    )
    
    self.fillEmployeesContainer()
    
    self.employeesViews = ft.ResponsiveRow(
      expand = True,
      alignment = ft.MainAxisAlignment.CENTER,
      vertical_alignment = ft.CrossAxisAlignment.CENTER,
      run_spacing = 10,
      controls=[
        self.employeesContainer,
        self.infoContainer,
      ]
    )
    
    self.addEmployeeButton = CustomFloatingActionButton(on_click=self.addEmployee)
    
    self.controls = [
      self.employeesViews,
      ft.Container(
        content=self.addEmployeeButton,
        right=10,
        bottom=10,
      )
    ]
    
  def addEmployee(self, e):
    newContent = EmployeesForm(self.page, self)
    if not self.infoContainer.height == 500:
      self.infoContainer.changeStyle(height=500, width=700, shadow=ft.BoxShadow(
        blur_radius=5,
        spread_radius=1,
        color=constants.BLACK_GRAY,
      ))
    self.infoContainer.setNewContent(newContent=newContent)
  
  def resetInfoContainer(self):
    self.infoContainer.setNewContent(
      newContent=ft.Column(
        controls=[
          ft.Text(value="Selecciona un empleado para ver más información", color=constants.BLACK, size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
      )
    )
    self.infoContainer.changeStyle(height=150, width=700, shadow=None)
    
  def resetEmployeesContainer(self):
    try:
      self.employeesContainer.content.controls.clear()
      self.fillEmployeesContainer()
      self.employeesContainer.update()
    except Exception as e:
      print(e)
  
  def fillEmployeesContainer(self):
    try:
      with getDB() as db:
        self.employees = getEmployees(db)
        if self.employees:
          for employee in self.employees:
            initial = employee.name[0] + employee.surname[0]
            
            fullname = f"{employee.name} {employee.surname} {employee.secondSurname}"
            
            employee = EmployeeContainer(
              initial=initial,
              ciEmployee=employee.ciEmployee,
              name=employee.name,
              surname=employee.surname,
              infoContainer=self.infoContainer,
              secondSurname=employee.secondSurname,
              page=self.page,
              principalContainer=self
            )
            self.employeesContainer.content.controls.append(employee)
    except Exception as e:
      print(f"Error loading employees: {e}")