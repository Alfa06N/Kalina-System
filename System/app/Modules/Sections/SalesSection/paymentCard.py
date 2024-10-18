import flet as ft
import constants
from Modules.customControls import CustomAlertDialog, CustomAnimatedContainer, CustomAnimatedContainerSwitcher, CustomOperationContainer, CustomTextField, CustomDropdown, CustomImageContainer, CustomFloatingActionButton, CustomFilledButton, CustomTooltip

class PaymentCard(ft.Container):
  def __init__(self, page, formContainer, height=140, width=140):
    super().__init__()
    self.page = page
    self.height = height
    self.width = width
    self.formContainer = formContainer
    
    self.bgcolor = constants.WHITE
    self.border = ft.border.all(2, constants.BLACK_GRAY)
    self.border_radius = 20
    self.padding = ft.padding.all(10)
    self.ink = True
    self.ink_color = constants.WHITE_GRAY
    self.on_click = lambda e: self.clickFunction()
    
    self.selectedPayments = []
    
    self.withoutPayment = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Icon(
          name=ft.icons.ADD_CARD_ROUNDED,
          size=32,
          color=constants.BLACK,
        ),
        ft.Text(
          value="Pagos",
          size=18,
          color=constants.BLACK,
          text_align=ft.TextAlign.CENTER,
          overflow=ft.TextOverflow.ELLIPSIS,
        )
      ]
    )
    
    self.content = self.withoutPayment
    
  def clickFunction(self):
    try:
      pass
    except:
      pass