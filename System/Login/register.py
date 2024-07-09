import flet as ft 
from Login.customControls import CustomContainer, CustomFilledButton, CustomOutlinedButton, CustomGradientContainer, CustomWhiteContainer
import constants

class RegisterForm(CustomGradientContainer):
  def __init__(self):
    super().__init__(height=500, width=450)
    
    self.nextButton = ft.Row(
      controls=[
        CustomFilledButton(text="Siguiente", bgcolor=constants.ORANGE, size=18, color=constants.BLACK, overlay=constants.ORANGE_OVERLAY, clickFunction=None)
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )

    self.titleRegister = ft.Row(
      controls=[
        ft.Text(value="Nuevo Usuario", size=42, color=constants.WHITE, weight=ft.FontWeight.BOLD)
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )

    self.newUserName = ft.TextField(label="Nombre de Nuevo Usuario", border_color=constants.WHITE_GRAY, border_width=2, focused_border_color=constants.ORANGE_LIGHT, label_style=ft.TextStyle(
      color=constants.ORANGE_LIGHT
    ))
    self.password = ft.TextField(label="Contraseña", border_color=constants.WHITE_GRAY, border_width=2, password=True, can_reveal_password=True, focused_border_color=constants.ORANGE_LIGHT, label_style=ft.TextStyle(
      color=constants.ORANGE_LIGHT
    ))
    self.passwordConfirmation = ft.TextField(label="Confirmar Contraseña", border_color=constants.WHITE_GRAY, border_width=2, password=True, can_reveal_password=True, focused_border_color=constants.ORANGE_LIGHT, label_style=ft.TextStyle(
      color=constants.ORANGE_LIGHT
    ))
    self.userCI = ft.TextField(label="Documento de Empleado", border_color=constants.WHITE_GRAY, border_width=2, focused_border_color=constants.ORANGE_LIGHT, label_style=ft.TextStyle(
      color=constants.ORANGE_LIGHT
    ))

    # inputs
    self.inputs = ft.Column(
      controls=[
        self.newUserName,
        self.userCI,
        self.password,
        self.passwordConfirmation,
      ],
    )

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
        self.radios,
        self.nextButton
      ],
      alignment=ft.MainAxisAlignment.CENTER,
      spacing=20,
    )

    ####################

    self.questionOne = ft.TextField(label="Primera Pregunta", border_color=constants.WHITE_GRAY, border_width=2, hint_text='"Comida favorita"', focused_border_color=constants.ORANGE_LIGHT, label_style=ft.TextStyle(
      color=constants.ORANGE_LIGHT
    ))
    self.answerOne = ft.TextField(label="Respuesta", border_color=constants.WHITE_GRAY, border_width=2, focused_border_color=constants.ORANGE_LIGHT, label_style=ft.TextStyle(
      color=constants.ORANGE_LIGHT
    ))
    self.questionTwo = ft.TextField(label="Segunda Pregunta", border_color=constants.WHITE_GRAY, border_width=2, hint_text='"Nombre de mi primera mascota"', focused_border_color=constants.ORANGE_LIGHT, label_style=ft.TextStyle(
      color=constants.ORANGE_LIGHT
    ))
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

    self.finishButton = ft.Row(
      controls=[
        CustomFilledButton(text="Crear Usuario", size=18, bgcolor=constants.ORANGE, color=constants.BLACK, overlay=constants.ORANGE_OVERLAY, clickFunction=None)
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )

    # formSecond
    self.formSecond = ft.Column(
      controls=[
        self.questionsTitle,
        self.questionsInputs,
        self.finishButton
      ],
      alignment=ft.MainAxisAlignment.CENTER,
      spacing=20,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # content
    self.content = self.formFirst

class RegisterPresentation(CustomWhiteContainer):
  def __init__(self):
    super().__init__(height=500, width=450)
    self.spacing = 10
    
    self.logo = ft.Image(
      src="../images/logoCDC-kalinaSystem.png",
      fit="contain",
      width=240,
      height=240
    )
    
    self.title = ft.Text(
      value="Bienvenido a bordo", 
      size=42, 
      color=constants.BROWN, 
      weight=ft.FontWeight.BOLD,
    )
    
    self.description = ft.Text(
      value="Regístrate y comienza a disfrutar de una experiencia personalizada. Nos alegra tenerte aquí"
    )
    
    self.button = CustomFilledButton(
      text="¿Ya tienes un usuario?",
      bgcolor=constants.BROWN,
      color=constants.WHITE, size=18,
      overlay=constants.BROWN_OVERLAY,
      clickFunction=None
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
      ]
    )
    
class Register(CustomContainer):
  def __init__(self):
    super().__init__(width=900, height=500)
    self.content = ft.Row(
      controls=[
        RegisterForm(),
        RegisterPresentation(),
      ]
    )