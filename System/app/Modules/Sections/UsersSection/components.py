import flet as ft
import constants
from Modules.customControls import CustomUserIcon, CustomOperationContainer, CustomTextField, CustomAnimatedContainer, CustomNavigationOptions, CustomFilledButton, CustomDropdown, CustomDeleteButton, CustomAlertDialog, CustomReturnButton
from config import getDB
from DataBase.crud.user import getUserByUsername, getUsers, updateUser, removeUser
from Modules.Sections.SalesSection.history_components import SaleContainer, SaleRecord
from DataBase.crud.sale import getSalesByUser
from DataBase.crud.recovery import getRecoveryByUserId, updateRecovery
import time
from validation import evaluateForm
from exceptions import DataAlreadyExists, DataNotFoundError
from utils.sessionManager import getCurrentUser, setUser

class UserContainer(ft.Container):
  def __init__(self, page, initial, username, fullname, role, infoContainer, mainContainer):
    super().__init__()
    self.initial = initial
    self.username = username
    self.fullname = fullname
    self.role = role
    self.page = page
    self.infoContainer = infoContainer
    self.spacing = 0
    self.mainContainer = mainContainer
    
    self.padding = ft.padding.all(10)
    self.border = ft.border.all(2, constants.BLACK_INK)
    self.bgcolor= constants.WHITE
    self.border_radius = ft.border_radius.all(30)
    self.on_click = self.showUserInfo
    self.animate = ft.animation.Animation(
      300, ft.AnimationCurve.EASE
    )
    
    self.usernameTitle = CustomAnimatedContainer(
      actualContent=ft.Text(
        value=self.username,
        size=20,
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
            self.usernameTitle,
            ft.Text(
              value=self.fullname,
              size=20,
              color=constants.BLACK,
              overflow=ft.TextOverflow.ELLIPSIS,
            )
          ]
        )
      ]
    )
  
  def showUserInfo(self, e):
    if not self.mainContainer.controlSelected == self:
      newContent = UserInfo(
        initial=self.initial,
        page=self.page,
        username=self.username,
        fullname=self.fullname,
        role=self.role,
        principalContainer=self.mainContainer,
        userContainer=self
      )
      self.mainContainer.showContentInfo(newContent, self)
      
  def select(self):
    self.border = ft.border.all(2, constants.BLACK_GRAY)
    self.bgcolor = constants.ORANGE
    self.update()
  
  def deselect(self):
    self.border = ft.border.all(2, constants.BLACK_INK)
    self.bgcolor = constants.WHITE
    
    self.update()
    
  def updateUsername(self, newUsername):
    self.username = newUsername
    self.usernameTitle.setNewContent(ft.Text(
        value=newUsername,
        size=20,
        color=constants.BLACK,
        weight=ft.FontWeight.W_700,
        overflow=ft.TextOverflow.ELLIPSIS,
    ))

class UserInfo(ft.Container):
  def __init__(self, page, initial, username, fullname, role, userContainer, principalContainer):
    super().__init__()
    self.initial = initial
    self.username = username
    self.fullname = fullname
    self.role = role
    self.page = page
    self.userContainer = userContainer
    self.principalContainer = principalContainer
    
    self.expand = True
    
    self.userIcon = CustomUserIcon(
      initial=self.initial, 
      width=100,
      height=100,
      fontSize=42,
      gradient=True,
    )
    
    self.usernameTitle = CustomAnimatedContainer(
      actualContent=ft.Text(
        value=self.username,
        color=constants.BLACK,
        size=24,
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
      width=700,
      height=300,
      alignment=ft.alignment.center,
      content=CustomAnimatedContainer(
        actualContent=EditContainer(self.username, infoContainer=self),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=400,
        reverse_duration=200,
      )
    )
    
    self.columnContent = ft.Column(
      scroll=ft.ScrollMode.AUTO,
      expand=True,
      alignment=ft.MainAxisAlignment.START,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
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
    )
    
    self.deleteButton = CustomDeleteButton(
      page=self.page,
      function=self.deleteUser
    )
    
    self.originalContent = ft.Stack(
      expand=True,
      controls=[
        self.columnContent,
        ft.Container(
          content=self.deleteButton,
          right=10,
          top=10,
        )
      ]
    )
    
    self.mainContent = CustomAnimatedContainer(
      actualContent=self.originalContent,
    )
    
    self.content = self.mainContent
    
  def deleteUser(self):
    try:
      if self.username == getCurrentUser():
        dialog = CustomAlertDialog(
          title="Operación bloqueada",
          content=ft.Text(
            value=f"No puedes eliminar al usuario de la sesión actual",
            size=18,
            color=constants.BLACK,  
          ),
          modal=False,
        )
        self.page.open(dialog)
      else:
        with getDB() as db:
          user = getUserByUsername(db, self.username)
          
          if user:
            user = removeUser(db, user)
            self.principalContainer.resetUsersContainer()
            self.principalContainer.resetInfoContainer()
          else:
            raise DataNotFoundError(f"Can't delete user '{self.username}'")
    except DataNotFoundError:
      raise
    except Exception as err:
      raise
  
  def selectOption(self, e):
    if not self.selected == e.control:
      self.selected.deselectOption()
      self.selected = e.control
      self.selected.selectOption()
      
      if e.control == self.editButton:
        self.selectedContainer.content.setNewContent(EditContainer(self.username, self))
      else:
        self.selectedContainer.content.setNewContent(ActivityContainer(self.username, self))
      
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
          size=20,
        ))
        return True
      else:
        self.editContainer.actionFailed("Contraseña incorrecta")
        time.sleep(1.5)
        self.editContainer.restartContainer()
        return False
    
  def showAdditionalContent(self, newContent):
    try:
      newContent = ft.Stack(
        expand=True,
        controls=[
          newContent,
          ft.Container(
            content=CustomReturnButton(
              function=lambda e: self.returnToMainContent()
            ),
            left=10,
            top=10,
          )
        ]
      )
      self.mainContent.setNewContent(newContent)
    except Exception:
      raise
  
  def returnToMainContent(self):
    try:
      self.mainContent.setNewContent(self.originalContent)
    except Exception:
      raise
      
  def updateUsername(self, newUsername):
    self.username = newUsername
    self.usernameTitle.setNewContent(ft.Text(
      value=newUsername,
        color=constants.BLACK,
        size=24,
        weight=ft.FontWeight.W_700,
        text_align=ft.TextAlign.CENTER,
    ))
    self.userContainer.updateUsername(newUsername)
    
