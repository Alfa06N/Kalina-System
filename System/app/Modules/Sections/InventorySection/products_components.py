import flet as ft 
import constants
from Modules.customControls import CustomUserIcon, CustomOperationContainer, CustomTextField, CustomAnimatedContainer, CustomNavigationOptions, CustomFilledButton, CustomDropdown, CustomDeleteButton, CustomAlertDialog, CustomImageContainer, CustomEditButton
from config import getDB
from DataBase.crud.product import getProducts, getProductById, updateProduct, updateProductStock, removeProduct, calculatePrice
from Modules.products_module import UpdateStockForm, UpdateInfoForm
from utils.imageManager import ImageManager

class ProductContainer(ft.Container):
  def __init__(self, idProduct, name, description, infoContainer, mainContainer, page, imgPath=None):
    super().__init__()
    # super().__init__(col={"xl": 6, "xxl": 6})
    self.name = name 
    self.idProduct = idProduct
    self.description = description
    self.imgPath = imgPath
    self.infoContainer = infoContainer
    self.mainContainer = mainContainer
    
    self.bgcolor = ft.colors.TRANSPARENT
    self.border_radius = ft.border_radius.all(30)
    self.ink = True
    self.ink_color = constants.WHITE_GRAY
    self.on_click = self.showProductInfo
    
    self.imageContainer = CustomAnimatedContainer(
      actualContent=CustomImageContainer(
        src=self.imgPath,
        width=150,
        height=150,
        border_radius=30,
      )
    )
    
    self.nameText = CustomAnimatedContainer(
      actualContent=ft.Text(
        value=self.name,
        color=constants.BLACK,
        size=18,
        weight=ft.FontWeight.W_700,
        overflow=ft.TextOverflow.ELLIPSIS,
      )
    )
    
    self.descriptionText = CustomAnimatedContainer(
      actualContent=ft.Text(
        value=self.description,
        color=constants.BLACK,
        size=18,
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
            self.descriptionText,
          ]
        )
      ]
    )
    
  def showProductInfo(self, e):
    newContent = ProductInfo(
      imgPath=self.imgPath,
      idProduct=self.idProduct,
      infoContainer=self.infoContainer,
      mainContainer=self.mainContainer,
      productContainer=self,
      page=self.page,
    )
    
    if not self.infoContainer.height == 600:
      self.infoContainer.changeStyle(height=600, width=700, shadow=ft.BoxShadow(
        blur_radius=5,
        spread_radius=1,
        color=constants.BLACK_GRAY,
      ))
    self.infoContainer.setNewContent(newContent)
  
  def updateContainer(self, name, description, imgPath):
    try:
      self.name = name
      self.description = description
      self.imgPath = imgPath
      
      self.nameText.setNewContent(
        newContent=ft.Text(
          value=self.name,
          color=constants.BLACK,
          size=18,
          weight=ft.FontWeight.W_700,
          overflow=ft.TextOverflow.ELLIPSIS,
        )
      )
      
      self.descriptionText.setNewContent(
        newContent=ft.Text(
          value=self.description,
          color=constants.BLACK,
          size=18,
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
      print(err)

class ProductInfo(ft.Stack):
  def __init__(self, page, idProduct, imgPath, productContainer, infoContainer, mainContainer):
    super().__init__()
    self.page = page
    self.idProduct = idProduct
    self.imgPath = imgPath
    self.infoContainer = infoContainer
    self.mainContainer = mainContainer
    self.productContainer = productContainer
    
    self.expand = True
    
    self.imageContainer = CustomAnimatedContainer(
      actualContent=CustomImageContainer(
        src=self.imgPath,
        border_radius=10,
      )
    )
    
    with getDB() as db:
      product = getProductById(db, idProduct=self.idProduct)
    
      self.nameText = CustomAnimatedContainer(
        actualContent=ft.Text(
          value=product.name,
          size=32,
          color=constants.BLACK,
          weight=ft.FontWeight.W_700,
        )
      )
      
      self.descriptionText = CustomAnimatedContainer(
        actualContent=ft.Text(
          value=product.description if not product.description == "" else "Sin descripción",
          size=18,
          color=constants.BLACK,
          max_lines=2,
          overflow=ft.TextOverflow.ELLIPSIS,
        )
      )
      
      self.stockText = ft.Text(
        value=f"Stock: {product.stock}",
        size=18,
        color=constants.BLACK,
        weight=ft.FontWeight.W_700,
      )
      
      self.stockContainer = ft.Container(
        border_radius=ft.border_radius.all(20),
        width=200,
        border=ft.border.all(2, constants.BLACK),
        padding=ft.padding.symmetric(vertical=10, horizontal=20),
        alignment=ft.alignment.center,
        content=self.stockText,
        ink=True,
        ink_color=constants.WHITE_GRAY,
        on_click=self.showEditStock
      )
      
      self.minStockText = ft.Text(
        value=f"Se enviará una notificación cuando el stock sea menor o igual a {product.minStock}",
        size=18,
        color=constants.BLACK,
        text_align=ft.TextAlign.CENTER,
      )
      
      self.costText = ft.Text(
        value=f"Costo: {round(product.cost)}$",
        size=18,
        color=constants.BLACK
      )
      
      self.ivaText = ft.Text(
        value=f"IVA: {round(product.cost * (product.iva/100), 2)}$",
        size=18,
        color=constants.BLACK,
      )
      
      self.priceText = ft.Text(
        value=f"Precio final: {round(calculatePrice(product.cost, product.iva, product.gain), 2)}$",
        color=constants.BLACK,
        size=18,
        weight=ft.FontWeight.W_700,
      )
      
      self.gainText = ft.Text(
        value=f"Ganancia: {round(product.cost * (product.gain / 100), 2)}$",
        color=constants.BLACK,
        size=18,
      )
      
      self.categoryText = ft.Text(
        value=f"{product.category.name}",
        size=18,
        color=constants.BLACK,
        weight=ft.FontWeight.W_700,
      )
    
    self.deleteButton = CustomDeleteButton(
      function=None,
      page=self.page,
    )
    
    self.editButton = CustomEditButton(
      function=self.showEditInfo
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
                self.stockContainer,
                self.descriptionText,
              ]
            ),
            ft.Column(
              expand=3,
              alignment=ft.MainAxisAlignment.CENTER,
              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
              controls=[
                ft.Row(
                  alignment=ft.MainAxisAlignment.CENTER,
                  controls=[
                    ft.Text(
                      value="Categoría:",
                      size=18,
                      color=constants.BLACK,
                    ),
                    self.categoryText,
                  ]
                  
                ),
                ft.Container(
                  border=ft.border.all(2, constants.BLACK),
                  alignment=ft.alignment.center_left,
                  border_radius=ft.border_radius.all(20),
                  height=200,
                  width=600,
                  padding=ft.padding.all(20),
                  content=ft.Column(
                    controls=[
                      self.costText,
                      self.ivaText,
                      self.gainText,
                      ft.Divider(color=constants.BLACK),
                      self.priceText,
                    ]
                  )
                ),
                ft.Container(
                  padding=ft.padding.all(5),
                  content=self.minStockText,
                )
              ]
            )
          ]
        ),
        ft.Container(
          content=self.deleteButton,
          right=10,
          top=10,
        ),
        ft.Container(
          content=self.editButton,
          right=80,
          top=10,
        )
      ]
    )
    
    self.animatedSwitcher = CustomAnimatedContainer(
      actualContent=self.info,
    )
    
    self.controls = [self.animatedSwitcher]
  
  def updateInfoControls(self, info:bool=False, stock:bool=False, prices:bool=False):
    try:
      self.returnToInfo()
      with getDB() as db:
        product = getProductById(db, self.idProduct)
        imageManager = ImageManager()
        
        if info:
          self.nameText.setNewContent(
            newContent=ft.Text(
              value=product.name,
              size=32,
              color=constants.BLACK,
              weight=ft.FontWeight.W_700,
            )
          )
          
          self.categoryText.value = product.category.name
          
          self.descriptionText.setNewContent(
            newContent=ft.Text(
              value=product.description if not product.description == "" else "Sin descripción",
              size=18,
              color=constants.BLACK,
              max_lines=2,
              overflow=ft.TextOverflow.ELLIPSIS,
            )
          )
            
          self.imgPath = imageManager.getImagePath(product.imgPath)
          self.imageContainer.setNewContent(
            newContent=CustomImageContainer(
              src=self.imgPath,
              border_radius=10,
            )
          )
          self.productContainer.updateContainer(name=product.name, description=product.description, imgPath=self.imgPath)

        if stock:
          self.stockText.value = f"Stock: {product.stock}"
          self.minStockText.value = f"Se enviará una notificación cuando el stock sea menor o igual a {product.minStock}"
        
        if prices:
          self.costText.value = f"Costo: {round(product.cost)}$"
          self.ivaText.value = f"IVA: {round(product.cost * (product.iva / 100), 2)}$"
          self.gainText.value = f"Ganancia: {round(product.cost * (product.gain / 100), 2)}$"
          self.priceText.value = f"Precio final: {round(calculatePrice(product.cost, product.iva, product.gain), 2)}$"
        
    except Exception as err:
      print(err)

  def showEditStock(self, e):
    try:
      newContent = UpdateStockForm(
        idProduct=self.idProduct,
        mainContainer=self.mainContainer,
        productInfoControl=self,
        page=self.page,
      )
      
      self.animatedSwitcher.setNewContent(newContent)
    except Exception as err:
      print(err)
  
  def showEditInfo(self, e):
    try:
      newContent = UpdateInfoForm(
        page=self.page,
        idProduct=self.idProduct,
        mainContainer=self.mainContainer,
        productInfoControl=self,
      )
      
      self.animatedSwitcher.setNewContent(newContent)
    except Exception as err:
      print(err)
    
  def returnToInfo(self):
    try:
      self.animatedSwitcher.setNewContent(
        self.info
      )
    except Exception as err:
      print(err)