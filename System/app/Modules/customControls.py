import flet as ft
import constants 
import time
from validation import validateCI, validateEmptyField, validatePassword, validateUsername, validateNumber, evaluateForm
from utils.imageManager import ImageManager
from datetime import datetime
import os
import re
from config import getDB
import threading
from exceptions import InvalidData
from DataBase.crud.product import calculatePrice, getProducts, getProductByName
from DataBase.crud.combo import calculateComboCost, getCombos
from utils.exchangeManager import exchangeRateManager
from DataBase.crud.product_combo import getRegisterByComboId
from DataBase.crud.product_combo import getRegisterByComboId
from DataBase.models import Product, Combo
from DataBase.crud.product import getProductById
from DataBase.crud.combo import getComboById
from utils.inventoryManager import inventoryManager
from utils.sessionManager import verifyPermission

class CustomPrincipalContainer(ft.Container):
  def __init__(self, containerContent, width=900, height=550):
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
      blur_radius = 5,
      color = constants.BLACK_INK
    ) 
      
  def updateContent(self, newContent):
    self.animatedContainer.content = newContent
    self.animatedContainer.update()
    
class CustomSimpleContainer(ft.Container):
  def __init__(self, gradient=False, height=550, width=450, expand=False):
    super().__init__()
    self.height = height
    self.width = width
    self.expand = expand
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
  def __init__(self, operationContent, mode="light"):
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
      duration=300, 
      curve=ft.AnimationCurve.EASE_IN_OUT
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
              name=ft.Icons.CHECK_CIRCLE_SHARP,
              color=constants.ORANGE_LIGHT,
            ),
            alignment=ft.alignment.center,
          ),
          ft.Container(
            content=ft.Text(value=message, size=20, color=constants.WHITE, overflow=ft.TextOverflow.ELLIPSIS),
          )
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
              name=ft.Icons.CHECK_CIRCLE_SHARP,
              color=ft.colors.GREEN,
            ),
            alignment=ft.alignment.center,
          ),
          ft.Container(
            content=ft.Text(value=message, size=20, color=constants.BLACK, overflow=ft.TextOverflow.ELLIPSIS),
          )
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
              name=ft.Icons.ERROR_OUTLINE_SHARP,
              color=constants.RED_FAILED_LIGHT,
            ),
            alignment=ft.alignment.center,
          ),
          ft.Container(
            content=ft.Text(value=message, size=20, color=constants.WHITE, overflow=ft.TextOverflow.ELLIPSIS),
          ),
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
              name=ft.Icons.ERROR_OUTLINE_SHARP,
              color=constants.RED_FAILED,
            ),
            alignment=ft.alignment.center,
          ),
          ft.Container(
            content=ft.Text(value=message, size=20, color=constants.BLACK, overflow=ft.TextOverflow.ELLIPSIS),
          ),
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
  def __init__(self, actualContent, transition=ft.AnimatedSwitcherTransition.FADE, duration=400, reverse_duration=200):
    super().__init__(content=actualContent)
    self.height = self.content.height if self.content.height else "auto"
    self.width = self.content.width if self.content.width else "auto"
    self.transition = transition
    self.duration = duration
    self.reverse_duration = reverse_duration
  
  def setNewContent(self, newContent):
    self.content = newContent
    self.update()

class CustomAnimatedContainerSwitcher(ft.Container):
  def __init__(self, content, height=150, width=300, padding=ft.padding.all(20), margin=ft.margin.all(20), border_radius=ft.border_radius.all(30), bgcolor=constants.WHITE, shadow=None, alignment=ft.alignment.center, expand=False, duration:int=300, animationCurve=ft.AnimationCurve.EASE_IN_OUT, col=None):
    super().__init__(col=col)
    self.height = height
    self.width = width
    self.shadow = shadow
    self.duration = duration
    self.animationCurve = animationCurve
    self.bgcolor = bgcolor
    self.margin = margin
    self.border_radius = border_radius
    self.padding = padding
    self.alignment = alignment
    self.expand = expand
    
    self.animate = ft.animation.Animation(self.duration, self.animationCurve)
    
    self.content = ft.AnimatedSwitcher(
      content=content,
      transition=ft.AnimatedSwitcherTransition.FADE,
      duration=400,
      reverse_duration=200,
    )
    
  def setNewContent(self, newContent):
    self.content.content = newContent
    self.content.update()
    
  def changeStyle(self, height=None, width=None, shadow=None, bgcolor=constants.WHITE):
    if height:
      self.height = height
    if width:
      self.width = width
    self.shadow = shadow
    self.bgcolor = bgcolor
    self.update()
  

class CustomFilledButton(ft.FilledButton):
  def __init__(self, text, overlay=constants.BROWN_OVERLAY, bgcolor=constants.BROWN, color=constants.WHITE, size=20, clickFunction=None):
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
      weight=ft.FontWeight.W_700,
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

class CustomFloatingActionButton(ft.FloatingActionButton):
  def __init__(self, icon=ft.Icons.ADD, height:int=70, width:int=70, bgcolor=constants.BROWN, color=constants.WHITE, on_click=None):
    super().__init__()
    self.height = height
    self.width = width
    self.bgcolor = bgcolor
    self.color = constants.WHITE
    self.on_click = on_click
    
    self.content = ft.Icon(
      name=icon, 
      size=24, 
      color=self.color
    )

class CustomOutlinedButton(ft.OutlinedButton):
  def __init__(self, text, color=constants.BLACK, size=20, icon=None, clickFunction=None):
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
  def __init__(self, function, size=32, color=constants.BLACK):
    super().__init__()
    self.on_click = function
    self.color = color
    self.size = size
    
    self.content = ft.Icon(
      name=ft.Icons.ARROW_BACK,
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
      size=20,
    )
    self.active_color = fill_color
    
class CustomTextField(ft.TextField):
  def __init__(self, label, field, revealPassword=False,  mode="light",  hint_text=None, on_changeFunction=None, expand=False, submitFunction=None, value="", suffix_text=None, disabled:bool=False):
    super().__init__()
    self.label = label
    self.border_width = 2
    self.expand = expand
    self.on_submit = submitFunction
    self.disabled = disabled
    self.hint_text = hint_text
    self.suffix_text = suffix_text
    self.value = value
    self.on_changeFunction = on_changeFunction
    self.field = field
    self.text_size = 18
    
    if mode == "gradient":
      self.color = constants.WHITE
      self.border_color = constants.WHITE_GRAY
      self.focused_border_color = constants.ORANGE_LIGHT
      self.label_style=ft.TextStyle(
        color=constants.ORANGE_LIGHT
      )
      self.cursor_color = constants.WHITE
    else:
      self.color = constants.BLACK
      self.border_color = constants.BLACK_GRAY
      self.focused_border_color = constants.BLACK
      self.label_style = ft.TextStyle(
        color=constants.BLACK
      )
      self.cursor_color = constants.BLACK
      
    if self.field == "password":
      self.password = True
      self.can_reveal_password = revealPassword
      
    elif self.field == "number":
      self.text_align = ft.TextAlign.RIGHT
      self.keyboard_type = ft.KeyboardType.NUMBER
      self.value = "0.00" if self.value == "" else self.value
      self.on_blur = self.onBlurNumbers
    
    elif self.field == "ci":
      self.prefix_text = "V-"
      self.input_filter=ft.NumbersOnlyInputFilter()
      
    self.on_change = lambda e: self.functionOnChange()
  
  def onBlurNumbers(self, e):
    if self.value == "":
      self.value = "0"
      self.update()
  
  def functionOnChange(self):
    try:
      if self.on_changeFunction:
        self.on_changeFunction()
        
      if self.field == "username":
        validateUsername(self)
      
      elif self.field == "password":
        validatePassword(self)
      
      elif self.field == "number":
        validateNumber(self)
    
      elif self.field == "ci":
        validateCI(self)
    
      elif self.field == "others":
        validateEmptyField(self)
    except Exception as err:
      raise

class CustomDropdown(ft.Dropdown):
  def __init__(self, label, expand=False, options:list=[], mode="light", value=None):
    super().__init__()
    self.label = label
    self.options = options
    self.border_width = 2
    self.expand = expand
    self.value = value
    
    self.text_size = 18
    
    if mode == "gradient":
      self.color = constants.WHITE
      self.border_color=constants.WHITE_GRAY
      self.focused_border_color=constants.ORANGE_LIGHT
      self.label_style=ft.TextStyle(
        color=constants.ORANGE_LIGHT
      )
    else:
      self.color = constants.BLACK
      self.border_color = constants.BLACK_GRAY
      self.focused_border_color=constants.BLACK
      self.label_style=ft.TextStyle(
        color=constants.BLACK
      )
    
    self.on_change = lambda e: validateEmptyField(self)
    
