import flet as ft
import constants

class Sales(ft.Row):
  def __init__(self):
    super().__init__()
    self.expand = True
    self.alignment = ft.MainAxisAlignment.CENTER
    self.vertical_alignment = ft.CrossAxisAlignment.CENTER
    
    self.controls = [
      ft.Text(
        value="There's nothing to show you in Sales",
        size=42,
        color=constants.BLACK,
        weight=ft.FontWeight.BOLD,
      )
    ]