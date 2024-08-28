import flet as ft
import constants
from Modules.customControls import CustomUserIcon, CustomOperationContainer, CustomTextField, CustomAnimatedContainer, CustomNavigationOptions, CustomFilledButton
from config import getDB
from DataBase.crud.user import getUserByUsername, getUsers, updateUser
import time
from validation import evaluateForm

class UserContainer(ft.Container):
  def __init__(self, initial, username, fullname, role, infoContainer):
    super().__init__()
    self.initial = initial
    self.username = username
    self.fullname = fullname
    self.role = role
    self.infoContainer = infoContainer
    
    self.padding = ft.padding.all(10)
    self.bgcolor=ft.colors.TRANSPARENT
    self.border_radius = ft.border_radius.all(30)
    self.ink = True
    self.ink_color = "#888888"
    self.on_click = self.showUserInfo
    
    self.usernameTitle = CustomAnimatedContainer(
      actualContent=ft.Text(
        value=self.username,
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
          controls=[
            self.usernameTitle,
            ft.Text(
              value=self.fullname,
              size=18,
              color=constants.BLACK,
              overflow=ft.TextOverflow.ELLIPSIS,
            )
          ]
        )
      ]
    )
  
  def showUserInfo(self, e):
    newContent = UserInfo(
      initial=self.initial,
      username=self.username,
      fullname=self.fullname,
      role=self.role,
      animatedUserContainer=self
    )
    self.infoContainer.setNewContent(newContent)
    
  def updateUsername(self, newUsername):
    self.username = newUsername
    self.usernameTitle.setNewContent(ft.Text(
        value=newUsername,
        size=18,
        color=constants.BLACK,
        weight=ft.FontWeight.W_700,
        overflow=ft.TextOverflow.ELLIPSIS,
    ))

class UserInfo(ft.Column):
  def __init__(self, initial, username, fullname, role, animatedUserContainer):
    super().__init__()
    self.initial = initial
    self.username = username
    self.fullname = fullname
    self.role = role
    self.animatedUserContainer = animatedUserContainer
    
    self.scroll = ft.ScrollMode.AUTO
    self.expand = True
    self.alignment = ft.MainAxisAlignment.START
    self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    self.userIcon = CustomUserIcon(
      initial=self.initial, 
      width=100,
      height=100,
      fontSize=42,
      gradient=True,
    )
    
    self.usernameTitle = CustomAnimatedContainer(
      actualContent=ft.Text(
        value=username,
        color=constants.BLACK,
        size=32,
        weight=ft.FontWeight.W_700,
        text_align=ft.TextAlign.CENTER,
      ),
      transition=ft.AnimatedSwitcherTransition.FADE,
      duration=400,
      reverse_duration=200,
    )
    
    self.userRole = ft.Text(
      value=role,
      size=24,
      color=constants.BLACK,
      text_align=ft.MainAxisAlignment.CENTER
    )
    
    self.activityContainer = ft.Container(
      alignment=ft.alignment.center,
      content=ft.Text("No hay nada aquí", color=constants.BLACK,)
    )
    
    self.editButton = CustomNavigationOptions(
      icon=ft.icons.EDIT_ROUNDED,
      text="Editar",
      function=self.selectOption,
      color="#666666",
      focusedColor=constants.BLACK,
      opacityInitial=1,
      highlightColor=None,
      contentAlignment=ft.MainAxisAlignment.CENTER,
      default=True,
    )
    self.activityButton = CustomNavigationOptions(
      icon=ft.icons.ANALYTICS_ROUNDED,
      text="Actividad",
      function=self.selectOption,
      color="#666666",
      highlightColor=None,
      inkColor="#888888",
      opacityInitial=1,
      contentAlignment=ft.MainAxisAlignment.CENTER,
      focusedColor=constants.BLACK,
    )
    self.navigation = ft.Container(
      margin=ft.margin.symmetric(horizontal=20, vertical=10),
      bgcolor=ft.colors.TRANSPARENT,
      padding=ft.padding.symmetric(horizontal=20),
      height=60,
      content=ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        spacing=20,
        controls=[
          self.editButton,
          self.activityButton,
        ]
      )
    )
    
    self.selected = self.editButton
    self.selectedContainer = ft.Container(
      # border=ft.border.all(1, constants.BLACK),
      width=700,
      height=350,
      alignment=ft.alignment.center,
      content=CustomAnimatedContainer(
        actualContent=EditContainer(self.username, infoContainer=self),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=400,
        reverse_duration=200,
      )
    )
    
    self.controls = [
      ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          self.userIcon,
          ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
              self.usernameTitle,
              self.userRole
            ]
          )
          
        ]
      ),
      ft.Divider(color=constants.BLACK_GRAY),
      self.navigation,
      self.selectedContainer,
    ]
  
  def selectOption(self, e):
    if not self.selected == e.control:
      self.selected.deselectOption()
      self.selected = e.control
      self.selected.selectOption()
      
      if e.control == self.editButton:
        self.selectedContainer.content.setNewContent(EditContainer(self.username, self))
      else:
        self.selectedContainer.content.setNewContent(self.activityContainer)
      
  def submitPassword(self, password):
    with getDB() as db:
      user = getUserByUsername(db, self.username)
      
      if password == user.password:
        self.editContainer.actionSuccess("Usuario validado")
        time.sleep(1.5)
        self.validPasswordField.value = ""
        self.editContainer.setNewOperation(ft.Text(
          value="Ingresa aquí el siguiente paso",
          color=constants.BLACK,
          size=32,
        ))
        return True
      else:
        self.editContainer.actionFailed("Contraseña incorrecta")
        time.sleep(1.5)
        self.editContainer.restartContainer()
        return False
      
  def updateUsername(self, newUsername):
    self.username = newUsername
    self.usernameTitle.setNewContent(ft.Text(
      value=newUsername,
        color=constants.BLACK,
        size=32,
        weight=ft.FontWeight.W_700,
        text_align=ft.TextAlign.CENTER,
    ))
    self.animatedUserContainer.updateUsername(newUsername)
      
