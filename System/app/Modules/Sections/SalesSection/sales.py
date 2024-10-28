import flet as ft
import constants
from Modules.customControls import CustomAlertDialog, CustomAnimatedContainer, CustomAnimatedContainerSwitcher, CustomOperationContainer, CustomTextField, CustomDropdown, CustomImageContainer, CustomFloatingActionButton, CustomFilledButton, CustomTooltip
from Modules.Sections.SalesSection.components import SaleItemsList, SaleForm
from utils.saleManager import saleMakerManager

class Sales(ft.Row):
  def __init__(self, page):
    super().__init__()
    self.expand = True
    self.page = page
    self.alignment = ft.MainAxisAlignment.CENTER
    self.vertical_alignment = ft.CrossAxisAlignment.CENTER
    
    self.itemsList = SaleItemsList(
      page=self.page,
    )
    
    self.saleForm = SaleForm(
      page=self.page,
    )
    
    # Reference to priceCard from saleForm to itemsList:
    self.itemsList.itemsSelector.priceCard = self.saleForm.priceCard
    
    self.contentRow = ft.Row(
      expand=True,
      controls=[
        self.itemsList,
        self.saleForm
      ]
    )
    
    self.mainContainer = CustomAnimatedContainerSwitcher(
      content=self.contentRow,
      shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=5,
        color=constants.WHITE_GRAY,
      ),
      padding=None,
      expand=True,
      height=None,
      width=None
    )
    
    self.controls = [
      self.mainContainer,
    ]
    
    saleMakerManager.setSaleContainer(self.mainContainer)