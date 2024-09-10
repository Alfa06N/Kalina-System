import flet as ft
import constants
from Modules.customControls import CustomAnimatedContainerSwitcher, CustomNavigationOptions, CustomAnimatedContainer, CustomFloatingActionButton
from Modules.Sections.InventorySection.products_components import ProductInfo
from Modules.Sections.InventorySection.combos_components import ComboInfo
from Modules.Sections.InventorySection.categories_components import CategoryInfo, CategoryContainer
from Modules.categories_modules import CategoryForm
import time
from DataBase.crud.category import getCategories
from config import getDB
from utils.imageManager import ImageManager

class Inventory(ft.Stack):
  def __init__(self, page):
    super().__init__()
    self.expand = True
    self.page = page
    
    self.categoryButton = CustomNavigationOptions(
      icon=ft.icons.CATEGORY_ROUNDED,
      text="Categorías",
      function=self.selectView,
      color="#666666",
      focusedColor=constants.BLACK,
      opacityInitial=1,
      highlightColor=None,
      contentAlignment=ft.MainAxisAlignment.CENTER,
    )
    
    self.productButton = CustomNavigationOptions(
      icon=ft.icons.COFFEE_ROUNDED,
      text="Productos",
      function=self.selectView,
      color="#666666",
      focusedColor=constants.BLACK,
      opacityInitial=1,
      highlightColor=None,
      contentAlignment=ft.MainAxisAlignment.CENTER,
      default=True,
    )
    
    self.comboButton = CustomNavigationOptions(
      icon=ft.icons.FASTFOOD_ROUNDED, #
      text="Combos",
      function=self.selectView, #
      color="#666666",
      focusedColor=constants.BLACK,
      opacityInitial=1,
      highlightColor=None,
      contentAlignment=ft.MainAxisAlignment.CENTER,
    )
    
    self.topNavigationBar = ft.Container(
      margin=ft.margin.symmetric(horizontal=20, vertical=10),
      bgcolor=ft.colors.TRANSPARENT,
      height=60,
      width=600,
      content=ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        spacing=20,
        controls=[
          self.categoryButton,
          self.productButton, 
          self.comboButton,
        ]
      )
    )
    
    self.itemsContainer = ft.Container(
      col={"sm": 12, "md": 9, "xl": 6},
      margin=ft.margin.symmetric(horizontal=20, vertical=20),
      # height=800,
      expand=True,
      alignment=ft.alignment.top_left,
      border_radius=ft.border_radius.all(30),
      bgcolor=constants.WHITE,
      shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=5,
        color=constants.BLACK_GRAY,
      ),
      content=CustomAnimatedContainer(
        actualContent=ft.Column(
          alignment=ft.MainAxisAlignment.CENTER,
          # height=800,
          expand=True,
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
      )
    )
    
    self.itemsContainer = CustomAnimatedContainerSwitcher(
      shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=5,
        color=constants.BLACK_INK,
      ),
      content=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      ),
      height=600,
      width=700,
      col={"sm": 12, "md": 9, "xl": 6},
    )
    
    self.categoryInitialContent = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      expand=True,
      controls=[
        ft.Text(
          value="Selecciona una categoría para ver más información",
          color=constants.BLACK,
          size=32,
          weight=ft.FontWeight.W_700,
          text_align=ft.TextAlign.CENTER,
        )
      ]
    )
    
    self.productInitialContent = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      expand=True,
      controls=[
        ft.Text(
          value="Selecciona un producto para ver más información",
          color=constants.BLACK,
          size=32,
          weight=ft.FontWeight.W_700,
          text_align=ft.TextAlign.CENTER,
        )
      ]
    )
    
    self.comboInitialContent = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      expand=True,
      controls=[
        ft.Text(
          value="Selecciona un combo para ver más información",
          color=constants.BLACK,
          size=32,
          weight=ft.FontWeight.W_700,
          text_align=ft.TextAlign.CENTER,
        )
      ]
    )
    
    self.infoContainer = CustomAnimatedContainerSwitcher(
      content=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          self.productInitialContent
        ]  
      ),
      col={"sm": 12, "md": 9, "xl": 6}
    )
    
    self.addItemButton = CustomFloatingActionButton(on_click=self.addItemForm)

    self.selected = self.productButton
    
    self.controls = [
      ft.Column(
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          self.topNavigationBar,
          ft.ResponsiveRow(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            run_spacing=10,
            controls=[
              self.itemsContainer,
              self.infoContainer,
            ]
          ),
        ]
      ),
      ft.Container(
        content=self.addItemButton,
        right=10,
        bottom=10,
      )
    ]
    
  def selectView(self, e):
    if not self.selected == e.control:
      self.selected.deselectOption()
      self.selected = e.control
      self.selected.selectOption()
      
      self.resetCurrentView()
  
  def resetInfoContainer(self):
    if not self.infoContainer.height == 150:
      self.infoContainer.changeStyle(height=150, width=300, shadow=None)
    self.showViewSelected()
      
  def showViewSelected(self):
    if self.selected == self.categoryButton:
      self.infoContainer.setNewContent(self.categoryInitialContent)
    elif self.selected == self.productButton:
      self.infoContainer.setNewContent(self.productInitialContent)
    elif self.selected == self.comboButton:
      self.infoContainer.setNewContent(self.comboInitialContent)
    
  def addItemForm(self, e):
    self.newContent = None
    if self.selected == self.categoryButton:
      self.newContent = CategoryForm(self.page, self)
    elif self.selected == self.productButton:
      pass
    elif self.selected == self.comboButton:
      pass
      
    if not self.infoContainer.height == 800:
      self.infoContainer.changeStyle(height=800, width=700, shadow=ft.BoxShadow(
        blur_radius=5,
        spread_radius=1,
        color=constants.BLACK_GRAY,
      ))
    if self.newContent:
      self.infoContainer.setNewContent(self.newContent)
      
  def editItemForm(self, newContent):
    self.infoContainer.changeStyle(
      height=800,
      width=700,
      shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=5,
        color=constants.BLACK_GRAY,
      )
    )
    self.infoContainer.setNewContent(newContent)

  
  def fillItemsContainer(self):
    items = []
    
    if self.selected == self.categoryButton:
      items = self.getCategoriesToFill()
    elif self.selected == self.productButton:
      pass
    elif self.selected == self.comboButton:
      pass
    
    newContent = ft.Column(
      scroll=ft.ScrollMode.AUTO,
      alignment=ft.MainAxisAlignment.CENTER,
      expand=True,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
      
    if len(items) == 0:
      newContent.controls = [
        ft.Text(
          value="No hay contenido que mostrar",
          size=32,
          color=constants.BLACK,
          weight=ft.FontWeight.W_700,
          text_align=ft.TextAlign.CENTER,
        )
      ]
    else:
      for item in items:
        newContent.controls.append(item)
    
    self.itemsContainer.setNewContent(newContent)
  
  def getCategoriesToFill(self):
    try:
      with getDB() as db:
        categories = getCategories(db)
        containers = []
        imageManager = ImageManager()
        if categories:
          for category in categories:
            container = CategoryContainer(
              idCategory=category.idCategory,
              name=category.name,
              description=category.description,
              imgPath=imageManager.getImagePath(category.imgPath),
              infoContainer=self.infoContainer,
              mainContainer=self
            )
            
            containers.append(container)
          return containers
    except Exception as err:
      print(err)
  
  def resetCurrentView(self):
    self.resetInfoContainer()
    self.fillItemsContainer()