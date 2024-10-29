import flet as ft
import constants
from Modules.customControls import CustomAlertDialog, CustomAnimatedContainer, CustomAnimatedContainerSwitcher, CustomOperationContainer, CustomTextField, CustomDropdown, CustomImageContainer, CustomFloatingActionButton, CustomFilledButton, CustomTooltip, CustomNavigationOptions
from Modules.Sections.SalesSection.components import SaleItemsList, SaleForm
from utils.saleManager import saleMakerManager

class SaleHistory(ft.Row):
  def __init__(self):
    super().__init__()
    self.expand = True
    self.alignment = ft.MainAxisAlignment.CENTER
    self.vertical_alignment = ft.CrossAxisAlignment.CENTER
    
    self.controls = [
      ft.Text(
        value="Historial de Ventas",
        size=42,
        color=constants.BLACK,
        weight=ft.FontWeight.W_700,
        text_align=ft.TextAlign.CENTER,
      )
    ]