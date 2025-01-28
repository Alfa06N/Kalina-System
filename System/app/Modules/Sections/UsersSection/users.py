import flet as ft
import constants
from DataBase.crud.user import getUsers, getUserByUsername, createUser
from config import getDB
from Modules.customControls import CustomUserIcon, CustomAnimatedContainer, CustomOperationContainer, CustomTextField, CustomAnimatedContainerSwitcher, CustomFloatingActionButton
from Modules.Sections.UsersSection.components import UserContainer
import time
import threading
from Modules.register_module import RegisterForm

class Users(ft.Stack):
  def __init__(self, page):
    super().__init__()
    self.expand = True
    self.page = page
    
    self.users = None
    self.usersContainer = ft.Container(
      col={"sm": 12, "md": 6, "xl": 4},
      margin=ft.margin.symmetric(horizontal=20, vertical=20),
      expand=True,
      alignment=ft.alignment.top_left,
      border_radius=ft.border_radius.all(30),
      bgcolor=constants.WHITE,
      shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=5,
        color=constants.BLACK_INK
      ),
      content=ft.Column(
        alignment=ft.MainAxisAlignment.START,
        expand=True,
      )
    )
    
    self.infoContainer = CustomAnimatedContainerSwitcher(
      content=ft.Column(
        controls=[
          ft.Text(value="Selecciona un usuario para ver más información", color=constants.BLACK, size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
      ),
      col={"sm": 12, "md": 6, "xl": 8},
    )
    
    self.controlSelected = None
    
    self.fillUsersContainer()
      
    self.usersViews = ft.ResponsiveRow(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      run_spacing=10,
      controls=[
        self.usersContainer,
        self.infoContainer,
      ]
    )
    
    self.addUserButton = CustomFloatingActionButton(
      on_click=lambda e: self.addRegisterForm(),
    )
    
    self.controls = [
      self.usersViews,
      ft.Container(
        content=self.addUserButton,
        right=10,
        bottom=10,
      )
    ]
    
  def resetInfoContainer(self):
    self.infoContainer.setNewContent(
      newContent=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        controls=[
          ft.Text(
            value="Selecciona un usuario para ver más información",
            color=constants.BLACK, size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER
          )
        ],
      )
    )
    self.controlSelected = None
    self.infoContainer.changeStyle(height=150, width=700, shadow=None)
    
  def resetUsersContainer(self):
    try:
      self.usersContainer.content.controls.clear()
      self.fillUsersContainer()
      self.usersContainer.update()
      self.controlSelected = None
    except Exception as err:
      raise
  
  def resetAll(self):
    self.resetUsersContainer()
    self.resetInfoContainer()
    
  def fillUsersContainer(self):
    try:
      with getDB() as db:
        self.users = getUsers(db)
        if self.users:
          for user in self.users:
            initial = user.employee.name[0] + user.employee.surname[0]
            
            fullname = f"{user.employee.name} {user.employee.surname} {user.employee.secondSurname}"
            
            user = UserContainer(
              initial=initial,
              username=user.username,
              fullname=fullname,
              role=user.role,
              page=self.page,
              mainContainer=self,
              infoContainer=self.infoContainer
            )
            self.usersContainer.content.controls.append(user)
    except Exception as err:
      print(f"Error loading users: {err}")
  
  def addRegisterForm(self):
    if not self.infoContainer.height == 550:
      self.infoContainer.changeStyle(
        height=600, width=500, shadow=ft.BoxShadow(
          blur_radius=5,
          spread_radius=1,
          color=constants.BLACK_INK,
        ),
        bgcolor=constants.WHITE,
      )
      
      form = RegisterForm(
        page=self.page,
        login=False,
      )
      form.width = None
      form.height = None
      form.expand = True
      
      def customSubmitForm():
        try:
          result = form.advance()
          if result:
            threading.Timer(1, self.resetAll).start()
        except:
          raise
      
      form.finishButton.on_click = lambda e: customSubmitForm()
      form.adminUsernameField.on_submit = lambda e: customSubmitForm()
      form.adminPasswordField.on_submit = lambda e: customSubmitForm()
      
      self.infoContainer.setNewContent(form)
  
  def showContentInfo(self, content, container):
    if self.controlSelected:
      self.controlSelected.deselect()
    self.controlSelected = container
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