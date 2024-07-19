import flet as ft 
from Modules.customControls import CustomFilledButton, CustomOutlinedButton, CustomCheckbox, CustomReturnButton, CustomSimpleContainer
from validation import evaluateForm, validateUsername, validatePassword, validateCI
import constants
from interface import showLogin

class RegisterForm(CustomSimpleContainer):
  def __init__(self, page):
    super().__init__(height=500, width=450, gradient=True)
    self.page = page
    
    self.nextButton = ft.Row(
      controls=[
        CustomFilledButton(text="Siguiente", bgcolor=constants.ORANGE, size=18, color=constants.BLACK, overlay=constants.ORANGE_OVERLAY, clickFunction=self.advance)
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )
    
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

    self.newUserName = ft.TextField(label="Nombre de Nuevo Usuario", border_color=constants.WHITE_GRAY, border_width=2, on_change=lambda e: validateUsername(self.newUserName), focused_border_color=constants.ORANGE_LIGHT, label_style=ft.TextStyle(
      color=constants.ORANGE_LIGHT
    ))
    self.password = ft.TextField(label="Contraseña", border_color=constants.WHITE_GRAY, border_width=2, password=True, expand=1, can_reveal_password=True, on_change=lambda e: validatePassword(self.password), focused_border_color=constants.ORANGE_LIGHT, label_style=ft.TextStyle(
      color=constants.ORANGE_LIGHT
    ))
    self.passwordConfirmation = ft.TextField(label="Confirmar Contraseña", border_color=constants.WHITE_GRAY, border_width=2, password=True, expand=1, on_change=lambda e: validatePassword(self.passwordConfirmation), can_reveal_password=False, focused_border_color=constants.ORANGE_LIGHT, label_style=ft.TextStyle(
      color=constants.ORANGE_LIGHT
    ))
    self.userCI = ft.TextField(label="Documento de Empleado", border_color=constants.WHITE_GRAY, border_width=2, on_change=lambda e: validateCI(self.userCI), input_filter=ft.NumbersOnlyInputFilter(), focused_border_color=constants.ORANGE_LIGHT, label_style=ft.TextStyle(
      color=constants.ORANGE_LIGHT
    ))

    # inputs
    self.inputs = ft.Column(
      controls=[
        self.newUserName,
        self.userCI,
        ft.Row(
          controls=[
            self.password,
            self.passwordConfirmation,
          ]
        )
      ],
    )
    
    # checkbox
    self.checkbox = CustomCheckbox(label="Usuario Administrador", fill_color=constants.ORANGE, color=constants.WHITE)

    # radios
    self.radios = ft.RadioGroup(
      content=ft.Row(
        controls=[
          ft.Radio(value="Administrador", label="Administrador", fill_color=constants.ORANGE),
          ft.Radio(value="Colaborador", label="Colaborador", fill_color=constants.ORANGE)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
      )
    )
    
    self.formFirst = ft.Column(
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

    self.questionOne = ft.Dropdown(
      label="Primera Pregunta",
      options=constants.dropdownOne,
      border_color=constants.WHITE_GRAY, border_width=2,
      focused_border_color=constants.ORANGE_LIGHT,
      label_style=ft.TextStyle(
        color=constants.ORANGE_LIGHT
      )
    )
    self.answerOne = ft.TextField(label="Respuesta", border_color=constants.WHITE_GRAY, border_width=2, focused_border_color=constants.ORANGE_LIGHT, label_style=ft.TextStyle(
      color=constants.ORANGE_LIGHT
    ))
    self.questionTwo = ft.Dropdown(
      label="Segunda Pregunta",
      options=constants.dropdownTwo,
      border_color=constants.WHITE_GRAY, border_width=2,
      focused_border_color=constants.ORANGE_LIGHT,
      label_style=ft.TextStyle(
        color=constants.ORANGE_LIGHT
      )
    )
    self.answerTwo = ft.TextField(label="Respuesta", border_color=constants.WHITE_GRAY, border_width=2, focused_border_color=constants.ORANGE_LIGHT, label_style=ft.TextStyle(
      color=constants.ORANGE_LIGHT
    ))

    self.questionsInputs = ft.Column(
      controls=[
        self.questionOne,
        self.answerOne,
        self.questionTwo,
        self.answerTwo
      ]
    )

    self.questionsTitle = ft.Row(
      controls=[
        ft.Text(value="Preguntas de Seguridad", size=42, color="e0e0e0", weight=ft.FontWeight.BOLD, width=350, text_align=ft.TextAlign.CENTER)
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )
    
    self.backButton = CustomReturnButton(function=self.back, color=constants.WHITE, size=30)

    self.finishButton = ft.Row(
      controls=[
        CustomFilledButton(text="Crear Usuario", size=18, bgcolor=constants.ORANGE, color=constants.BLACK, overlay=constants.ORANGE_OVERLAY, clickFunction=None)
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )
    
    self.secondContent = ft.Column(
      controls=[
        self.questionsTitle,
        self.questionsInputs,
        self.finishButton
      ],
      alignment=ft.MainAxisAlignment.CENTER,
      spacing=20,
    )
    
    self.formSecond = ft.Stack(
      controls=[
        self.secondContent,
        ft.Container(
          content=self.backButton,
          margin=ft.margin.only(top=90, left=0),
          alignment=ft.alignment.top_left,
          width=60,
          height=60,
        )
      ]
    )
    
    self.formList = [self.formFirst, self.formSecond]
    self.currentForm = 0
    
    self.animatedContainer = ft.AnimatedSwitcher(
      content=self.formList[self.currentForm],
      transition=ft.AnimatedSwitcherTransition.SCALE,
      duration=300,
      reverse_duration=200,
      # switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
      # switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
    )
    
    # content
    self.content = self.animatedContainer
    
  def advance(self, e):
    isValid = True
    if self.animatedContainer.content == self.formFirst:
      isValid = evaluateForm(username=[self.newUserName], ci=[self.userCI], password=[self.password, self.passwordConfirmation])
      
      if not self.password.value == self.passwordConfirmation.value:
        # self.page.open(CustomDialog(title="Las contraseñas no coinciden", description="Asegúrese de ingresar los datos correctos en cada campo"))
        self.page.open(ft.AlertDialog(
          title=ft.Text("Las contraseñas no coinciden", color=constants.BLACK),
          content=ft.Text("Asegurese de ingresar los datos correctos en cada campo", color=constants.BLACK),
          bgcolor=constants.WHITE,
        ))
        return False
    
    if not isValid:
      print("Campos no válidos")
    else:
      print("Campos Válidos")
      if self.currentForm < len(self.formList) - 1:
        self.currentForm += 1
        self.updateForm()
    
  def back(self, e):
    if self.currentForm > 0:
      self.currentForm -= 1
      self.updateForm()
  
  def updateForm(self):
    self.animatedContainer.content = self.formList[self.currentForm]
    self.update()

class RegisterPresentation(CustomSimpleContainer):
  def __init__(self, page):
    super().__init__(height=500, width=450, gradient=False)
    self.spacing = 20
    self.page = page
    
    self.logo = ft.Image(
      src="../images/logoReg-kalinaSystem.png",
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