import flet as ft 
import constants
from Modules.customControls import CustomUserIcon, CustomOperationContainer, CustomTextField, CustomAnimatedContainer, CustomNavigationOptions, CustomFilledButton, CustomDropdown, CustomDeleteButton, CustomAlertDialog, CustomImageContainer, CustomEditButton
from config import getDB
import time
from utils.imageManager import ImageManager
from DataBase.crud.combo import createCombo, getComboById, getComboByName, getCombos, removeCombo
from Modules.Sections.InventorySection.products_components import ProductContainer
from Modules.combos_module import UpdateInfoForm

class ComboContainer(ft.Container):
  def __init__(self, page, infoContainer, mainContainer, idCombo, name, imgPath=None):
    super().__init__()
    self.name = name
    self.idCombo = idCombo
    self.imgPath = imgPath
    self.infoContainer = infoContainer
    self.mainContainer = mainContainer
    
    self.border = ft.border.all(2, constants.BLACK_INK)
    self.bgcolor = constants.WHITE
    self.border_radius = ft.border_radius.all(30)
    self.on_click = self.showComboInfo
    self.animate = ft.animation.Animation(
      300, ft.AnimationCurve.EASE
    )
    
    self.imageContainer = CustomAnimatedContainer(
      actualContent=CustomImageContainer(
        src=self.imgPath,
        width=110,
        height=110,
        border_radius=30,
      )
    )
    
    self.nameText = CustomAnimatedContainer(
      actualContent=ft.Text(
        value=self.name,
        color=constants.BLACK,
        size=20,
        weight=ft.FontWeight.W_600,
        overflow=ft.TextOverflow.ELLIPSIS,
      )
    )
    
    self.content = ft.Row(
      expand=True,
      alignment=ft.MainAxisAlignment.START,
      controls=[
        self.imageContainer,
        ft.Column(
          expand=True,
          alignment=ft.MainAxisAlignment.CENTER,
          spacing=0,
          controls=[
            self.nameText,
          ]
        )
      ]
    )
    
  def select(self):
    self.border = ft.border.all(2, constants.BLACK_GRAY)
    self.bgcolor = constants.ORANGE
    self.update()
  
  def deselect(self):
    self.border = ft.border.all(2, constants.BLACK_INK)
    self.bgcolor = constants.WHITE
    
    self.update()
    
  def showComboInfo(self, e):
    if not self.mainContainer.controlSelected == self:
      newContent = ComboInfo(
        imgPath=self.imgPath,
        idCombo=self.idCombo,
        infoContainer=self.infoContainer,
        mainContainer=self.mainContainer,
        comboContainer=self,
        page=self.page,
      )
      
      self.mainContainer.showNewInfoContent(newContent, self)
    
  def updateContainer(self, name, imgPath):
    try:
      self.name = name
      self. imgPath = imgPath
      
      self.nameText.setNewContent(
        newContent=ft.Text(
          value=self.name,
          color=constants.BLACK,
          size=20,
          weight=ft.FontWeight.W_700,
          overflow=ft.TextOverflow.ELLIPSIS,
        )
      )
      
      self.imageContainer.setNewContent(
        newContent=CustomImageContainer(
          src=self.imgPath,
          width=150,
          height=150,
          border_radius=30,
        )
      )
    except Exception as err:
      raise