class CustomUserIcon(ft.Container):
  def __init__(self, initial, fontSize: int = 24, width: int = 60, height: int = 60, gradient: bool = True):
    super().__init__()
    self.width = width
    self.height = height
    self.border_radius = ft.border_radius.all(50)
    self.fontSize = fontSize
    # self.padding = ft.padding.all(10)
    self.alignment = ft.alignment.center
    
    if gradient:
      self.gradient = ft.LinearGradient(
        begin=ft.alignment.top_center,
        end=ft.alignment.bottom_center,
        colors=[constants.BROWN, constants.BLACK]
      )
      self.content = ft.Text(value=initial, size=self.fontSize, weight=ft.FontWeight.BOLD, color=constants.ORANGE_LIGHT)
    else:
      self.bgcolor = ft.colors.TRANSPARENT
      self.border = ft.border.all(2, constants.BLACK_GRAY)
      self.content = ft.Text(value=initial, size=self.fontSize, weight=ft.FontWeight.BOLD, color=constants.BLACK)
    
class CustomAppBar(ft.AppBar):
  def __init__(self, title, page, initial=""):
    super().__init__()
    self.page = page
    self.initial = initial
    
    if not initial == "":
      self.leading = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          CustomUserIcon(initial=self.initial, gradient=True)
        ],
        expand=True
      )
    
    self.leading_width = 70
    self.title = ft.Text(title, color=constants.BLACK, weight=ft.FontWeight.W_700, size=32)
    self.toolbar_height = 70
    self.center_title = True
    self.surface_tint_color = constants.BLACK
    self.elevation = 1
    self.shadow_color = constants.WHITE_GRAY
    self.bgcolor = constants.WHITE
    self.actions = [
      ft.PopupMenuButton(
        icon_color=constants.BLACK,
        icon_size=32,
        padding=ft.padding.all(12),
        bgcolor=constants.WHITE,
        items=[
          ft.PopupMenuItem(
            content=ft.Row(
              alignment=ft.MainAxisAlignment.START,
              vertical_alignment=ft.CrossAxisAlignment.CENTER,
              controls=[
                ft.Icon(
                  name=ft.Icons.SETTINGS_ROUNDED,
                  size=32,
                  color=constants.BLACK,
                ),
                ft.Text(
                  value="Configuración",
                  size=20,
                  weight=ft.FontWeight.W_400,
                  color=constants.BLACK,
                )
              ]
            ),
          ),
          ft.PopupMenuItem(
            content=ft.Row(
              alignment=ft.MainAxisAlignment.START,
              vertical_alignment=ft.CrossAxisAlignment.CENTER,
              controls=[
                ft.Icon(
                  name=ft.Icons.CURRENCY_EXCHANGE_ROUNDED,
                  color=constants.BLACK,
                  size=32,
                ),
                ft.Text(
                  value="Tasa de cambio",
                  size=20,
                  weight=ft.FontWeight.W_400,
                  color=constants.BLACK,
                )
              ]
            ),
            on_click=lambda e: self.openExchangeDialog()
          ),
          ft.PopupMenuItem(
            content=ft.Row(
              alignment=ft.MainAxisAlignment.START,
              vertical_alignment=ft.CrossAxisAlignment.CENTER,
              controls=[
                ft.Icon(
                  name=ft.icons.INVENTORY_ROUNDED,
                  color=constants.BLACK_GRAY,
                  size=32,
                ),
                ft.Text(
                  value="Estado de inventario",
                  color=constants.BLACK,
                  weight=ft.FontWeight.W_400,
                  size=20,
                )
              ]  
            ),  
            on_click=lambda e: self.openStockDialog()
          ),
          ft.PopupMenuItem(),
          ft.PopupMenuItem(
            content=ft.Row(
              alignment=ft.MainAxisAlignment.START,
              vertical_alignment=ft.CrossAxisAlignment.CENTER,
              controls=[
                ft.Icon(
                  name=ft.Icons.LOGOUT_OUTLINED,
                  color=constants.BLACK,
                  size=32,
                ),
                ft.Text(
                  value="Cerrar sesión",
                  color=constants.BLACK,
                  weight=ft.FontWeight.W_400,
                  size=20,
                )
              ]
            ),
            on_click=self.openLogoutDialog
          ),
        ]
      )
    ]
    
  def openStockDialog(self):
    try:
      self.dialog = CustomLowStockDialog(
        page=self.page
      )
      
      self.page.open(self.dialog)
    except: 
      raise
    
  def openExchangeDialog(self):
    try:
      self.dialog = CustomExchangeDialog(
        page=self.page,
      )
      
      self.page.open(self.dialog)
    except:
      raise
  
  def openLogoutDialog(self, e):
    self.dialog = CustomAlertDialog(
      modal=True,
      title="¿Deseas cerrar sesión?",
      content="",
      actions=[
        CustomTextButton(text="Sí", on_click=self.logout),
        CustomTextButton(text="No", on_click=lambda e: self.page.close(self.dialog)),
      ]
    )
    self.page.open(self.dialog)
    
  def logout(self, e):
    from interface import initApp
    self.page.close(self.dialog)
    self.page.controls.clear()
    
    initApp(self.page)
    
class CustomAlertDialog(ft.AlertDialog):
  def __init__(self, title, content=None, modal:bool=True, actions: list = []):
    super().__init__()
    self.title = ft.Text(
      value=title,
      size=24,
      color=constants.BLACK,
      weight=ft.FontWeight.W_500,
    )
    self.content = content
    self.actions = actions
    self.actions_alignment = ft.MainAxisAlignment.END,
    self.modal = modal  
    
class CustomExchangeDialog(CustomAlertDialog):
  def __init__(self, page, title="Actualizar tasa de cambio", exchangeControl=None):
    self.page = page
    self.title = title
    self.exchangeControl = exchangeControl
    
    self.amountField = CustomTextField(
      label="Monto en bolívares",
      field="number",
      expand=True,
      suffix_text="Bs",
      submitFunction=lambda e: self.submitFunction(),
    )
    
    if exchangeRateManager.getRate():
      self.amountField.value = float(exchangeRateManager.getRate())
    
    
    self.content = self.amountField
    
    self.actions = [
      CustomTextButton(text="Confirmar", on_click=lambda e:self.submitFunction()),
      CustomTextButton(text="Cancelar", on_click=lambda e: self.page.close(self)),
    ]
    
    super().__init__(
      modal=True,
      title=self.title,
      content=self.content,
      actions=self.actions, 
    )
    
    
  def openDialog(self):
    self.page.overlay.append(self)
    self.page.open(self)
  
  def submitFunction(self):
    try:
      if evaluateForm(numbers=[self.amountField]):
        exchangeRateManager.setRate(float(self.amountField.value))
        self.page.close(self)
        if self.exchangeControl:
          pass
    except:
      raise
    
class CustomTextButton(ft.TextButton):
  def __init__(self, text:str, on_click=None, color=ft.colors.BLUE_700):
    super().__init__()
    self.content = ft.Text(
      value=text,
      size=18,
      color=color,
    )
    self.on_click = on_click
    
class CustomExchangeContainer(ft.Container):
  def __init__(self, page, rate):
    super().__init__()
    self.page = page
    self.rate = rate
    
    self.border = ft.border.all(1, constants.WHITE_GRAY)
    self.padding=ft.padding.all(20)
    self.border_radius=ft.border_radius.all(10)
    self.ink = True
    self.ink_color = constants.BLACK_INK
    self.margin = ft.margin.all(10)
    self.on_click = lambda e: self.showExchangeDialog()
    self.alignment=ft.alignment.center
    
    self.defaultIcon = ft.Icon(
      name=ft.Icons.WARNING_ROUNDED,
      color=constants.RED_TEXT,
      size=32,
    )
    
    self.defaultText = ft.Text(
      value="Tasa de cambio sin establecer",
      color=constants.BLACK,
      size=20,
      weight=ft.FontWeight.W_600,
      overflow=ft.TextOverflow.ELLIPSIS,
    )
    
    self.defaultContent = ft.Row(
      alignment=ft.MainAxisAlignment.CENTER,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        self.defaultIcon,
        self.defaultText,
      ]
    )
    
    self.exchangeIcon = ft.Icon(
      name=ft.Icons.CURRENCY_EXCHANGE_ROUNDED,
      color=constants.BLACK,
      size=32,
    )
    
    self.exchangeText = ft.Text(
      value=f"{self.rate}Bs" if self.rate else "0Bs",
      color=constants.BLACK,
      size=20,
      weight=ft.FontWeight.W_600,
      overflow=ft.TextOverflow.ELLIPSIS,
    )
    
    self.exchangeContent = ft.Row(
      alignment=ft.MainAxisAlignment.CENTER,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        self.exchangeIcon,
        ft.Text(
          value="Tasa de cambio establecida:",
          color=constants.BLACK,
          size=20,
        ),
        self.exchangeText,
      ]
    )
    
    self.animatedContainer = CustomAnimatedContainer(
      actualContent=self.exchangeContent if self.rate else self.defaultContent
    )
    
    self.content = self.animatedContainer
    
  def showExchangeDialog(self):
    try:
      self.dialog = CustomExchangeDialog(
        page=self.page,
      )
      
      self.page.open(self.dialog)
    except:
      raise
    
  def updateAboutRate(self, newRate):
    try:
      self.rate = newRate
      
      self.exchangeText.value = f"{self.rate}Bs" if self.rate else "0Bs"
      
      newContent = self.exchangeContent if self.rate else self.defaultContent
      
      if newContent == self.animatedContainer.content:
        self.animatedContainer.content.update()
      else:
        self.animatedContainer.setNewContent(newContent)
    except:
      raise
    
    
