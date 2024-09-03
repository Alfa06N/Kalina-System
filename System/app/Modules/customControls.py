import flet as ft
import constants 
import time
from validation import validateCI, validateEmptyField, validatePassword, validateUsername
from datetime import datetime

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
      blur_radius = 20,
      color = "#444444"
    ) 
      
  def updateContent(self, newContent):
    self.animatedContainer.content = newContent
    self.animatedContainer.update()
    
class CustomSimpleContainer(ft.Container):
  def __init__(self, gradient=False, height=550, width=450):
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
  def __init__(self, content, height:int=150, width:int=300, padding=ft.padding.all(20), margin=ft.margin.all(20), border_radius=ft.border_radius.all(30), bgcolor=constants.WHITE, shadow=None, alignment=ft.alignment.center, duration:int=300, animationCurve=ft.AnimationCurve.EASE_IN_OUT, col=None):
    super().__init__(col=col)
    # self.col = None
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
    
  def changeStyle(self, height, width, shadow=None, bgcolor=constants.WHITE):
    self.height = height
    self.width = width
    self.shadow = shadow
    self.bgcolor = bgcolor
    self.update()
  

class CustomFilledButton(ft.FilledButton):
  def __init__(self, text, overlay=constants.BROWN_OVERLAY, bgcolor=constants.BROWN, color=constants.WHITE, size=18, clickFunction=None):
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