class ComboInfo(ft.Stack):
  def __init__(self, page, idCombo, imgPath, comboContainer, infoContainer, mainContainer):
    super().__init__()
    self.page = page
    self.idCombo = idCombo
    self.imgPath = imgPath
    self.infoContainer = infoContainer
    self.mainContainer = mainContainer
    self.comboContainer = comboContainer
    
    self.expand = True
    
    self.imageContainer = CustomAnimatedContainer(
      actualContent=CustomImageContainer(
        src=self.imgPath,
        border_radius=30,
      )
    )
    
    with getDB() as db:
      combo = getComboById(db, idCombo=self.idCombo)
      
      self.nameText = CustomAnimatedContainer(
        actualContent=ft.Text(
          value=combo.name,
          size=28,
          color=constants.BLACK,
          weight=ft.FontWeight.W_700,
          text_align=ft.TextAlign.CENTER,
        )
      )
      
      self.productsList = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        scroll=ft.ScrollMode.ALWAYS,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[container for container in self.getProductsContainers()]
      )
      
      self.priceText = CustomAnimatedContainer(
        actualContent=ft.Text(
          value=f"Precio: {round(combo.price, 2)}$",
          size=20,
          color=constants.BLACK,
          weight=ft.FontWeight.W_600,
        )
      )
      
      self.priceContainer = ft.Container(
        border_radius=ft.border_radius.all(20),
        width=200,
        border=ft.border.all(2, constants.BLACK),
        padding=ft.padding.symmetric(vertical=10, horizontal=20),
        alignment=ft.alignment.center,
        content=self.priceText,
        ink=True,
        ink_color=constants.WHITE_GRAY,
        on_click=None,
      )
    
    self.deleteButton = CustomDeleteButton(
      function=self.deleteCombo,
      page=self.page,
    )
    
    self.editButton = CustomEditButton(
      function=self.showEditInfo,
    )
    
    self.info = ft.Stack(
      expand=True,
      controls=[
        ft.Row(
          expand=True,
          alignment=ft.MainAxisAlignment.CENTER,
          vertical_alignment=ft.CrossAxisAlignment.CENTER,
          spacing=10,
          controls=[
            ft.Column(
              expand=2,
              alignment=ft.MainAxisAlignment.CENTER,
              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
              controls=[
                self.nameText,
                self.imageContainer,
                self.priceText,
              ]
            ),
            ft.Column(
              expand=3,
              alignment=ft.MainAxisAlignment.CENTER,
              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
              controls=[
                ft.Row(
                  alignment=ft.MainAxisAlignment.START,
                  vertical_alignment=ft.CrossAxisAlignment.CENTER,
                  controls=[
                    ft.Icon(
                      name=ft.icons.COFFEE_ROUNDED,
                      color=constants.BLACK, 
                      size=28, 
                    ),
                    ft.Text(
                      value=f"Productos:",
                      size=24,
                      weight=ft.FontWeight.W_600,
                      color=constants.BLACK,
                      
                    )
                  ]  
                ),
                ft.Container(
                  border=ft.border.all(2, constants.WHITE_GRAY),
                  border_radius=20,
                  margin=ft.margin.symmetric(vertical=10),
                  expand=True,
                  padding=10,
                  content=ft.Row(
                    expand=True,
                    controls=[self.productsList]
                  ),
                ),
                
              ]
            ),
          ]
        ),
        ft.Container(
          content=self.deleteButton,
          right=10,
          top=0,
        ),
        ft.Container(
          content=self.editButton,
          right=80,
          top=0,
        )
      ]
    )
    
    self.animatedSwitcher = CustomAnimatedContainer(
      actualContent=self.info,
    )
    
    self.controls = [self.animatedSwitcher]
    
  def getProductsContainers(self):
    try:
      containers = []
      with getDB() as db:
        combo = getComboById(db, idCombo=self.idCombo)
        
        for register in combo.products:
          imageManager = ImageManager()
          productContainer = ProductContainer(
            idProduct=register.product.idProduct,
            name=register.product.name,
            description=f"{register.productQuantity} unidades.",
            infoContainer=self.infoContainer,
            page=self.page,
            mainContainer=self.mainContainer,
            imgPath=imageManager.getImagePath(register.product.imgPath),
          )
          
          productContainer.on_click = None
          containers.append(productContainer)
      return containers
    except Exception as err:
      raise
  
  def deleteCombo(self):
    try:
      with getDB() as db:
        combo = getComboById(db, self.idCombo)
        
        if removeCombo(db, combo):
          self.mainContainer.resetCurrentView()
    except Exception as err:
      raise
  
  def showEditInfo(self, e):
    try:
      newContent = UpdateInfoForm(
        page=self.page,
        idCombo=self.idCombo,
        mainContainer=self.mainContainer,
        comboInfoControl=self,
      )
      
      self.animatedSwitcher.setNewContent(newContent)
    except Exception as err:
      print(err)

  def returnToInfo(self):
    try:
      self.animatedSwitcher.setNewContent(self.info)
    except Exception as err:
      print(err)
  
  def updateInfoControls(self):
    try:
      self.returnToInfo()
      time.sleep(0.5)
      with getDB() as db:
        combo = getComboById(db, self.idCombo)
        imageManager = ImageManager()
        
        if combo:
          self.nameText.setNewContent(
            newContent=ft.Text(
              value=combo.name,
              size=32,
              color=constants.BLACK,
              weight=ft.FontWeight.W_700,
              text_align=ft.TextAlign.CENTER,
            )
          )
          
          self.priceText.setNewContent(
            newContent=ft.Text(
              value=f"Precio: {round(combo.price, 2)}$",
              size=20,
              color=constants.BLACK,
              weight=ft.FontWeight.W_700,
            )
          )
          self.imgPath = imageManager.getImagePath(combo.imgPath)
          self.imageContainer.setNewContent(
            newContent=CustomImageContainer(
              src=self.imgPath,
              border_radius=30,
            )
          )
          self.comboContainer.updateContainer(name=combo.name, imgPath=self.imgPath)
    except Exception as err:
      raise