class CustomSidebar(ft.Container):
  def __init__(self, page):
    super().__init__()
    self.margin = ft.margin.all(0)
    self.gradient = ft.LinearGradient(
      begin=ft.alignment.center_left,
      end=ft.alignment.center_right,
      colors=[constants.BLACK, constants.BROWN]
    )
    self.page = page
    self.border_radius = ft.border_radius.only(top_right=20, bottom_right=20)
    self.shadow = ft.BoxShadow(
      spread_radius = 1,
      blur_radius = 20,
      color = "#555555"
    ) 
    self.width=70
    self.animate = ft.animation.Animation(
      duration=300, 
      curve=ft.AnimationCurve.EASE_IN_OUT,
    )
    
    self.openButton = ft.IconButton(
      icon=ft.Icons.ARROW_RIGHT,
      # icon_color=constants.WHITE,
      selected_icon=ft.Icons.ARROW_LEFT,
      on_click=self.toggleIconButton,
      icon_size=50,
      selected=False,
      style=ft.ButtonStyle(
        color={
          "selected": constants.ORANGE_OVERLAY,
          "": constants.WHITE
        }
      )
    )
    
    self.home = CustomNavigationOptions(icon=ft.Icons.HOME_WORK_ROUNDED, text="Inicio", function=self.selectOne, inkColor="#666666",)
    self.sales = CustomNavigationOptions(icon=ft.Icons.SELL_ROUNDED, text="Ventas", function=self.selectOne, inkColor="#666666", default=True)
    self.payments = CustomNavigationOptions(icon=ft.Icons.WALLET_ROUNDED, text="Pagos", function=self.selectOne, inkColor="#666666",)
    self.users = CustomNavigationOptions(icon=ft.Icons.SECURITY_ROUNDED, text="Usuarios", function=self.selectOne, inkColor="#666666",)
    self.clients = CustomNavigationOptions(icon=ft.Icons.PEOPLE_ROUNDED, text="Clientes", function=self.selectOne, inkColor="#666666",)
    self.employees = CustomNavigationOptions(icon=ft.Icons.WORK_ROUNDED, text="Empleados", function=self.selectOne, inkColor="#666666",)
    self.closings = CustomNavigationOptions(icon=ft.Icons.MONEY_ROUNDED, text="Cierres", function=self.selectOne, inkColor="#666666",)
    self.statistics = CustomNavigationOptions(icon=ft.Icons.SSID_CHART_ROUNDED, text="Estadísticas", function=self.selectOne, inkColor="#666666",)
    self.inventory = CustomNavigationOptions(icon=ft.Icons.INVENTORY_2_ROUNDED, text="Inventario", function=self.selectOne, inkColor="#666666")
    
    
    self.navigationOptions = [
      self.users,
      self.clients,
      self.employees,
      self.sales,
      self.inventory,
      self.payments,
      self.closings,
    ]
    
    self.content = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          vertical_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[self.openButton]
        ),
        ft.Column(
          expand=True,
          alignment=ft.MainAxisAlignment.CENTER,
          scroll=ft.ScrollMode.AUTO,
          controls=[
            ft.Row([self.users]),
            ft.Row([self.employees]),
            ft.Row([self.clients]),
            ft.Row([self.inventory]),
            ft.Row([self.sales]),
            ft.Row([self.payments]),
            ft.Row([self.closings]),
          ]
        ),
      ]
    )
    self.selected = self.sales
  
  def toggleIconButton(self, e):
    self.openButton.selected = not e.control.selected
    self.openContainer()
    self.openButton.update()
    
  def switchPage(self, pageName):
    if pageName == "Users":
      self.updateMainContent(Users(self.page))
      self.switchButton(self.users)
    elif pageName == "Clients":
      self.updateMainContent(Clients(self.page))
      self.switchButton(self.clients)
    elif pageName == "Employees":
      self.updateMainContent(Employees(self.page))
      self.switchButton(self.employees)
    elif pageName == "Sales":
      self.updateMainContent(Sales(self.page))
      self.switchButton(self.sales)
    elif pageName == "Inventory":
      self.updateMainContent(Inventory(self.page))
      self.switchButton(self.inventory)
    elif pageName == "Payments":
      self.updateMainContent(Payments(self.page))
      self.switchButton(self.payments)
    elif pageName == "Closings":
      self.updateMainContent(Closings(self.page))
      self.switchButton(self.closings)
      
  def switchButton(self, newSelected):
    self.selected.deselectOption()
    self.selected = newSelected
    self.selected.selectOption()
  
  def selectOne(self, e):
    def switchTo(button):
      self.switchButton(button)
      exchangeRateManager.clearSubscribers()
      
    if not self.selected == e.control:
      button = e.control

      if e.control == self.users and verifyPermission(self.page):
        from Modules.Sections.UsersSection.users import Users
        self.updateMainContent(Users(self.page))  
        switchTo(button)
      elif e.control == self.clients and verifyPermission(self.page):
        from Modules.Sections.ClientsSection.clients import Clients
        self.updateMainContent(Clients(self.page))
        switchTo(button)
      elif e.control == self.employees and verifyPermission(self.page):
        from Modules.Sections.EmployeesSection.employees import Employees
        self.updateMainContent(Employees(self.page))
        switchTo(button)
      elif e.control == self.sales:
        from Modules.Sections.SalesSection.sales import Sales
        self.updateMainContent(Sales(self.page))
        switchTo(button)
      elif e.control == self.inventory:
        from Modules.Sections.InventorySection.inventory import Inventory
        self.updateMainContent(Inventory(self.page))
        switchTo(button)
      elif e.control == self.payments and verifyPermission(self.page):
        from Modules.Sections.PaymentsSection.payments import Payments 
        self.updateMainContent(Payments(self.page))
        switchTo(button)
      elif e.control == self.closings and verifyPermission(self.page):
        from Modules.Sections.ClosingsSection.closings import Closings
        self.updateMainContent(Closings(self.page))
        switchTo(button)
    
  def openContainer(self):
    if self.width == 70:
      self.width = 200
    else:
      self.width = 70  
    for option in self.navigationOptions:
        option.animateOpacityText()
    self.update()
    
  def updateMainContent(self, newContent):
    if hasattr(self.page, "mainContainer"):
      self.page.mainContainer.setNewContent(newContent)
    
class CustomNavigationOptions(ft.Container):
  def __init__(self, icon, text, function, color = constants.WHITE, highlightColor="white10", inkColor="#888888", focusedColor = constants.ORANGE_OVERLAY, contentAlignment=ft.MainAxisAlignment.START, opacityInitial:int=0, default:bool=False):
    super().__init__()
    self.expand = True
    self.on_hover = self.highlight
    self.padding = ft.padding.symmetric(vertical=15, horizontal=20)
    self.border_radius = 10
    self.on_click = function
    self.margin = 0
    self.ink = True
    self.ink_color = inkColor
    self.color = color
    self.focusedColor = focusedColor
    self.highlightColor = highlightColor
    self.default = default
    
    if not default:
      self.optionIcon = ft.Icon(name=icon, color=self.color, size=24)
      self.optionText = ft.Text(value=text, color=self.color, size=20, animate_opacity=300, opacity=opacityInitial, weight=ft.FontWeight.NORMAL)
    else:
      self.optionIcon = ft.Icon(name=icon, color=self.focusedColor, size=24,)
      self.optionText = ft.Text(value=text, color=self.focusedColor, size=20, animate_opacity=300, opacity=opacityInitial, weight=ft.FontWeight.W_600)
    
    self.content = ft.Row(
      alignment=contentAlignment,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        self.optionIcon,
        self.optionText,
      ]
    )
    
  def animateOpacityText(self):
    self.optionText.opacity = 1 if self.optionText.opacity == 0 else 0
    self.update()
    
  def selectOption(self):
    self.optionIcon.color = self.focusedColor
    self.optionText.color = self.focusedColor
    self.optionText.weight = ft.FontWeight.W_600
    self.update()
    
  def deselectOption(self):
    self.optionIcon.color = self.color
    self.optionText.color = self.color 
    self.optionText.weight = ft.FontWeight.NORMAL 
    self.update()
  
  def highlight(self, e):
    if e.data == "true":
      e.control.bgcolor = self.highlightColor
      e.control.update()
    else:
      e.control.bgcolor = None
      e.control.update()
  
