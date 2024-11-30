import flet as ft 
import constants
import time
from Modules.customControls import CustomPrincipalContainer, CustomFilledButton, CustomSimpleContainer, CustomOutlinedButton, CustomAnimatedContainer, CustomOperationContainer, CustomTextField, CustomDropdown
from interface import showLogin
from validation import validateUsername, validatePassword, validateCI, validateEmptyField, evaluateForm
from utils.pathUtils import getImagePath
from DataBase.crud.user import getUserByUsername, getUserById, updateUser
from DataBase.crud.recovery import updateRecovery
from DataBase.crud.employee import getEmployeeById
from exceptions import DataAlreadyExists, DataNotFoundError, InvalidData
import threading
from config import getDB

class RecoveryForm(CustomSimpleContainer):
  def __init__(self, page):
    super().__init__()
    self.spacing = 10
    self.page = page
    self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    self.idUser = None
    
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
      options=[],
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
    try:
      isValid = False
      message = ""
      if self.count == 0:
        message = self.identifyUserFunction()
        if message:
          isValid = True
          self.count += 1
          self.title.setNewContent(ft.Row(
            controls=[
              ft.Text(value=self.username.value.strip(), size=42, weight=ft.FontWeight.BOLD, color=constants.BLACK, text_align=ft.TextAlign.CENTER)
            ],
            alignment=ft.MainAxisAlignment.CENTER
          ))
          
      elif self.count == 1:
        message = self.verifyUserFunction()
        if message:
          self.count += 1
          isValid = True
      
      else:
        message = self.passwordChangeFunction()
        if message:
          isValid = True
          self.count += 1
      
      if isValid:
        self.animatedContainer.actionSuccess(message)
        time.sleep(2)
        if self.count < len(self.containers):
          self.animatedContainer.setNewOperation(self.containers[self.count])
        elif self.count == len(self.containers):
          threading.Timer(1.5, lambda: showLogin(self.page)).start()
    except InvalidData as err:
      self.animatedContainer.actionFailed(err)
      threading.Timer(1.5, self.animatedContainer.restartContainer).start()
    except DataAlreadyExists as err:
      self.animatedContainer.actionFailed(err)
      threading.Timer(1.5, self.animatedContainer.restartContainer).start()
    except DataNotFoundError as err:
      self.animatedContainer.actionFailed(err)
      threading.Timer(1.5, self.animatedContainer.restartContainer).start()
    except Exception as err:
      raise
  
  def getQuestions(self):
    try:
      with getDB() as db:
        user = getUserById(db, self.idUser)
        questions = []
        
        questions.append(ft.dropdown.Option(user.recovery.questionOne))
        questions.append(ft.dropdown.Option(user.recovery.questionTwo))
        
        return questions
    except Exception as err:
      pass
  
  def identifyUserFunction(self):
    try:
      if evaluateForm(username=[self.username], ci=[self.userCI]):
        with getDB() as db:
          user = getUserByUsername(db, self.username.value.strip())
          employee = getEmployeeById(db, self.userCI.value)
          
          if not user:
            raise DataNotFoundError("Usuario no encontrado.")
          elif not employee:
            raise DataNotFoundError("Empleado no encontrado.")
          elif not user.employee.ciEmployee == employee.ciEmployee:
            raise DataNotFoundError("Los datos no tienen relación.")

          self.idUser = user.idUser
          self.questionField.options = self.getQuestions()
          message = "Usuario identificado."
          
          return message
    except Exception as err:
      raise
  
  def verifyUserFunction(self):
    try:
      isValid = False
      if evaluateForm(others=[self.questionField, self.responseField]):
        with getDB() as db:
          user = getUserById(db, self.idUser)
          if self.questionField.value == user.recovery.questionOne:
            isValid = self.responseField.value.strip() == user.recovery.answerOne
          elif self.questionField.value == user.recovery.questionTwo:
            isValid = self.responseField.value.strip() == user.recovery.answerTwo
      
      if isValid:
        message = "Usuario Verificado."
        return message
      else:
        raise DataNotFoundError("La respuesta es incorrecta.")
    except Exception as err:
      raise

  def passwordChangeFunction(self):
    try:
      if evaluateForm(password=[self.passwordField, self.passwordConfirmationField]):
        with getDB() as db:
          user = getUserById(db, self.idUser)
          if self.passwordField.value.strip() == self.passwordConfirmationField.value.strip():
            user.password = self.passwordField.value.strip()
            db.commit()
            db.refresh(user)
            
            message = "Contraseña establecida."
            return message
          else:
            raise InvalidData("Las contraseñas no coinciden.")
    except Exception as err:
      raise
    
    
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
      overlay=constants.ORANGE_OVERLAY,
      bgcolor=constants.ORANGE,
      color=constants.BLACK,
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
  