import flet as ft
from Modules.customControls import CustomPrincipalContainer, CustomSimpleContainer, CustomOperationContainer, CustomAnimatedContainer, CustomOutlinedButton, CustomImageSelectionContainer
import constants

class ProductContainer():
  def __init__(self, page):
    pass

class ProductListContainer():
  def __init__(self, page):
    pass

class ProductForm(CustomOperationContainer):
  def __init__(self, page):
    
    self.content = ft.Column(
      
    )
    super().__init__()
  
class ProductImageSelection(CustomImageSelectionContainer):
  def __init__(self, page):
    super().__init__(page)