class CustomMainContainer(ft.Container):
  def __init__(self, content):
    super().__init__()
    self.expand = True
    self.padding = 0
    self.margin = 5
    
    self.switcher = CustomAnimatedContainer(
      actualContent=content,
      transition=ft.AnimatedSwitcherTransition.FADE,
      duration=400,
      reverse_duration=200,
    )
    
    self.content = self.switcher
    
  def setNewContent(self, newContent):
    self.switcher.content = newContent
    self.switcher.update() 
    
class CustomCardInfo(ft.Card):
  def __init__(self, icon, title, subtitle="", width:int=300, height:int=150, spacing:int=0, containerClickFunction=None, TextButtons=[], variant=ft.CardVariant.ELEVATED):
    super().__init__(variant=variant)
    self.width = width
    self.height = height
    self.spacing = spacing
    self.icon = icon
    self.title = title
    self.subtitle = subtitle
    self.textButtons = []
    self.containerClickFunction = containerClickFunction
    
    self.content = ft.Column(
      width=self.width,
      height=self.height,
      expand=True,
      spacing=self.spacing,
      controls=[
        ft.Container(
          padding=ft.padding.all(5),
          ink=True,
          border_radius=ft.border_radius.all(10),
          margin=ft.margin.all(10),
          on_click=containerClickFunction,
          ink_color=constants.BLACK_INK,
          content=ft.ListTile(
            leading=ft.Icon(
              name=self.icon, 
              size=24, 
              color=constants.BLACK
            ),
            title=ft.Text(
              value=self.title,
            ),
            subtitle=ft.Text(
              self.subtitle,
            )
          )
        ),
      ]
    )
    
class CustomDatePicker(ft.DatePicker):
  def __init__(self, firstDate=datetime(year=1940, month=1, day=1), lastDate=datetime(year=datetime.now().year-18, month=datetime.now().month, day=datetime.now().day), on_change=None, on_dismiss=None):
    super().__init__()
    self.first_date = firstDate
    self.last_date = lastDate
    self.on_change = on_change
    self.on_dismiss = on_dismiss
    
    self.date_picker_entry_mode = ft.DatePickerEntryMode.CALENDAR
    self.confirm_text = "Confirmar"
    self.cancel_text = "Cancelar"
  
class CustomEditButton(ft.OutlinedButton):
  def __init__(self, function=None, mode="light", size=24):
    super().__init__()
    self.mode = mode
    self.size = size
    self.function = function
    self.color = constants.BLACK if self.mode == "light" else constants.ORANGE_LIGHT
    
    self.style = ft.ButtonStyle(
      color=self.color,
      padding=0,
      side=ft.BorderSide(
        width=2,
        color=self.color
      )
    )
    
    self.content = ft.Icon(
      name=ft.Icons.EDIT_ROUNDED,
      color=self.color,
      size=self.size
    )
    
    self.on_click = self.function

class CustomDeleteButton(ft.OutlinedButton):
  def __init__(self, page, function=None, mode="light", size=24):
    super().__init__()
    self.mode = mode
    self.size = size
    self.page = page
    self.function = function
    self.color = constants.BLACK if self.mode == "light" else constants.ORANGE_LIGHT
    
    self.style = ft.ButtonStyle(
      color=self.color,
      padding=0,
      side=ft.BorderSide(
        width=2,
        color=self.color
      )
    )
    
    self.content = ft.Icon(
      name=ft.Icons.DELETE_ROUNDED,
      color=self.color,
      size=self.size
    )
    
    self.on_click = self.showWarningDialog if not self.function == None else None
    
  def showWarningDialog(self, e):
    self.newDialog = CustomAlertDialog(
      title="¿Estás seguro de llevar a cabo esta acción?",
      content=ft.Text(
        value="Los datos se eliminarán permanentemente",
        size=18, 
        color=constants.BLACK,
      ),
      actions=[
        CustomTextButton(text="Eliminar", on_click=self.executeFunction),
        CustomTextButton(text="Cancelar", on_click=self.closeDialog)
      ]
    )
    self.page.open(self.newDialog)
  
  def executeFunction(self, e):
    self.page.close(self.newDialog)
    self.function()
    
  def closeDialog(self, e):
    self.page.close(self.newDialog)
    
class CustomImageSelectionContainer(ft.Container):
  def __init__(self, page, src=None, height:int=200, width:int=200):
    super().__init__()
    self.height = height
    self.width = width
    self.page = page
    self.src = src
    self.border_radius = ft.border_radius.all(20)
    
    self.selectedImagePath = self.src
    
    self.imageIcon = ft.Container(
      border=ft.border.all(2, constants.WHITE_GRAY),
      border_radius=ft.border_radius.all(30),
      bgcolor=ft.colors.TRANSPARENT,
      height=150,
      width=150,
      alignment=ft.alignment.center,
      content=ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        controls=[
          ft.Icon(
            name=ft.Icons.ADD_PHOTO_ALTERNATE_ROUNDED,
            color=constants.BLACK,
            size=32,
          ),
          ft.Text(
            value="Agregar imagen",
            color=constants.BLACK,
            size=16,
          )
        ]
      )
    )
    
    if not self.selectedImagePath:
      self.editImageContainer = CustomAnimatedContainer(
        actualContent=self.imageIcon
      )
    else:
      self.editImageContainer = CustomAnimatedContainer(
        actualContent=CustomImageContainer(
          src=self.selectedImagePath,
          shadow=False,
        )
      )
    
    self.selectImage = ft.Container(
      border_radius=ft.border_radius.all(30),
      height=150,
      width=150,
      alignment=ft.alignment.center,
      content=self.editImageContainer,
      ink=True,
      ink_color=constants.BLACK_INK,
      on_click=self.openFilePicker
    )
    
    self.deleteButton = ft.Container(
      visible=False if self.src == None else True,
      content=CustomTextButton(
        text="Eliminar",
        color=constants.RED_FAILED,
        on_click=self.deleteImage,
      )
    )
    
    self.filePicker = ft.FilePicker(
      on_result=self.updateImage
    )
    
    self.content = ft.Column(
      expand=True,
      alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        self.selectImage,
        self.deleteButton
      ]
    )
    
  def turnOnButtonVisibility(self):
    self.deleteButton.visible = True
    self.deleteButton.update()
    
  def turnOffButtonVisibility(self):
    self.deleteButton.visible = False
    self.deleteButton.update()
    
  def openFilePicker(self, e):
    try:
      if self.filePicker not in self.page.overlay:
        self.page.overlay.append(self.filePicker)
      self.page.update()
      self.filePicker.pick_files(
        allow_multiple=False
      )
    except Exception as err:
      print(err)
      
  def validFileExtension(self, filePath):
    allowedExtensions = [".jpg", ".jpeg", ".png", ".jfif"]
    fileExtension = os.path.splitext(filePath)[1].lower()
    return fileExtension in allowedExtensions
    
  def updateImage(self, e:ft.FilePickerResultEvent):
    try:
      if e.files:
        for file in e.files:
          if self.validFileExtension(file.path):
            image = CustomImageContainer(
              src=file.path,
              shadow=False,
            )
            
            self.selectedImagePath = file.path
            self.editImageContainer.setNewContent(image)
            self.turnOnButtonVisibility()
          else:
            print(f"Tipo de archivo no permitido: {os.path.splitext(file.path)[1].lower()}")
    except Exception as err:
      raise
    
  def deleteImage(self, e):
    if self.selectedImagePath:
      self.editImageContainer.setNewContent(self.imageIcon)
      self.selectedImagePath = None
      self.turnOffButtonVisibility()
      
class CustomImageContainer(ft.Container):
  def __init__(self, src=None, border_radius=10, fit=ft.ImageFit.COVER, width:int=200, height:int=200, border=True, bgcolor=constants.WHITE, shadow=True):
    super().__init__()
    self.height = height
    self.width = width
    self.bgcolor = bgcolor
    self.alignment = ft.alignment.center
    self.border_radius = border_radius
    self.shadow = ft.BoxShadow(
      spread_radius=1,
      blur_radius=1,
      color=constants.WHITE_GRAY,
    ) if shadow else None
    
    if src:
      self.content = ft.Image(
        src=src,
        fit=fit,
        width=self.width,
        height=self.height,
      )
    else:
      # self.border = ft.border.all(2, constants.WHITE_GRAY) if border == True else None
      self.content = ft.Icon(
        name=ft.Icons.IMAGE_ROUNDED,
        color=constants.BLACK,
        size=32,
      )
    
