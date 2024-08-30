import flet as ft
import constants

class Inventory(ft.Row):
  def __init__(self, page):
    super().__init__()
    self.expand = True
    self.page = page
    self.alignment = ft.MainAxisAlignment.CENTER
    self.vertical_alignment = ft.CrossAxisAlignment.CENTER
    
    self.controls = [
      ft.Text(
        value="There's nothing to show you in Inventory",
        size=42,
        color=constants.BLACK,
        weight=ft.FontWeight.BOLD,
      )
    ]