import flet as ft 
from Modules.customControls import CustomFilledButton, CustomOutlinedButton, CustomCheckbox, CustomReturnButton, CustomSimpleContainer, CustomTextField, CustomDropdown, CustomAnimatedContainer, CustomOperationContainer
from validation import evaluateForm, validateUsername, validatePassword, validateCI
import constants
from interface import showLogin
import time
from utils.pathUtils import getImagePath

class RegisterForm(CustomSimpleContainer):
  def __init__(self, page):
    super().__init__(height=500, width=450, gradient=True)
    self.page = page
    
    self.button = ft.Row(
      controls=[
        CustomOutlinedButton(text="Siguiente", color=constants.WHITE, size=18, icon=None, clickFunction=self.advance),
      ], 
      alignment=ft.MainAxisAlignment.CENTER
    )

    self.titleRegister = ft.Row(
      controls=[
        ft.Text(value="Nuevo Usuario", size=42, color=constants.WHITE, weight=ft.FontWeight.BOLD)
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )

    self.newUserName = CustomTextField(
      label="Nombre de nuevo usuario",
      revealPassword=True,
      mode="gradient",
      hint_text=None,
      field="username",
      expand=False,
      submitFunction=self.advance
    )
    
    self.password = CustomTextField(
      label="Contraseña",
      revealPassword=True,
      mode="gradient",
      hint_text=None,
      field="password",
      expand=1,
      submitFunction=self.advance
    )
    
    self.passwordConfirmation = CustomTextField(
      label="Contraseña",
      revealPassword=False,
      mode="gradient",
      hint_text=None,
      field="password",
      expand=1,
      submitFunction=self.advance
    )
    
    self.userCI = CustomTextField(
      label="Documento de Empleado",
      revealPassword=True,
      mode="gradient",
      hint_text=None,
      field="ci",
      expand=False,
      submitFunction=self.advance
    )

    # inputs
    self.inputs = ft.Column(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      controls=[
        self.newUserName,
        self.userCI,
        ft.Row(
          controls=[
            self.password,
            self.passwordConfirmation,
          ],
        )
      ],
    )
    
    # checkbox
    self.checkbox = CustomCheckbox(label="Usuario Administrador", fill_color=constants.ORANGE, color=constants.WHITE)
    
    self.formFirst = ft.Column(
      expand=True,
      controls=[
        self.titleRegister,
        self.inputs,
        ft.Row(
          controls=[self.checkbox],
          alignment=ft.MainAxisAlignment.CENTER
        ),
        self.button,
      ],
      alignment=ft.MainAxisAlignment.CENTER,
      spacing=20,
    )

    ####################

    self.questionOne = CustomDropdown(
      label="Primera pregunta",
      options=constants.dropdownOne,
      mode="gradient"
    )
    
    self.answerOne = CustomTextField(
      label="Respuesta",
      mode="gradient",
      hint_text=None,
      revealPassword=True,
      field="others",
      expand=False,
      submitFunction=self.advance
    )
    
    self.questionTwo = CustomDropdown(
      label="Segunda pregunta",
      options=constants.dropdownTwo,
      mode="gradient"
    )
    
    self.answerTwo = CustomTextField(
      label="Respuesta",
      mode="gradient",
      hint_text=None,
      revealPassword=True,
      field="others",
      expand=False,
      submitFunction=self.advance
    )

    self.questionsInputs = ft.Column(
      expand=True,
      controls=[
        self.questionOne,
        self.answerOne,
        self.questionTwo,
        self.answerTwo
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )
    
    self.backButton = CustomReturnButton(function=self.back, color=constants.WHITE, size=30)

    self.finishButton = ft.Row(
      controls=[
        CustomFilledButton(text="Crear Usuario", size=18, bgcolor=constants.ORANGE, color=constants.BLACK, overlay=constants.ORANGE_OVERLAY, clickFunction=self.advance)
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )
    
    self.secondContent = ft.Column(
      expand=True,
      controls=[
        ft.Row(
          controls=[
            ft.Icon(
              name=ft.icons.HELP_OUTLINED,
              color=constants.WHITE,
            ),
            ft.Text(value="Preguntas de Seguridad", size=18, color=constants.WHITE),
          ],
          alignment=ft.MainAxisAlignment.CENTER,
          vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        self.questionsInputs,
        self.finishButton
      ],
      alignment=ft.MainAxisAlignment.CENTER,
      spacing=20,
    )
    
    self.formSecond = ft.Stack(
      expand=True,
      controls=[
        self.secondContent,
        ft.Container(
          content=self.backButton,
          margin=ft.margin.only(top=0, left=0),
          alignment=ft.alignment.top_left,
          width=60,
          height=60,
        )
      ]
    )
    
    self.formList = [self.formFirst, self.formSecond]
    self.currentForm = 0
    
    self.animatedContainer = CustomAnimatedContainer(
      actualContent=self.formList[self.currentForm],
      transition=ft.AnimatedSwitcherTransition.SCALE,
      duration=300,
      reverse_duration=200,
    )
    
    self.operation = CustomOperationContainer(
      operationContent=self.animatedContainer,
      mode="gradient"
    )
    
    # content
    self.content = self.operation
    
  def advance(self, e):
    isValid = True
    if self.animatedContainer.content == self.formFirst:
      isValid = evaluateForm(username=[self.newUserName], ci=[self.userCI], password=[self.password, self.passwordConfirmation])
      
      if isValid and not self.password.value == self.passwordConfirmation.value:
        isValid = False
        self.operation.actionFailed("Las contraseñas no coinciden")
        time.sleep(2)
        self.operation.restartContainer()
        return False

    else:
      isValid = evaluateForm(others=[self.questionOne, self.questionTwo, self.answerOne, self.answerTwo])
      
      if isValid:
        self.operation.actionSuccess("Nuevo usuario añadido al sistema")
        return True
    
    if not isValid:
      print("Campos no válidos")
    else:
      print("Campos Válidos")
      if self.currentForm < len(self.formList) - 1:
        self.currentForm += 1
        self.animatedContainer.setNewContent(self.formList[self.currentForm])
    
  def back(self, e):
    if self.currentForm > 0:
      self.currentForm -= 1
      self.animatedContainer.setNewContent(self.formList[self.currentForm])

class RegisterPresentation(CustomSimpleContainer):
  def __init__(self, page):
    super().__init__(height=500, width=450, gradient=False)
    self.spacing = 20
    self.page = page
    
    self.logo = ft.Image(
      src=getImagePath("logoReg-kalinaSystem.png"),
      fit="contain",
      width=180,
      height=180
    )
    
    self.title = ft.Text(
      value="Bienvenido a bordo", 
      size=42, 
      color=constants.BROWN, 
      weight=ft.FontWeight.BOLD,
      text_align=ft.TextAlign.CENTER
    )
    
    self.description = ft.Text(
      value="Regístrate y disfruta de una experiencia personalizada. Nos alegra tenerte aquí",
      color=constants.BLACK, 
      size=18,
      weight=ft.FontWeight.BOLD,
      text_align=ft.TextAlign.CENTER
    )
    
    self.button = CustomFilledButton(
      text="¿Ya tienes un usuario?",
      bgcolor=constants.BROWN,
      color=constants.WHITE, size=18,
      overlay=constants.BROWN_OVERLAY,
      clickFunction=lambda e: showLogin(self.page)
    )
    
    self.login = ft.Row(
      controls=[
        self.button
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )
    
    self.content = ft.Column(
      controls=[
        self.title,
        self.logo,
        self.login,
        self.description
      ],
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
class Register(ft.Row):
  def __init__(self, page):
    super().__init__()
    self.page = page
    self.spacing = 0
    
    self.controls = [
      RegisterForm(self.page),
      RegisterPresentation(self.page),
    ]