class CustomAutoComplete(ft.Container):
  def __init__(self, height=60, width=250, expand=False, on_select=None, suggestions:list=[]):
    super().__init__()
    self.height = height
    self.width = width
    self.expand = expand
    self.border = ft.border.all(2, constants.WHITE_GRAY)
    self.border_radius = ft.border_radius.all(20)
    self.margin = ft.margin.symmetric(vertical=10)
    self.alignment = ft.alignment.center
    self.content = ft.AutoComplete(
      suggestions=suggestions,
      on_select=on_select,
    )
    
class CustomNumberField(ft.Container):
  def __init__(self, label, expand=False, helper_text=None, value=0, on_change=None):
    super().__init__()
    self.width = 220
    self.height = 60
    self.expand = True
    self.label = label
    self.alignment = ft.alignment.center
    self.on_changeFunction = on_change
    self.fieldValue = 0
    
    self.field = ft.TextField(
      expand=expand,
      label=self.label,
      value=value,
      color=constants.BLACK,
      border_color=constants.BLACK_GRAY,
      focused_border_color=constants.BLACK,
      helper_text=helper_text,
      border_width=2,
      input_filter=ft.NumbersOnlyInputFilter(),
      label_style=ft.TextStyle(
        color=constants.BLACK,
      ),
      cursor_color=constants.BLACK,
      text_align=ft.TextAlign.CENTER,
      text_size=18,
      on_blur=self.onBlurFunction,
      on_change=lambda e: self.on_changeFun(),
      content_padding=ft.padding.symmetric(horizontal=20, vertical=10),
    )
    
    self.content = ft.Row(
      alignment=ft.MainAxisAlignment.CENTER,
      spacing=5,
      controls=[
        ft.IconButton(
          icon=ft.Icons.REMOVE_ROUNDED,
          icon_color=constants.BLACK,
          icon_size=24,
          on_click=self.removeOne,
        ),
        self.field,
        ft.IconButton(
          icon=ft.Icons.ADD_ROUNDED,
          icon_color=constants.BLACK,
          icon_size=24,
          on_click=self.addOne,
        )
      ]
    )
  
  def addOne(self, e):
    self.field.value = int(self.field.value) + 1
    self.on_changeFun()
  
  def removeOne(self, e):
    if not int(self.field.value) == 0:
      self.field.value = int(self.field.value) - 1
      self.on_changeFun()
      
  def on_changeFun(self):
    self.updateField()
    self.on_changeFunction()
  
  def updateField(self):
    self.field.update()
    self.updateFieldValue()
  
  def updateFieldValue(self):
    try:
      self.fieldValue = int(self.field.value)
    except Exception as err:
      pass
    
  def onBlurFunction(self, e):
    if self.field.value == "":
      self.field.value = "0"
      self.on_changeFun()
    
class CustomTooltip(ft.Tooltip):
  def __init__(self, message, content, border_radius=10, padding=20, bgcolor=constants.WHITE,):
    super().__init__(message=message, content=content)
    self.border_radius = border_radius
    self.padding = padding
    self.bgcolor = bgcolor
    
    self.text_style=ft.TextStyle(size=20, color=constants.BLACK)
    
    self.text_align = ft.TextAlign.CENTER
    
    self.border = ft.border.all(2, constants.BLACK_GRAY)
    
    self.prefer_below = False
    
    self.enable_feedback = True
    
class CustomContainerButtonGradient(ft.Container):
  def __init__(self, text, borderColor, gradientColor, on_click=None, expand=True, height=80, alignment=ft.alignment.center, textSize=24):
    super().__init__()
    self.expand = expand
    self.alignment = alignment
    self.borderColor = borderColor
    self.gradientColor = gradientColor
    self.padding = ft.padding.symmetric(horizontal=30, vertical=20)
    self.on_click = on_click
    
    self.border = ft.border.only(bottom=ft.border.BorderSide(3, self.borderColor))
    
    self.border_radius = ft.border_radius.all(10)
    
    self.animate = ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
    
    self.content = ft.Text(
      value=text,
      size=textSize,
      color=constants.BLACK,
      weight=ft.FontWeight.W_700,
    )
    
    self.on_hover = self.on_hoverFunction
  
  def on_hoverFunction(self, e):
    self.gradient = ft.LinearGradient(
      begin=ft.alignment.bottom_center,
      end=ft.alignment.top_center,
      colors=[self.gradientColor, ft.colors.WHITE10],
    ) if e.data == "true" else None
    
    self.update()
    
class CustomItemsDialog(ft.AlertDialog):
  def __init__(self, page, width:int=800, height:int=500, title:str="Buscar Productos y Combos", finalFunction=None, products:bool=True, combos:bool=False):
    super().__init__()
    self.page = page
    
    self.products = products
    self.combos = combos
    self.modal = True
    self.selectedItems = []
    self.finalFunction = finalFunction
    
    self.title = ft.Text(
      value=title,
      size=32,
      weight=ft.FontWeight.W_700,
      color=constants.BLACK,
      text_align=ft.TextAlign.CENTER,
    )
    
    self.productButton = CustomNavigationOptions(
      icon=ft.Icons.COFFEE_ROUNDED,
      text="Productos",
      function=self.switchView,
      color="#666666",
      focusedColor=constants.BLACK,
      opacityInitial=1,
      highlightColor=None,
      contentAlignment=ft.MainAxisAlignment.CENTER,
      default=True if products == True else False,
    )
    
    self.comboButton = CustomNavigationOptions(
      icon=ft.Icons.FASTFOOD_ROUNDED,
      text="Combos",
      function=self.switchView,
      color="#666666",
      focusedColor=constants.BLACK,
      opacityInitial=1,
      default=False if products == True else True,
      highlightColor=None,
      contentAlignment=ft.MainAxisAlignment.CENTER,
    )

    self.navigationButtons = ft.Container(
      margin=ft.margin.symmetric(horizontal=20, vertical=10),
      bgcolor=ft.colors.TRANSPARENT, 
      height=60,
      width=400,
      alignment=ft.alignment.center,
      content=ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        spacing=20,
      )
    )
    
    self.productsView = CustomGridView(
      expand=True,
      width=800,
      controls=self.getItems("Products"),
    )
    
    self.combosView = CustomGridView(
      expand=True,
      width=800,
      controls=self.getItems("Combos")
    )
    
    if self.products:
      self.navigationButtons.content.controls.append(self.productButton)
    if self.combos:
      self.navigationButtons.content.controls.append(self.comboButton)
    
    self.itemsContainer = CustomAnimatedContainerSwitcher(
      bgcolor=ft.colors.TRANSPARENT,
      content=ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ALWAYS,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
        ]
      )
    )
    
    self.cancelButton = CustomContainerButtonGradient(
      text="Cancelar",
      borderColor=constants.RED_TEXT,
      gradientColor=constants.RED_FAILED_LIGHT,
      on_click=lambda e: self.closeDialog()
    )
    
    self.confirmButton = CustomContainerButtonGradient(
      text="Confirmar",
      borderColor=constants.GREEN_TEXT,
      gradientColor=constants.GREEN_LIGHT,
      on_click=lambda e: self.confirmFunction(),
    )
    
    self.selectedView = self.productButton if products == True else self.comboButton
    self.actualView = self.productsView if products == True else self.combosView
    
    self.content = ft.Column(
      alignment=ft.MainAxisAlignment.START,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      spacing=5,
      width=1000,
      expand=True,
      controls=[
        self.navigationButtons,
        ft.Divider(color=constants.WHITE_GRAY),
        self.actualView,
        ft.Divider(color=constants.WHITE_GRAY),
        ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          controls=[
            self.cancelButton,
            self.confirmButton,
          ]
        )
      ]
    )
    
  def openDialog(self, selectedItems):
    self.selectedItems = selectedItems.copy()

    self.page.open(self)
    self.updateItemSelection()
    
  def updateItemSelection(self):
    for container in self.productsView.controls:
      print(f"Product: {container.item.name} - Selected: {container.item.name in self.selectedItems}")
      if container.selected and container.item.name not in self.selectedItems:
        container.selectImage(select=False)
      elif not container.selected and container.item.name in self.selectedItems:
        container.selectImage(select=True)
    for container in self.combosView.controls:
      if container.selected and container.item.name not in self.selectedItems:
        container.selectImage(select=False)
      elif not container.selected and container.item.name in self.selectedItems:
        container.selectImage(select=True)
    self.update()
  
  def closeDialog(self):
    self.page.close(self)
    
  def confirmFunction(self):
    self.closeDialog()
    self.finalFunction(self.selectedItems)
    
  def updateView(self):
    try:
      # Actualiza los items que se van a seleccionar
      self.actualView = self.productsView if self.selectedView == self.productButton else self.combosView
      self.content.controls[2] = self.actualView
      self.content.update()
    except:
      raise
    
  def switchView(self, e):
    try:
      # Cambia la vista entre productos y categorías
      if not e.control == self.selectedView:
        self.selectedView.deselectOption()
        self.selectedView = e.control
        self.selectedView.selectOption()
        self.updateView()
    except:
      raise
  
  def getItems(self, view:str):
    try:
      # Obtiene los cardItems a mostrar
      with getDB() as db:
        content = []
        if view == "Products" and self.products:
          products = getProducts(db)
          
          for product in products:
            itemCard = CustomItemCard(
              page=self.page,
              item=product,
              on_click=self.selectItem,
              selected=True if product.name in self.selectedItems else False,
            )
            print(f"Product: {product.name} - Selected: {product.name in self.selectedItems}")
            content.append(itemCard)
        elif view == "Combos" and self.combos:
          combos = getCombos(db)
          
          for combo in combos:
            itemCard = CustomItemCard(
              page=self.page,
              item=combo,
              on_click=self.selectItem,
              selected=True if combo.name in self.selectedItems else False,
            )
            content.append(itemCard)
        return content
    except:
      raise
  
  def selectItem(self, e):
    try:
      e.control.selectImage(select=not e.control.selected)
      e.control.update()
      if e.control.selected:
        self.selectedItems.append(e.control.item.name)
      else:
        self.selectedItems.remove(e.control.item.name)
    except:
      raise
    
