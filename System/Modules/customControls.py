import flet as ft
import constants 

class CustomContainer(ft.Container):
  def __init__(self, width, height, containerContent):
    super().__init__()
    self.width = width
    self.height = height
    self.border_radius = ft.border_radius.all(30)
    self.bgcolor = constants.WHITE
    self.animatedContainer = ft.AnimatedSwitcher(
      content=containerContent,
      transition=ft.AnimatedSwitcherTransition.FADE,
      duration=400,
      reverse_duration=200,
    )
    self.content = self.animatedContainer
    self.shadow = ft.BoxShadow(
      spread_radius = 1,
      blur_radius = 20,
      color = "#444444"
    ) 
  def updateContent(self, newContent):
    self.animatedContainer.content = newContent
    self.animatedContainer.update()

class CustomGradientContainer(ft.Container):
  def __init__(self, height, width):
    super().__init__()
    self.width = width
    self.height = height
    self.border_radius = ft.border_radius.all(30)
    self.padding = ft.padding.symmetric(horizontal=30, vertical=20)
    self.gradient=ft.LinearGradient(
      begin=ft.alignment.top_center,
      end=ft.alignment.bottom_center,
      colors=[constants.BROWN, constants.BLACK]
    )

class CustomWhiteContainer(ft.Container):
  def __init__(self, height, width):
    super().__init__()
    self.width = width
    self.height = height
    self.border_radius = ft.border_radius.all(30)
    self.padding = ft.padding.symmetric(horizontal=30, vertical=20)
    self.bgcolor = constants.WHITE

class CustomFilledButton(ft.FilledButton):
  def __init__(self, text, overlay, bgcolor, color, size, clickFunction):
    super().__init__()
    self.text = text
    self.size = size
    self.color = color
    self.bgcolor = bgcolor
    self.overlay = overlay
    self.elevation = 8
    self.clickFunction = clickFunction

    self.content = ft.Text(
      value=self.text,
      size=self.size,
      weight=ft.FontWeight.BOLD
    )
    
    # Evento Click
    self.on_click = self.clickFunction

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
  def __init__(self, text, color, size, icon, clickFunction):
    super().__init__()
    self.text = text
    self.color = color
    self.size = size
    self.icon = icon
    self.on_click = clickFunction

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
      animation_duration=1000,
      bgcolor={
        ft.ControlState.DEFAULT: ft.colors.TRANSPARENT
      },
      color=self.color,
      side=ft.BorderSide(
        width=2,
        color=self.color
      )
    )
    
class CustomReturnButton(ft.OutlinedButton):
  def __init__(self, function, color, size):
    super().__init__()
    self.on_click = function
    self.color = color
    self.size = size
    
    self.content = ft.Icon(
      name=ft.icons.ARROW_BACK,
      color=self.color,
      size=self.size,
    )
    
    self.style = ft.ButtonStyle(
      color=self.color,
      padding=0,
      side=ft.BorderSide(
        width=2,
        color=self.color
      ),
      # overlay_color={
      #   ft.ControlState.HOVERED: None,
      #   ft.ControlState.FOCUSED: None,
      # }
    )
    
class CustomCheckbox(ft.Checkbox):
  def __init__(self, label, color, fill_color):
    super().__init__()
    self.label = label
    self.color = color
    self.label_style = ft.TextStyle(
      color=self.color,
      size=18,
    )
    self.active_color = fill_color
    
class CustomDialog(ft.AlertDialog):
  def __init__(self, title, description):
    super().__init__()
    self.title = ft.Text(title)
    self.content = ft.Text(description)
    self.shadow_color = constants.BLACK