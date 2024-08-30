import flet as ft
import constants

class Closings(ft.Row):
  def __init__(self, page):
    super().__init__()
    self.page = page
    self.expand = True
    self.alignment = ft.MainAxisAlignment.CENTER
    self.vertical_alignment = ft.CrossAxisAlignment.CENTER
    
    self.controls = [
      ft.Text(
        value="There's nothing to show you here in Closings",
        size=42,
        color=constants.BLACK,
        weight=ft.FontWeight.BOLD,
      )
    ]