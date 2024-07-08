import flet as ft 
from Login.login import Login

def showLogin(page: ft.Page):
  login = Login()

  footer = ft.Row(
    height = 60,
    controls=[
      ft.Text("© 2024 Kariña System. Todos los derechos reservados.", color="#222222", size=16)
    ],
    alignment=ft.MainAxisAlignment.CENTER
  )

  page.add(
    ft.Row(height=60),
    login,
    footer
  )