class EditContainer(CustomOperationContainer):
  def __init__(self, username, infoContainer):
    self.username = username
    self.infoContainer = infoContainer
    self.validPasswordField = CustomTextField(
      label="Contraseña",
      revealPassword=True,
      field="password",
      submitFunction=lambda e: self.submitPassword(self.validPasswordField.value)
    )
    
    self.validateUser = ft.Container(
      height=350,
      width=600,
      alignment=ft.alignment.center,
      content=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=25,
        # expand=True,
        controls=[
          ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
              ft.Icon(
                name=ft.icons.HELP_OUTLINED,
                color=constants.BROWN,
              ),
              ft.Text(
                value="Valida tu identidad",
                size=18,
                color=constants.BLACK,
              )
            ]
          ),
          ft.Row(
            width=300,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[self.validPasswordField]
          ),
        ]
      )
    )
    
    self.usernameField = CustomTextField(
      label="Nombre de Usuario",
      revealPassword=False,
      mode="light",
      hint_text=None,
      field="username",
      expand=False,
      submitFunction=None,
    )
    
    self.passwordField = CustomTextField(
      label="Nueva Contraseña",
      revealPassword=True,
      mode="light",
      hint_text=None,
      field="password",
      expand=False,
      submitFunction=None,
    )
    
    self.showIcon = ft.IconButton(
      icon=ft.icons.VISIBILITY_OFF_ROUNDED,
      icon_color=constants.BLACK,
      on_click=self.showPasswordTemporarily,
    )
    
    with getDB() as db:
      user = getUserByUsername(db, self.username)
      if user:
        self.usernameField.value = user.username
        self.passwordField.value = user.password
    
    self.editProperties = ft.Container(
      height=400,
      width=600,
      alignment=ft.alignment.center,
      content=ft.Column(
        expand=True,
        spacing=25,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
              ft.Icon(
                name=ft.icons.HELP_OUTLINED,
                color=constants.BROWN,
              ),
              ft.Text(
                value="Edita tu usuario",
                size=18,
                color=constants.BLACK,
              )
            ]
          ),
          ft.Column(
            width=300,
            height=100,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
              self.usernameField,
              self.passwordField,
            ]
          ),
          CustomFilledButton(
            text="Enviar",
            overlay=constants.BROWN_OVERLAY,
            bgcolor=constants.BROWN,
            color=constants.WHITE,
            size=24,
            clickFunction=self.submitForm
          )
        ]
      )
    )
    
    self.operationContent = self.validateUser
    super().__init__(self.operationContent, "light")
    
  def submitPassword(self, password):
    with getDB() as db:
      user = getUserByUsername(db, self.username)
      
      print(user.password)
      if password == user.password:
        self.actionSuccess("Usuario validado")
        time.sleep(1.5)
        self.validPasswordField.value = ""
        self.setNewOperation(self.editProperties)
        return True
      else:
        self.actionFailed("Contraseña incorrecta")
        time.sleep(1.5)
        self.restartContainer()
        return False
      
  def showPasswordTemporarily(self, e):
    print("Button clicked")
    self.passwordField.password=False
    # self.showIcon.icon = ft.icons.VISIBILITY_ROUNDED
    self.passwordField.update()
    # self.showIcon.update()
      
    time.sleep(2)
      
    self.passwordField.password = True
    # self.showIcon.icon = ft.icons.VISIBILITY_OFF_ROUNDED
    self.passwordField.update()
    # self.showIcon.update()
    
  def submitForm(self, e):
    with getDB() as db:
      user = getUserByUsername(db, self.username)
      
      try:
        if evaluateForm(username=[self.usernameField], password=[self.passwordField]):
          updatedUser = updateUser(db, user, self.usernameField.value, self.passwordField.value) 
          print(updatedUser)
          
          if updatedUser:
            print(updatedUser.username)
            self.infoContainer.updateUsername(updatedUser.username)
            self.actionSuccess("Usuario editado")
      except Exception as ex:
        print(f"Ocurrió un error: {ex}")
        self.actionFailed("Ocurrió un error")
        time.sleep(1.5)
        self.restartContainer()
      
class NavigationTabs(ft.Container):
  def __init__(self, editContainer, activityContainer):
    super().__init__()
    self.height = 80
     