import flet as ft
import constants
from Modules.customControls import CustomAlertDialog, CustomAnimatedContainer, CustomAnimatedContainerSwitcher, CustomOperationContainer, CustomTextField, CustomDropdown, CustomImageContainer, CustomFloatingActionButton, CustomFilledButton, CustomTooltip

class Sales(ft.Row):
  def __init__(self, page):
    super().__init__()
    self.expand = True
    self.page = page
    self.alignment = ft.MainAxisAlignment.CENTER
    self.vertical_alignment = ft.CrossAxisAlignment.CENTER
    
    self.principalContainer = CustomAnimatedContainerSwitcher(
      content=ft.Text(
        value="There's nothing to show you in Sales",
        size=42,
        color=constants.BLACK,
        weight=ft.FontWeight.BOLD,
      ),
      shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=5,
        color=constants.WHITE_GRAY,
      ),
      expand=True,
      height=None,
      width=None
    )
    
    self.controls = [
      self.principalContainer,
    ]