import flet as ft
import constants 
import time
from validation import validateCI, validateEmptyField, validatePassword, validateUsername

class CustomPrincipalContainer(ft.Container):
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
    
class CustomSimpleContainer(ft.Container):
  def __init__(self, height, width, gradient):
    super().__init__()
    self.height = height
    self.width = width
    self.border_radius = ft.border_radius.all(30)
    self.padding = ft.padding.symmetric(horizontal=30, vertical=40)
    self.bgcolor = constants.WHITE
    self.alignment = ft.alignment.center
    
    if gradient:
      self.gradient = ft.LinearGradient(
        begin=ft.alignment.top_center,
        end=ft.alignment.bottom_center,
        colors=[constants.BROWN, constants.BLACK]
      )

class CustomOperationContainer(ft.Container):
  def __init__(self, operationContent, mode):
    super().__init__()
    self.originalHeight = operationContent.height
    self.height = self.originalHeight
    self.originalWidth = operationContent.width
    self.width = self.originalWidth
    self.padding = 0
    self.border_radius = ft.border_radius.all(0)
    self.mode = mode
    
    self.operationContent = operationContent
    
    self.animate = ft.animation.Animation(
      duration=800, 
      curve=ft.AnimationCurve.ELASTIC_OUT
    )
    
    self.content = operationContent
    
  def actionSuccess(self, message):
    self.padding = ft.padding.symmetric(horizontal=30, vertical=20)
    self.border_radius = ft.border_radius.all(30)
    self.height = 100
    self.width = 400
    self.alignment = ft.alignment.center_left
    
    if (self.mode == "gradient"):
      self.border = ft.border.all(4, constants.ORANGE_LIGHT)
      self.content = ft.Row(
        controls=[
          ft.Container(
            border_radius=ft.border_radius.all(10),
            border=ft.border.all(2, constants.WHITE),
            height=50,
            width=50,
            bgcolor=ft.colors.TRANSPARENT,
            content=ft.Icon(
              name=ft.icons.CHECK_CIRCLE_SHARP,
              color=constants.ORANGE_LIGHT,
            ),
            alignment=ft.alignment.center,
          ),
          ft.Text(value=message, size=18, color=constants.WHITE),
        ]
      )
      
    elif (self.mode == "light"):
      self.gradient = ft.LinearGradient(
        begin=ft.alignment.center_left,
        end=ft.alignment.center,
        colors=[constants.GREEN_SUCCESS, constants.WHITE],
      )
      self.border = ft.border.all(4, constants.BLACK)
      self.content = ft.Row(
        controls=[
          ft.Container(
            border_radius=ft.border_radius.all(10),
            border=ft.border.all(1, constants.WHITE_GRAY),
            height=50,
            width=50,
            bgcolor=constants.WHITE,
            content=ft.Icon(
              name=ft.icons.CHECK_CIRCLE_SHARP,
              color=ft.colors.GREEN,
            ),
            alignment=ft.alignment.center,
          ),
          ft.Text(value=message, size=18, color=constants.BLACK),
        ]
      )
    self.update()
  
  def actionFailed(self, message):
    self.padding = ft.padding.symmetric(horizontal=30, vertical=20)
    self.border_radius = ft.border_radius.all(30)
    self.height = 100
    self.width = 400
    self.alignment = ft.alignment.center_left
    
    if (self.mode == "gradient"):
      self.border = ft.border.all(4, constants.RED_FAILED_LIGHT)
      self.content = ft.Row(
        controls=[
          ft.Container(
            border_radius=ft.border_radius.all(10),
            border=ft.border.all(2, constants.WHITE),
            height=50,
            width=50,
            bgcolor=ft.colors.TRANSPARENT,
            content=ft.Icon(
              name=ft.icons.ERROR_OUTLINE_SHARP,
              color=constants.RED_FAILED_LIGHT,
            ),
            alignment=ft.alignment.center,
          ),
          ft.Text(value=message, size=18, color=constants.WHITE),
        ]
      )
      
    elif (self.mode == "light"):
      self.gradient = ft.LinearGradient(
        begin=ft.alignment.center_left,
        end=ft.alignment.center,
        colors=[constants.RED_FAILED, constants.WHITE],
      )
      self.border = ft.border.all(4, constants.BLACK)
      self.content = ft.Row(
        controls=[
          ft.Container(
            border_radius=ft.border_radius.all(10),
            border=ft.border.all(1, constants.WHITE_GRAY),
            height=50,
            width=50,
            bgcolor=constants.WHITE,
            content=ft.Icon(
              name=ft.icons.ERROR_OUTLINE_SHARP,
              color=constants.RED_FAILED,
            ),
            alignment=ft.alignment.center,
          ),
          ft.Text(value=message, size=18, color=constants.BLACK),
        ]
      )
    self.update()   
  
  def restartContainer(self):
    self.border_radius = ft.border_radius.all(0)
    self.gradient = None
    self.alignment = ft.alignment.center
    self.border = None
    self.content = self.operationContent
    self.height = self.originalHeight
    self.width = self.originalWidth
    self.padding = 0
    self.update()
  
  def setNewOperation(self, newContent):
    self.operationContent = newContent
    self.restartContainer()
  
class CustomAnimatedContainer(ft.AnimatedSwitcher):
  def __init__(self, actualContent, transition, duration, reverse_duration):
    super().__init__(content=actualContent)
    self.height = actualContent.height
    self.width = actualContent.width
    self.transition = transition
    self.duration = duration
    self.reverse_duration = reverse_duration
  
  def setNewContent(self, newContent):
    self.content = newContent
    self.update()

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
    
class CustomTextField(ft.TextField):
  def __init__(self, label, revealPassword, mode, hint_text, field, expand, submitFunction):
    super().__init__()
    self.label = label
    self.border_width = 2
    self.expand = expand
    self.on_submit = submitFunction
    
    if mode == "gradient":
      self.border_color = constants.WHITE_GRAY
      self.focused_border_color = constants.ORANGE_LIGHT
      self.label_style=ft.TextStyle(
        color=constants.ORANGE_LIGHT
      )
    
    if field == "username":
      self.on_change = lambda e: validateUsername(self)
      
    elif field == "password":
      self.password = True
      self.can_reveal_password = revealPassword
      self.on_change = lambda e: validatePassword(self)
    
    elif field == "ci":
      self.input_filter=ft.NumbersOnlyInputFilter()
      self.on_change = lambda e: validateCI(self)
    
    elif field == "others":
      self.on_change = lambda e: validateEmptyField(self)

class CustomDropdown(ft.Dropdown):
  def __init__(self, label, options, mode):
    super().__init__()
    self.label = label
    self.options = options
    self.border_width = 2
    
    if mode == "gradient":
      self.border_color=constants.WHITE_GRAY
      self.focused_border_color=constants.ORANGE_LIGHT
      self.label_style=ft.TextStyle(
        color=constants.ORANGE_LIGHT
      )
    
    self.on_change = lambda e: validateEmptyField(self)