class ActivityContainer(ft.Container):
  def __init__(self, username, infoContainer):
    super().__init__()
    self.username = username
    self.infoContainer = infoContainer
    
    with getDB() as db:
      user = getUserByUsername(db, self.username)
      sales = getSalesByUser(db, user.idUser)
      
      self.salesList = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
      )

      if len(sales) == 0:
        self.salesList.controls.append(ft.Container(
          expand=True,
          alignment=ft.alignment.center,
          content=ft.Text(
            value="Este usuario no ha realizado ventas",
            color=constants.BLACK,
            size=24,
            weight=ft.FontWeight.W_600,
          )
        ))
      else: 
        for sale in sales:
          container = SaleContainer(
            page=self.page, 
            idSale=sale.idSale,
            infoContainer=None,
            mainContainer=None,
          )
          container.on_click = lambda e: self.infoContainer.showAdditionalContent(SaleRecord(
            page=self.page,
            idSale=sale.idSale
          ))
          self.salesList.controls.append(container)
    
    self.content = self.salesList
      
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
      alignment=ft.alignment.center,
      content=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        expand=True,
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
                size=20,
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
    
    with getDB() as db:
      user = getUserByUsername(db, self.username)
      if user:
        self.usernameField.value = user.username
        self.passwordField.value = user.password
    
    self.editProperties = ft.Container(
      alignment=ft.alignment.center,
      padding=ft.padding.symmetric(vertical=10),
      content=ft.Column(
        expand=True,
        spacing=10,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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
                size=20,
                color=constants.BLACK,
              )
            ]
          ),
          ft.Column(
            expand=True,
            width=400,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
              self.usernameField,
              self.passwordField,
            ]
          ),
          CustomFilledButton(
            text="Enviar",
            clickFunction=self.submitForm
          ) 
        ]
      )
    )
    
    self.questionOne = CustomDropdown(
      label="Pregunta 1",
      options=constants.dropdownOne,
      mode="light",
      expand=True,
    )
    self.answerOne = CustomTextField(
      label="Respuesta",
      field="others",
      revealPassword=True,
      submitFunction=None,
      expand=True,
    )
    self.questionTwo = CustomDropdown(
      label="Pregunta 2",
      expand=True,
      options=constants.dropdownTwo,
      mode="light",
    )
    self.answerTwo = CustomTextField(
      label="Respuesta",
      field="others",
      revealPassword=True,
      submitFunction=None,
      expand=True,
    )
    self.finishButton = CustomFilledButton(
      text="Guardar cambios",
      clickFunction=self.submitSecretQuestions,
    )
    self.editSecretQuestions = ft.Container(
      padding=ft.padding.symmetric(vertical=10),
      content=ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
              ft.Icon(
                name=ft.icons.HELP_OUTLINED,
                color=constants.BLACK,
              ),
              ft.Text(
                value="Preguntas de seguridad",
                size=18,
                color=constants.BLACK,
              )
            ]
          ),
          ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
              self.questionOne,
              self.answerOne,
            ]
          ),
          ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
              self.questionTwo,
              self.answerTwo,
            ]
          ),
          self.finishButton
        ]
      )
    )
    
    self.operationContent = self.validateUser
    super().__init__(self.operationContent, "light")
    
  def submitSecretQuestions(self, e):
    try:
      if evaluateForm(others=[self.questionOne, self.answerOne, self.questionTwo, self.answerTwo]):
        with getDB() as db:
          user = getUserByUsername(db, self.username)
          newRecovery = updateRecovery(db, user.idUser, self.questionOne.value, self.answerOne.value, self.questionTwo.value, self.answerTwo.value)
          
          if newRecovery:
            self.actionSuccess("Preguntas de seguridad actualizadas")
            time.sleep(1.5)
            self.setNewOperation(newContent=self.validateUser)
    except Exception as e:
      print(e)
      self.actionFailed("Algo salió mal")
      time.sleep(1.5)
      self.restartContainer()
    
  def submitPassword(self, password):
    with getDB() as db:
      user = getUserByUsername(db, self.username)

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
    
  def submitForm(self, e):
    with getDB() as db:
      user = getUserByUsername(db, self.username)
      currentSessionUser = getCurrentUser()
      
      try:
        if evaluateForm(username=[self.usernameField], password=[self.passwordField]):
          updatedUser = updateUser(db, user, self.usernameField.value, self.passwordField.value) 
          
          if updatedUser:
            self.infoContainer.updateUsername(updatedUser.username)
            self.actionSuccess("Usuario editado")
            time.sleep(1.5)
            self.setNewOperation(newContent=self.editSecretQuestions)
            if user.username == currentSessionUser:
              setUser(updatedUser.username)
      except DataAlreadyExists as err:
        self.actionFailed(err)
        time.sleep(1.5)
        self.restartContainer()
      except Exception as ex:
        print(f"Ocurrió un error: {ex}")
        self.actionFailed("Ocurrió un error")
        time.sleep(1.5)
        self.restartContainer()