class CustomItemCard(ft.Container):
  def __init__(self, page, item, width=200, height=200, on_click=None, selected=False):
    super().__init__()
    self.height = height
    self.width = width
    self.page = page 
    self.item = item
    self.on_click = on_click
    self.selected = selected

    self.border_radius = ft.border_radius.all(30)
    self.shadow = ft.BoxShadow(
      blur_radius=5,
      spread_radius=1,
      color=constants.BLACK_GRAY,
    )
    self.animate = ft.animation.Animation(250, ft.AnimationCurve.EASE_IN_OUT)
    
    with getDB() as db:
      imageManager = ImageManager()
      self.imageContainer = CustomImageContainer(
        src=imageManager.getImagePath(item.imgPath),
        height=self.height,
        width=self.width,
        border=False,
        bgcolor=constants.WHITE,
      )
      
      self.shaderControl = ft.ShaderMask(
        content=self.imageContainer,
        blend_mode=ft.BlendMode.MULTIPLY,
        shader=ft.LinearGradient(
          begin=ft.alignment.bottom_center,
          end=ft.alignment.center,
          colors=[ft.colors.BLACK, ft.colors.TRANSPARENT],
        ),
        border_radius=30,
      )
      
      self.textName = ft.Text(
        value=f"{item.name}",
        size=26,
        color=constants.WHITE,
        weight=ft.FontWeight.W_700,
        overflow=ft.TextOverflow.ELLIPSIS,
        max_lines=1,
      )
      
    self.checkControl = ft.Container(
      bottom=10,
      right=10,
      scale=0 if self.selected == False else 1,
      animate_scale=ft.animation.Animation(600, ft.AnimationCurve.ELASTIC_OUT),
      content=ft.Icon(
        name=ft.Icons.CHECK_CIRCLE_ROUNDED,
        size=32,
        color=constants.GREEN_SUCCESS,
      ),
      border_radius=50,
      shadow=ft.BoxShadow(
        blur_radius=5,
        spread_radius=1,
        color=constants.BLACK,
      )
    )
    
    self.imageControl = ft.Stack(
      expand=True,
      controls=[
        self.shaderControl,
        ft.Container(
          bottom=0,
          left=10,
          right=10,
          expand=True,
          # width=self.width,
          content=self.textName,
          padding=ft.padding.symmetric(vertical=10),
          alignment=ft.alignment.center,
        ),
        self.checkControl,
      ]
    )
    
    self.content = self.imageControl
    
  def selectImage(self, select=True):
    self.checkControl.scale = 1 if select else 0
    self.selected = select
    
    if select:
      self.border = ft.border.all(4, constants.GREEN_SUCCESS)
      threading.Timer(0.25, self.removeBorder).start()
    
    # self.update()
  
  def deselectImage(self):
    self.checkControl.scale = 0
    self.border = ft.border.all(4, constants.GREEN_SUCCESS)
    self.update()
    
    threading.Timer(0.25, self.removeBorder).start()
    self.selected = False
  
  def removeBorder(self):
    self.border = None
    self.update()
    
