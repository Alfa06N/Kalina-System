import flet as ft
import constants

class Home(ft.Row):
  def __init__(self, page):
    super().__init__()
    self.expand = True
    self.alignment = ft.MainAxisAlignment.CENTER
    self.vertical_alignment = ft.CrossAxisAlignment.CENTER
    self.page = page
    self.controls = [
      ft.Text(
        value="There's nothing to show you",
        size=42,
        color=constants.BLACK,
        weight=ft.FontWeight.BOLD,
      )
    ]