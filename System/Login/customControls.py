import flet as ft
import constants 

class CustomContainer(ft.Container):
  def __init__(self, width=900, height=500):
    super().__init__()
    self.width = width
    self.height = height
    self.border_radius = ft.border_radius.all(30)
    self.bgcolor = constants.WHITE
    self.shadow = ft.BoxShadow(
      spread_radius = 1,
      blur_radius = 20,
      color = "#444444"
    ) 

class CustomGradientContainer(ft.Container):
  def __init__(self):
    super().__init__()
    self.width = 450
    self.height = 500
    self.border_radius = ft.border_radius.all(30)
    self.padding = ft.padding.symmetric(horizontal=30, vertical=20)
    self.gradient=ft.LinearGradient(
      begin=ft.alignment.center_left,
      end=ft.alignment.center_right,
      colors=[constants.BROWN, constants.BLACK]
    )

class CustomWhiteContainer(ft.Container):
  def __init__(self):
    super().__init__()
    self.width = 450
    self.height = 500
    self.border_radius = ft.border_radius.all(30)
    self.padding = ft.padding.symmetric(horizontal=30, vertical=20)
    self.bgcolor = constants.WHITE

class CustomFilledButton(ft.FilledButton):
  def __init__(self, text, overlay, bgcolor, color, size):
    super().__init__()
    self.text = text
    self.size = size
    self.color = color
    self.bgcolor = bgcolor
    self.overlay = overlay
    self.elevation = 8

    self.content = ft.Text(
      value=self.text,
      size=self.size,
      weight=ft.FontWeight.BOLD
    )

    self.style=ft.ButtonStyle(
      shape=ft.RoundedRectangleBorder(radius=10),
      bgcolor={
        ft.ControlState.DEFAULT: self.bgcolor,
        ft.ControlState.HOVERED: self.bgcolor,
        ft.ControlState.FOCUSED: self.overlay,
        ft.ControlState.PRESSED: self.bgcolor
      },
      color=self.color,
      overlay_color={
        ft.ControlState.HOVERED: self.overlay,
        ft.ControlState.PRESSED: self.bgcolor,
        ft.ControlState.FOCUSED: None,
        ft.ControlState.DEFAULT: None,
      },
      elevation={ft.ControlState.DEFAULT: 5, 
      ft.ControlState.SELECTED: 0,},
      padding=ft.padding.symmetric(horizontal=50, vertical=20),
      animation_duration=2000,
    )

class CustomOutlinedButton(ft.OutlinedButton):
  def __init__(self, text, color, size, icon):
    super().__init__()
    self.text = text
    self.color = color
    self.size = size
    self.icon = icon

    self.content = ft.Text(
      value=self.text, 
      size=self.size, 
      color=self.color, 
      weight=ft.FontWeight.BOLD
    )

    self.icon = self.icon

    self.style = ft.ButtonStyle(
      shape=ft.RoundedRectangleBorder(radius=10),
      padding=ft.padding.symmetric(horizontal=50, vertical=20),
      animation_duration=2000,
      bgcolor={
        ft.ControlState.DEFAULT: ft.colors.TRANSPARENT
      },
      color=self.color
    )