class CustomItemsSelector(ft.Container):
  def __init__(self, page, width=800, height=400, products=True, combos=False, sale=False, priceCard=None):
    super().__init__()
    self.page = page
    self.products = products
    self.combos = combos
    self.expand = True
    self.padding = ft.padding.all(10)
    self.price = 0
    self.selectedItems = []
    self.showedItems = []
    self.sale = sale
    self.priceCard = priceCard

    self.alignment = ft.alignment.center
    self.expand = True
    
    self.initialContent = CustomInitialRowContent(
      message="Selecciona los productos deseados",
    )
    
    self.itemsList = ft.Column(
      scroll=ft.ScrollMode.ALWAYS,
      expand=True,
      controls=[
        
      ]
    )
    
    self.priceText = ft.Text(
      value="0.00$",
      size=32,
      color=constants.ORANGE_LIGHT,
      weight=ft.FontWeight.W_700,
      text_align=ft.TextAlign.CENTER,
    )
    
    self.priceContainer = ft.Container(
      gradient=ft.LinearGradient(
        begin=ft.alignment.bottom_center,
        end=ft.alignment.top_center,
        colors=[constants.BLACK, constants.BROWN],
      ),
      border_radius=10,
      alignment=ft.alignment.center,
      shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=5,
        color=constants.WHITE_GRAY,
      ),
      content=ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[self.priceText]
      )
    )
    
    self.itemsContainer = ft.Container(
      expand=True,
      bgcolor=constants.WHITE,
      padding=ft.padding.symmetric(vertical=10, horizontal=10),
      margin=ft.margin.only(bottom=10),
      border_radius=ft.border_radius.all(10),
      shadow=ft.BoxShadow(
        spread_radius=2,
        blur_radius=10,
        blur_style=ft.ShadowBlurStyle.INNER,
        color=constants.BLACK_GRAY,
      ),
      content=ft.Row(
        expand=True,
        controls=[self.itemsList]  
      ),
    )
    
    self.addButton = CustomFilledButton(
      text="Añadir",
      clickFunction=lambda e: self.showSelectionDialog(),
    )
    
    self.resetListButton = CustomOutlinedButton(
      text="Vaciar", 
      clickFunction=lambda e: self.removeAllItems(),
    )
    
    self.content = ft.Column(
      expand=True,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      alignment=ft.MainAxisAlignment.CENTER,
      spacing=0,
      controls=[
        self.priceContainer,
        self.itemsContainer,
        ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          controls=[
            self.resetListButton,
            self.addButton,
          ]
        )
      ]
    )
    
    self.dialog = CustomItemsDialog(
      page=self.page,
      products=self.products,
      combos=self.combos,
      finalFunction=self.getItemsSelected,
    )
    
  def showSelectionDialog(self):
    self.dialog.openDialog(self.selectedItems)
  
  def addItemToList(self, item):
    self.itemsList.controls.append(item)
    
  def animateOffset(self, item):
    item.opacity = 1
    time.sleep(0.05)
    item.update()
    item.offset=ft.transform.Offset(0, 0)
    time.sleep(0.05)
    item.update()
    
  def calculateItemsPrice(self):
    cost = 0
    
    with getDB() as db:
      for itemField in self.itemsList.controls:
        item = itemField.item
        quantity = itemField.quantityField.fieldValue
        
        if hasattr(item, "idProduct"):
          if self.sale:
            # Add product's total price
            cost += calculatePrice(
              cost=item.cost,
              gain=item.gain,
              iva=item.iva,
            ) * quantity
          else:
            # Only add product's cost
            cost += item.cost * quantity
        else:
          cost += item.price * quantity
    
    self.priceText.value = f"{round(cost, 2)}$"
    self.price = cost
    self.priceText.update()
    
    if self.priceCard:
      self.priceCard.updatePriceText(round(cost, 2))
  
  def updateItemsList(self):
    self.itemsList.controls = []
    self.itemsList.update()
    self.itemsList.controls = self.showedItems
    self.itemsList.update()
  
  def removeItem(self, itemField):
    try:
      self.selectedItems.remove(itemField.name)
      self.showedItems.remove(itemField)
      self.updateItemsList()
      
      self.calculateItemsPrice()
    except:
      raise
  
  def removeAllItems(self):
    try:
      self.selectedItems.clear()
      self.showedItems.clear()
      self.itemsList.controls = self.showedItems
      self.itemsList.update()
      
      self.calculateItemsPrice()
    except Exception as err:
      raise
      
    
  def getItemsSelected(self, selectedItems):
    try:
      print(f"selectedItems: {selectedItems}")
      self.selectedItems = selectedItems.copy()
      print(f"self.selectedItems: {self.selectedItems}")
      
      self.showItemsSelected()
    except:
      raise
    
  def showItemsSelected(self):
    try:
      with getDB() as db:
        # Obtener los nombres de los ítems mostrados actualmente
        currentItems = [itemField.name for itemField in self.showedItems]
        print(f"Items mostrados actualmente: {currentItems}")
            
        # Calcular ítems nuevos y eliminados
        newItems = [item for item in self.selectedItems if item not in currentItems]
        removedItems = [itemField for itemField in self.showedItems if itemField.name not in self.selectedItems]
        print(f"Items nuevos: {newItems}")
        print(f"Items eliminados: {[itemField.name for itemField in removedItems]}")
        
        if newItems:
          products = {product.name: product for product in getProducts(db)}
          combos = {combo.name: combo for combo in getCombos(db)}
          
          for itemName in newItems:
            item = products.get(itemName) or combos.get(itemName)
            
            if item:
              itemField = CustomItemQuantityInput(
                page=self.page,
                item=item,
                name=item.name,
                sell=self.sale,
                removeFunction=self.removeItem,
                on_change=self.calculateItemsPrice,
              )
              self.showedItems.append(itemField)
              print(f"Nuevo ítem añadido a la lista de selección: {itemField.item.name}")
        
        for itemField in removedItems:
          self.showedItems.remove(itemField)
          print(f"Item eliminado: {itemField.name}")
        
        self.updateItemsList()
        self.calculateItemsPrice()
        
        print(f"Items mostrados: {[itemField.name for itemField in self.showedItems]}")
        print(f"Containers: {self.showedItems}")
        print(f"Son iguales los showedItems y los itemsList: {self.itemsList.controls == self.showedItems}")
        print(f"Items seleccionados: {self.selectedItems}")
    except Exception as err:
      print(f"Error al mostrar los ítems seleccionados: {err}")
      pass
  
  def getItemsWithQuantity(self):
    try:
      products = []
      combos = []
      
      for itemField in self.itemsList.controls:
        item = itemField.item
        if hasattr(item, "idProduct"):
          itemInfo = {
            "type": "Product",
            "id": item.idProduct,
            "name": item.name,
            "quantity": itemField.quantityField.fieldValue,
            "gain": round(float((item.gain/100) * item.cost * itemField.quantityField.fieldValue), 2) ,
            "price": round(float(itemField.quantityField.fieldValue * calculatePrice(cost=item.cost, gain=item.gain, iva=item.iva) if self.sale else item.cost), 2)
          }
          products.append(itemInfo)
        else:
          itemInfo = {
            "type": "Combo",
            "id": item.idCombo,
            "name": item.name,
            "quantity": itemField.quantityField.fieldValue,
            "gain": round(float((item.price - item.cost) * itemField.quantityField.fieldValue), 2),
            "price": round(float(itemField.quantityField.fieldValue * item.price), 2),
            "products": [],
          }
          
          with getDB() as db:
            comboProducts = getRegisterByComboId(db, item.idCombo)
            
            for register in comboProducts:
              productInfo = {
                "id": register.product.idProduct,
                "name": register.product.name,
                "totalQuantity": register.productQuantity * itemField.quantityField.fieldValue,
                "totalPrice": round(float(calculatePrice(cost=register.product.cost, gain=register.product.gain, iva=register.product.iva)), 2)
              }
              itemInfo["products"].append(productInfo)
            
          combos.append(itemInfo)
      
      return products, combos
    except Exception as err:
      raise
    
  def validateAllItemFields(self):
    try:
      isValid = True
      if len(self.itemsList.controls) == 0:
        raise InvalidData("No se han seleccionado productos.")
      else:
        for itemField in self.itemsList.controls:
          if itemField.quantityField.fieldValue == 0:
            raise InvalidData("No pueden haber campos en 0.")
      return isValid
    except:
      raise
    
class CustomGridView(ft.GridView):
  def __init__(self, expand, controls, width=600, runs_count=5, max_extent=200, child_aspect_ratio=1.0, spacing=10, run_spacing=10):
    super().__init__()
    self.expand = True
    self.semantic_child_count = 3
    self.max_extent = max_extent
    self.child_aspect_ratio = child_aspect_ratio = 1.0
    self.spacing = spacing
    self.run_spacing = run_spacing
    self.padding = ft.padding.all(10)
    
    self.controls = controls
    
class CustomItemQuantityInput(ft.Container):
  def __init__(self, page, item, name, sell=False, opacity=1, removeFunction=None, on_change=None):
    super().__init__()
    self.item = item
    self.name = name
    self.type = "Product" if hasattr(self.item, "idProduct") else "Combo"
    self.page = page
    self.sell = sell
    self.border_radius = ft.border_radius.all(10)
    self.opacity = opacity
    self.bgcolor = constants.WHITE
    self.margin = ft.margin.symmetric(horizontal=10, vertical=10)
    
    self.on_changeFunction = on_change
    self.shadow = ft.BoxShadow(
      spread_radius=1,
      blur_radius=5,
      color=constants.WHITE_GRAY
    )
    
    self.animate_opacity=300
    
    with getDB() as db:
      
      if isinstance(self.item, Product):
        self.object = "Producto"
        self.maxStock = self.item.stock
      else:
        self.object = "Combo"
        self.maxStock = 0
        
      imageManager = ImageManager()

      self.image = CustomImageContainer(
        src=imageManager.getImagePath(self.item.imgPath),
        height=120,
        width=120,
      )
      
      self.nameText = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
          ft.Icon(
            name=ft.Icons.COFFEE_ROUNDED if isinstance(self.item, Product) else ft.Icons.FASTFOOD_ROUNDED,
            size=24,
            color=constants.BLACK,
          ),
          ft.Text(
            value=f"{self.object}:",
            size=18,
            color=constants.BLACK,
            weight=ft.FontWeight.W_700,
          ),
          ft.Text(
            value=f"{self.name}",
            size=18,
            color=constants.BLACK,
            overflow=ft.TextOverflow.ELLIPSIS,
          )
        ]
      )
      
      self.quantityField = CustomNumberField(
        label="",
        expand=True,
        on_change=self.customOnChange,
      )
      
      self.priceText = ft.Text(
        value=f"0.00$",
        color=constants.BLACK,
        size=18,
        overflow=ft.TextOverflow.ELLIPSIS,
      )
      
      if hasattr(self.item, "idProduct"):
        self.stockWarning = ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          controls=[
            ft.Icon(
              name=ft.Icons.INFO_OUTLINE_ROUNDED,
              color=constants.BLACK,
              size=24,
            ),
            ft.Text(
              value=f"Stock:",
              color=constants.BLACK,
              size=18,
              weight=ft.FontWeight.W_700,
              text_align=ft.TextAlign.CENTER,
              overflow=ft.TextOverflow.ELLIPSIS,
            ),
            ft.Text(
              value=f"{self.item.stock} unidades",
              color=constants.BLACK,
              size=18,
              text_align=ft.TextAlign.CENTER,
              overflow=ft.TextOverflow.ELLIPSIS,
            )
          ]
        )
      else: 
        products = getRegisterByComboId(db=db, idCombo=self.item.idCombo)
        message = f"Productos que conforman el combo \"{self.item.name}\":"
        for register in products:
          message += f"\n◆ {register.product.name} • {register.productQuantity}"
        self.productsList = ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          controls=[
            ft.Icon(
              name=ft.Icons.INFO_OUTLINE_ROUNDED,
              color=constants.BLACK,
              size=24,
            ),
            ft.Text(
              value=f"Productos",
              color=constants.BLACK,
              size=18,
              weight=ft.FontWeight.W_700,
              text_align=ft.TextAlign.CENTER,
              overflow=ft.TextOverflow.ELLIPSIS,
              tooltip=ft.Tooltip(
                message=message,
                padding=20,
                border_radius=10,
                text_style=ft.TextStyle(
                  size=20,
                  color=constants.BLACK,
                ),
                bgcolor=constants.WHITE,
                border=ft.border.all(2, constants.BLACK),
              )
            )
          ]
        )
    
    self.removeButton = CustomRemoveButton(
      on_click=lambda e: removeFunction(itemField=self) if not removeFunction == None else None,
    )
    
    self.topContent = ft.Row(
      expand=True,
      controls=[
        self.image,
        ft.Column(
          alignment=ft.MainAxisAlignment.CENTER,
          horizontal_alignment=ft.CrossAxisAlignment.START,
          expand=True,
          controls=[
            self.nameText,
            ft.Row(
              controls=[self.quantityField,]
            ),
          ]
        ),
        self.removeButton,
      ]
    )
    
    self.bottomContent = ft.Row(
      alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Row(
          controls=[
            ft.Icon(
              name=ft.Icons.ATTACH_MONEY_ROUNDED,
              size=24,
              color=constants.BLACK,
            ),
            ft.Text(
              value="Precio:",
              color=constants.BLACK,
              weight=ft.FontWeight.W_700,
              size=18,
            ),
            self.priceText
          ]
        ),
        # Here goes additional content
      ]
    )
    
    if hasattr(self, "stockWarning"):
      self.bottomContent.controls.append(self.stockWarning)
    else:
      self.bottomContent.controls.append(self.productsList)
    
    self.content = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      height=170,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      spacing=0,
      controls=[
        self.topContent,
        ft.Container(
          height=2,
          bgcolor=constants.BLACK_GRAY,
          content=ft.Row(expand=True),  
        ),
        ft.Container(
          padding=10,
          content=self.bottomContent,
        ),
      ]
    )
  
  def customOnChange(self):
    try:
      with getDB() as db:
        fieldValue = self.quantityField.fieldValue
        stock = getProductByName(db, self.name).stock if self.type == "Product" else 0
        
        # Verifica la entrada
        if int(fieldValue) > stock and self.type == "Product":
          self.quantityField.field.value = stock
          self.quantityField.fieldValue = stock
          fieldValue = self.quantityField.fieldValue
          self.quantityField.field.update()
        
        if self.sell:
          self.priceText.value = f"{round(calculatePrice(cost=self.item.cost, iva=self.item.iva, gain=self.item.gain), 2) * fieldValue}$" if self.type == "Product" else f"{round(self.item.price, 2) * fieldValue}$"
        
        else:
          self.priceText.value = f"{round(self.item.cost, 2) * fieldValue}$" if self.type == "Product" else f"{round(self.item.price, 2) * fieldValue}$"
        
        self.priceText.update()
        
        self.on_changeFunction()
    except:
      raise
  
  def animateOpacity(self):
    self.opacity = 1 if self.opacity == 0 else 0
    self.update()
    
