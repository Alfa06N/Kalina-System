import flet as ft 
import constants
import time
from Modules.customControls import CustomPrincipalContainer, CustomFilledButton, CustomSimpleContainer, CustomOutlinedButton, CustomAnimatedContainer, CustomOperationContainer, CustomTextField, CustomDropdown
from interface import showLogin
from validation import validateUsername, validatePassword, validateCI, validateEmptyField, evaluateForm
from utils.pathUtils import getImagePath

class RecoveryForm(CustomSimpleContainer):
  def __init__(self, page):
    super().__init__()
    self.spacing = 10
    self.page = page
    self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    self.title = CustomAnimatedContainer(
      actualContent=ft.Row(
        controls=[
          ft.Text(value="¿Quién eres?", color=constants.BLACK, size=42, weight=ft.FontWeight.BOLD),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
      ),
      transition=ft.AnimatedSwitcherTransition.FADE,
      duration=300,
      reverse_duration=200,
    )
    
    self.username = CustomTextField(
      label="Nombre de Usuario",
      revealPassword=False,
      mode="light",
      hint_text=None,
      field="username",
      expand=False,
      submitFunction=self.nextStep,
    )
    
    self.nextButton = CustomOutlinedButton(
      text="Siguiente", 
      color=constants.BLACK, 
      size=18, 
      icon=None, 
      clickFunction=self.nextStep
    )
    
    self.userCI = CustomTextField(
      label="Documento de Empleado",
      revealPassword=False,
      mode="light",
      hint_text=None,
      field="ci",
      expand=False, 
      submitFunction=self.nextStep,
    )
    
    self.identifyUser = ft.Column(
      expand=True,
      spacing=20,
      height=300,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Row(
          controls=[
            ft.Icon(
              name=ft.icons.HELP_OUTLINED,
              color=constants.BROWN,
            ),
            ft.Text(value="Identifica tu usuario", size=18, color=constants.BLACK)
          ],
          alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Column(
          expand=True,
          controls=[
            self.username,
            self.userCI,
          ],
          alignment=ft.MainAxisAlignment.CENTER
        ),
        self.nextButton,
      ]
    )
    
    self.questionField = CustomDropdown(
      label="Pregunta de Seguridad",
      options=constants.dropdownOne,
      mode="light"
    )
    
    self.responseField = CustomTextField(
      label="Respuesta",
      revealPassword=False,
      mode="light",
      hint_text=None,
      field="others",
      expand=False,
      submitFunction=self.nextStep,
    )
    
    self.verifyUser = ft.Column(
      spacing=20,
      height=300,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Row(
          controls=[
            ft.Icon(
              name=ft.icons.HELP_OUTLINED,
              color=constants.BROWN,
            ),
            ft.Text(value="Responde para verificar tu identidad", size=18, color=constants.BLACK),
          ],
          alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Column(
          expand=True,
          controls=[
            self.questionField,
            self.responseField,
          ],
          alignment=ft.MainAxisAlignment.CENTER
        ),
        self.nextButton,
      ]
    )
    
    self.passwordField = CustomTextField(
      label="Contraseña",
      revealPassword=True,
      field="password",
      submitFunction=self.nextStep,
    )
    
    self.passwordConfirmationField = CustomTextField(
      label="Confirmar Contraseña",
      field="password",
      submitFunction=self.nextStep,
    )
    
    self.passwordChange = ft.Column(
      spacing=20,
      height=300,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Row(
          controls=[
            ft.Icon(
              name=ft.icons.HELP_OUTLINED,
              color=constants.BROWN,
            ),
            ft.Text(value="Establece tu nueva contraseña", size=18, color=constants.BLACK)
          ],
          alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Column(
          expand=True,
          controls=[
            self.passwordField,
            self.passwordConfirmationField,
          ],
          alignment=ft.MainAxisAlignment.CENTER, 
        ),
        self.nextButton
      ],
    )
    
    self.animatedContainer = CustomOperationContainer(
      operationContent=self.identifyUser,
      mode="light"
    )
    
    self.recoveryContent = ft.Column(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      controls=[self.animatedContainer]
    )
    
    self.content = ft.Column(
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        self.title,
        self.recoveryContent,
      ]
    )
    
    self.forms = [
      self.username,
      self.userCI,
    ]
    self.containers = [self.identifyUser, self.verifyUser, self.passwordChange]
    self.count = 0
  
  def nextStep(self, e):
    isValid = False
    message = ""
    if self.count == 0:
      if evaluateForm(username=[self.username], ci=[self.userCI]):
        self.count += 1
        isValid = True
        message = "Usuario Identificado"
        self.title.setNewContent(ft.Row(
          controls=[
            ft.Text(value=self.username.value, size=42, weight=ft.FontWeight.BOLD, color=constants.BLACK)
          ],
          alignment=ft.MainAxisAlignment.CENTER
        ))
        
    elif self.count == 1:
      if evaluateForm(others=[self.questionField, self.responseField]):
        self.count += 1
        isValid = True
        message = "Usuario Verificado"
    
    else:
      if evaluateForm(password=[self.passwordField, self.passwordConfirmationField]):
        if self.passwordField.value == self.passwordConfirmationField.value:
          isValid = True
          self.count += 1
          message = "Contraseña Establecida"
        else:
          isValid = False
          message = "Las contraseñas no coinciden"
          self.animatedContainer.actionFailed(message)
          time.sleep(2)
          self.animatedContainer.restartContainer()
    
    if isValid:
      self.animatedContainer.actionSuccess(message)
      time.sleep(2)
      if self.count < len(self.containers):
        self.animatedContainer.setNewOperation(self.containers[self.count])
    
    
class RecoveryPresentation(CustomSimpleContainer):
  def __init__(self, page):
    super().__init__(gradient=True)
    self.page = page
    
    self.title = ft.Text(
      value="Recupera tu acceso",
      size=42,
      text_align=ft.TextAlign.CENTER,
      weight=ft.FontWeight.BOLD,
      color=constants.WHITE
    )
    
    self.button = CustomFilledButton(
      text="Iniciar Sesión",
      size=18,
      color=constants.BLACK,
      bgcolor=constants.ORANGE,
      overlay=constants.ORANGE_OVERLAY,
      clickFunction=lambda e: showLogin(self.page)
    )
    
    self.img = ft.Image(
      src=getImagePath("gifCDC-kalinaSystem.gif"),
      fit="contain", 
      width=240, 
      height=240
    )
    
    self.description = ft.Text(
      value="No te preocupes, todos olvidamos cosas a veces.",
      text_align=ft.TextAlign.CENTER,
      size=18, 
      color=constants.WHITE,
      weight=ft.FontWeight.BOLD
    )
    
    self.content = ft.Column(
      spacing=10,
      controls=[
        self.title, 
        self.img,
        self.button,
        self.description,
      ],
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
class Recovery(ft.Row):
  def __init__(self, page):
    super().__init__()
    self.page = page
    
    self.controls = [
      RecoveryForm(self.page),
      RecoveryPresentation(self.page),
    ]
  