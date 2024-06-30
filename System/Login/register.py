import flet as ft 
from .customControls import CustomContainer, CustomFilledButton, CustomOutlinedButton

class RegisterForm(ft.Container):
  def __init__(self):
    super().__init__()
    self.height = 500
    self.width = 400
    self.border_radius = ft.border_radius.all(30)
    self.padding = ft.padding.symmetric(horizontal=30, vertical=20)
    self.gradient=ft.LinearGradient(
      begin=ft.alignment.center_left,
      end=ft.alignment.center_right,
      colors=["#222222", "#36240c"]
    )
    
    self.nextButton = ft.Row(
      controls=[
        CustomFilledButton(text="Siguiente", bgcolor="#E19E45", size=18, color="#222222", overlay="#e6b363")
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )

    self.titleRegister = ft.Row(
      controls=[
        ft.Text(value="Nuevo Usuario", size=42, color="#e0e0e0", weight=ft.FontWeight.BOLD)
      ],
      alignment=ft.MainAxisAlignment.CENTER
    )

    self.newUserName = ft.TextField(label="Nombre de Nuevo Usuario", border_color="e0e0e0", border_width=2)
    self.password = ft.TextField(label="Contraseña", border_color="e0e0e0", border_width=2, password=True, can_reveal_password=True)
    self.passwordConfirmation = ft.TextField(label="Confirmar Contraseña", border_color="e0e0e0", border_width=2, password=True, can_reveal_password=True)
    self.adminPassword = ft.TextField(label="Autorización de Administrador", border_color="e0e0e0", border_width=2, password=True, hint_text="Contraseña")

    # inputs
    self.inputs = ft.Column(
      controls=[
        self.newUserName,
        self.password,
        self.passwordConfirmation,
        self.adminPassword,
      ],
    )

    # radios
    self.radios = ft.RadioGroup(
      content=ft.Row(
        controls=[
          ft.Radio(value="Administrador", label="Administrador", fill_color="#E19E45"),
          ft.Radio(value="Colaborador", label="Colaborador", fill_color="#E19E45")
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

    self.questionOne = ft.TextField(label="Primera Pregunta", border_color="e0e0e0", border_width=2, hint_text='"Comida favorita"')
    self.answerOne = ft.TextField(label="Respuesta", border_color="e0e0e0", border_width=2)
    self.questionTwo = ft.TextField(label="Segunda Pregunta", border_color="e0e0e0", border_width=2, hint_text='"Nombre de mi primera mascota"')
    self.answerTwo = ft.TextField(label="Respuesta", border_color="e0e0e0", border_width=2)

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
        CustomFilledButton(text="Crear Usuario", size=18, bgcolor="#E19E45", color="#222222", overlay="#e6b363")
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
    )

    # content
    self.content = self.formSecond

class RegisterPresentation(ft.Container):
  pass