class CustomInitialRowContent(ft.Row):
  def __init__(self, message, size=32):
    super().__init__()
    self.expand = True
    self.alignment = ft.MainAxisAlignment.CENTER
    self.vertical_alignment = ft.CrossAxisAlignment.CENTER
    
    self.controls = [
      ft.Text(
        value=message,
        size=32,
        color=constants.BLACK,
        weight=ft.FontWeight.W_700,
        text_align=ft.TextAlign.CENTER,
      )
    ]
  
class CustomRemoveButton(ft.Container):
  def __init__(self, on_click=None, height=120, width=80, icon=ft.Icons.DELETE_OUTLINE_ROUNDED, border_radius=ft.border_radius.all(10), bgcolor=constants.RED_FAILED_LIGHT, shadow:bool=True):
    super().__init__()
    self.height = height
    self.width = width
    self.animate = ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
    self.border_radius = border_radius
    self.alignment = ft.alignment.center
    # self.bgcolor = bgcolor
    
    self.on_click = on_click
    
    self.gradient = ft.LinearGradient(
      begin=ft.alignment.bottom_center,
      end=ft.alignment.top_center,
      colors=[constants.BLACK, constants.BROWN]
    )
    
    self.shadow = ft.BoxShadow(
      blur_radius=5,
      spread_radius=1,
      color=constants.WHITE_GRAY,
    )
    
    self.icon = ft.Icon(
      name=icon,
      color=constants.WHITE,
      size=32,
    )
    
    self.content = self.icon
    
class CustomCheckControl(ft.Container):
  def __init__ (self, selected:bool=False, iconColor=constants.GREEN_TEXT, Iconsize=32, iconName=ft.Icons.CHECK_CIRCLE_ROUNDED, shadow=None):
    super().__init__()
    self.selected = selected
    self.shadow = shadow
    
    self.scale = 0 if self.selected == False else 1
    self.animate_scale = ft.animation.Animation(600, ft.AnimationCurve.ELASTIC_OUT)
    
    self.border_radius = 50
    
    self.content = ft.Icon(
      name=iconName,
      size=iconSize,
      color=iconColor,
    )
    
  def selectControl(self, select=True):
    self.selected = select
    
    self.scale = 1 if self.selected else 0
    self.update()

class CustomExpansionTile(ft.ExpansionTile):
  def __init__(self, title:str, subtitle, controls:list=[]):
    super().__init__(
      title=ft.Text(
        value=title,
        color=constants.BLACK,
        size=20,
        weight=ft.FontWeight.W_600,
      ),
      subtitle=subtitle,
      controls=controls,
      affinity=ft.TileAffinity.PLATFORM,
      maintain_state=True,
    )
    
class CustomListTile(ft.ListTile):
  def __init__(self, title:str, leading, subtitle, trailing=None):
    super().__init__(
      title=ft.Text(
        value=title,
        color=constants.BLACK,
        size=20,
      ),
      leading=leading,
      subtitle=subtitle,
      trailing=trailing
    )
    
    
class CustomLowStockDialog(ft.AlertDialog):
  def __init__(self, page, products:list=[]):
    super().__init__()
    self.products = inventoryManager.checkLowStock()
    self.page = page
    self.modal = True
    self.title = ft.Text(
      value="Estado del inventario",
      size=24,
      color=constants.BLACK,
      weight=ft.FontWeight.W_500,
    )
    
    self.content = ft.Container(
      alignment=ft.alignment.center,
      height=300,
      width=500,
      border_radius=10,
      content=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER if len(self.products) == 0 else ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER if len(self.products) == 0 else ft.CrossAxisAlignment.START,
        scroll=ft.ScrollMode.ALWAYS,
        expand=True,
      )
    )
    
    if self.products == []:
      self.content.content.controls = [
        ft.Icon(
          name=ft.icons.CHECK_CIRCLE_ROUNDED,
          size=48,
          color=constants.GREEN_TEXT,
        ),
        ft.Text(
          value="El inventario está bien abastecido.",
          size=32,
          color=constants.BLACK,
          weight=ft.FontWeight.W_700,
          text_align=ft.TextAlign.CENTER
        )
      ]
    else:
      from DataBase.crud.product import getProductById
      with getDB() as db:
        imageManager = ImageManager()
        for idProduct in self.products:
          product = getProductById(db, idProduct)
          print("Product add: ", product.name)
          self.content.content.controls.append(
            ft.Container(
              padding=10,
              gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center,
                colors=[constants.ORANGE, ft.colors.WHIET38] if not product.stock < product.minStock/2 else [constants.RED_FAILED, ft.colors.WHITE38],
              ),
              border_radius=10,
              border=ft.border.all(1, constants.BLACK_GRAY),
              content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                  ft.Text(
                    value=f"{product.stock}",
                    color=constants.BLACK,
                    weight=ft.FontWeight.W_600,
                    size=20,
                  ),
                  ft.Text(
                    value=f"unidades restantes en stock de",
                    color=constants.BLACK,
                    size=20,
                  ),
                  ft.Text(
                    value=f"\"{product.name}\"",
                    color=constants.BLACK,
                    weight=ft.FontWeight.W_600,
                    size=20,
                  )
                ]
              ),
              ink=True,
              on_click=lambda e: self.viewProductInfo(product.idProduct, imageManager.getImagePath(product.imgPath))
            )
          )
    self.actions = [
      CustomTextButton(
        text="Finalizar",
        on_click=lambda e: self.page.close(self),
      )
    ]
    
  def viewProductInfo(self, idProduct:int, imgPath):
    try:
      self.page.close(self)
      
      if hasattr(self.page, "sideBar"):
        print("Done")
      #   sideBar = self.page.sideBar
      #   print(sidebar)
      #   if not sideBar.selected == sideBar.inventory:
      #     inventory = sideBar.switchPage(sideBar.inventory)
      #     inventory.showItemInfo(
      #       idItem=idProduct,
      #       imgPath=imgPath,
      #     )
      #     print("first if")
      #   else:
      #     inventory = self.page.mainContainer.content.content
      #     inventory.selectView(inventory.productButton)
      #     inventory.showItemInfo(
      #       idItem=idProduct,
      #       imgPath=imgPath
      #     )
      #     print("Second if")
    except:
      raise
      