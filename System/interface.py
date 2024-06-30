import flet as ft 
from Login.login import Login

def showLogin(page: ft.Page):
  login = Login()

  footer = ft.Row(
    height = 50,
    controls=[
      ft.Text("© 2024 Kariña System. Todos los derechos reservados.", color="#222222")
    ],
    alignment=ft.MainAxisAlignment.CENTER
  )

  page.add(
    ft.Row(height=50),
    login,
    footer
  )