class CustomFloatingActionButton(ft.FloatingActionButton):
  def __init__(self, icon=ft.icons.ADD, height:int=70, width:int=70, bgcolor=constants.BROWN, color=constants.WHITE, on_click=None):
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
  def __init__(self, label, field, revealPassword=False,  mode="light",  hint_text=None,  expand=False, submitFunction=None, disabled:bool=False):
    super().__init__()
    self.label = label
    self.border_width = 2
    self.expand = expand
    self.on_submit = submitFunction
    self.disabled = disabled
    
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
    
    if field == "username":
      self.on_change = lambda e: validateUsername(self)
      
    elif field == "password":
      self.password = True
      self.can_reveal_password = revealPassword
      self.on_change = lambda e: validatePassword(self)
    
    elif field == "ci":
      self.prefix_text = "V-"
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
      self.border = ft.border.all(2, constants.WHITE_GRAY)
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
    self.title = ft.Text(title, color=constants.BLACK, weight=ft.FontWeight.BOLD, size=32)
    self.toolbar_height = 70
    self.center_title = True
    self.surface_tint_color = constants.BLACK
    self.elevation = 2
    self.shadow_color = constants.WHITE_GRAY
    self.bgcolor = constants.WHITE
    self.actions = [
      ft.PopupMenuButton(
        icon_color=constants.BLACK,
        padding=ft.padding.all(12),
        items=[
          ft.PopupMenuItem(icon=ft.icons.SETTINGS_ROUNDED, text="Configuración"),
          ft.PopupMenuItem(),
          ft.PopupMenuItem(icon=ft.icons.LOGOUT_OUTLINED, text="Cerrar sesión", on_click=self.openLogoutDialog)
        ]
      )
    ]
  
  def openLogoutDialog(self, e):
    self.dialog = CustomAlertDialog(
      modal=True,
      title="¿Deseas cerrar sesión?",
      content="",
      actions=[
        ft.TextButton("Sí", on_click=self.logout),
        ft.TextButton("No", on_click=lambda e: self.page.close(self.dialog))
      ]
    )
    self.page.open(self.dialog)
    
  def logout(self, e):
    self.page.close(self.dialog)
    self.page.controls.clear()
    from interface import initApp
    initApp(self.page)
    
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
      icon=ft.icons.ARROW_RIGHT,
      # icon_color=constants.WHITE,
      selected_icon=ft.icons.ARROW_LEFT,
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
    
    self.home = CustomNavigationOptions(icon=ft.icons.HOME_WORK_ROUNDED, text="Inicio", function=self.selectOne, default=True)
    self.sales = CustomNavigationOptions(icon=ft.icons.SELL_ROUNDED, text="Ventas", function=self.selectOne)
    self.payments = CustomNavigationOptions(icon=ft.icons.WALLET_ROUNDED, text="Pagos", function=self.selectOne)
    self.users = CustomNavigationOptions(icon=ft.icons.SECURITY_ROUNDED, text="Usuarios", function=self.selectOne)
    self.clients = CustomNavigationOptions(icon=ft.icons.PEOPLE_ROUNDED, text="Clientes", function=self.selectOne)
    self.employees = CustomNavigationOptions(icon=ft.icons.WORK_ROUNDED, text="Empleados", function=self.selectOne)
    self.closings = CustomNavigationOptions(icon=ft.icons.MONEY_ROUNDED, text="Cierres", function=self.selectOne)
    self.statistics = CustomNavigationOptions(icon=ft.icons.SSID_CHART_ROUNDED, text="Estadísticas", function=self.selectOne)
    self.inventory = CustomNavigationOptions(icon=ft.icons.INVENTORY_2_ROUNDED, text="Inventario", function=self.selectOne)
    
    
    self.navigationOptions = [
      self.home,
      self.users,
      self.clients,
      self.employees,
      self.sales,
      self.inventory,
      self.payments,
      self.closings,
      self.statistics
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
            ft.Row([self.home]),
            ft.Row([self.users]),
            ft.Row([self.clients]),
            ft.Row([self.employees]),
            ft.Row([self.sales]),
            ft.Row([self.inventory]),
            ft.Row([self.payments]),
            ft.Row([self.closings]),
            ft.Row([self.statistics])
          ]
        ),
      ]
    )
    self.selected = self.home
  
  def toggleIconButton(self, e):
    self.openButton.selected = not e.control.selected
    self.openContainer()
    self.openButton.update()
    
  def switchPage(self, pageName):
    if pageName == "Home":
      self.updateMainContent(Home(self.page))
      self.switchButton(self.home)
    elif pageName == "Users":
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
    elif pageName == "Statistics":
      self.updateMainContent(Statistics(self.page))
      self.switchButton(self.statistics)
      
  def switchButton(self, newSelected):
    self.selected.deselectOption()
    self.selected = newSelected
    self.selected.selectOption()
  
  def selectOne(self, e):
    if not self.selected == e.control:
      self.switchButton(e.control)
      
      if e.control == self.home:
        from Modules.Sections.HomeSection.home import Home
        self.updateMainContent(Home(self.page))
      elif e.control == self.users:
        from Modules.Sections.UsersSection.users import Users
        self.updateMainContent(Users(self.page))  
      elif e.control == self.clients:
        from Modules.Sections.ClientsSection.clients import Clients
        self.updateMainContent(Clients(self.page))
      elif e.control == self.employees:
        from Modules.Sections.EmployeesSection.employees import Employees
        self.updateMainContent(Employees(self.page))
      elif e.control == self.sales:
        from Modules.Sections.SalesSection.sales import Sales
        self.updateMainContent(Sales(self.page))
      elif e.control == self.inventory:
        from Modules.Sections.InventorySection.inventory import Inventory
        self.updateMainContent(Inventory(self.page))
      elif e.control == self.payments:
        from Modules.Sections.PaymentsSection.payments import Payments 
        self.updateMainContent(Payments(self.page))
      elif e.control == self.closings:
        from Modules.Sections.ClosingsSection.closings import Closings
        self.updateMainContent(Closings(self.page))
      elif e.control == self.statistics:
        from Modules.Sections.StatisticsSection.statistics import Statistics
        self.updateMainContent(Statistics(self.page))
    
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
  def __init__(self, icon, text, function, color = constants.WHITE, highlightColor="white10", inkColor="#666666", focusedColor = constants.ORANGE_OVERLAY, contentAlignment=ft.MainAxisAlignment.START, opacityInitial:int=0, default:bool=False):
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
      self.optionText = ft.Text(value=text, color=self.color, size=18, animate_opacity=300, opacity=opacityInitial)
    else:
      self.optionIcon = ft.Icon(name=icon, color=self.focusedColor, size=24,)
      self.optionText = ft.Text(value=text, color=self.focusedColor, size=18, animate_opacity=300, opacity=opacityInitial)
    
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
    self.update()
    
  def deselectOption(self):
    self.optionIcon.color = self.color
    self.optionText.color = self.color
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
    
class CustomAlertDialog(ft.AlertDialog):
  def __init__(self, title, content, modal:bool=True, actions: list = []):
    super().__init__()
    self.title = ft.Text(title)
    self.content = ft.Text(content)
    self.actions = actions
    self.actions_alignment = ft.MainAxisAlignment.END,
    self.modal = modal   
    
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
      name=ft.icons.DELETE_ROUNDED,
      color=self.color,
      size=self.size
    )
    
    self.on_click = self.showWarningDialog if not self.function == None else None
    
  def showWarningDialog(self, e):
    self.newDialog = CustomAlertDialog(
      title="¿Estás seguro de llevar a cabo esta acción?",
      content="Los datos se eliminarán permanentemente",
      actions=[
        ft.TextButton("Eliminar", on_click=self.executeFunction),
        ft.TextButton("Cancelar", on_click=self.closeDialog)
      ]
    )
    self.page.open(self.newDialog)
  
  def executeFunction(self, e):
    self.page.close(self.newDialog)
    self.function()
    
  def closeDialog(self, e):
    self.page.close(self.newDialog)