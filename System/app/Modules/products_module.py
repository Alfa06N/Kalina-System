import flet as ft
from Modules.customControls import CustomPrincipalContainer, CustomSimpleContainer, CustomOperationContainer, CustomAnimatedContainer, CustomOutlinedButton, CustomImageSelectionContainer, CustomNumberField, CustomTooltip, CustomFilledButton, CustomTextField, CustomAutoComplete, CustomDropdown, CustomAlertDialog, CustomReturnButton
import constants
from config import getDB
from validation import evaluateForm
from DataBase.crud.product import createProduct, getProductByName, getProductById, calculatePrice, updateProductStock, updateProductInfo, updateProductPrices
from DataBase.crud.category import getCategories, getCategoryByName
import time
from utils.imageManager import ImageManager
from exceptions import DataAlreadyExists
from utils.sessionManager import getCurrentUser

class ProductContainer():
  def __init__(self, page):
    pass

class ProductListContainer():
  def __init__(self, page):
    pass

class ProductForm(CustomOperationContainer):
  def __init__(self, page, mainContainer):
    self.page = page
    self.mainContainer = mainContainer
    
    self.title = ft.Row(
      alignment=ft.MainAxisAlignment.CENTER,
      controls=[
        ft.Text(
          value="Nuevo Producto",
          size=42,
          color=constants.BLACK,
          weight=ft.FontWeight.W_700,
          text_align=ft.TextAlign.CENTER,
        )
      ]
    )
    
    self.nameField = CustomTextField(
      label="Nombre",
      field="others",
      submitFunction=None,
      expand=True,
    )
    
    self.descriptionField = CustomTextField(
      label="Descripción (Opcional)",
      field="others",
      submitFunction=None,
      expand=True,
    )
    
    self.stockField = CustomNumberField(
      label="Stock inicial",
      expand=True,
    )
    
    self.minimStockField = CustomNumberField(
      label="Stock mínimo",
      expand=True,
    )
    
    self.helpText = CustomTooltip(
      message="Se emitirá una alerta cuando el stock del producto sea menor que el mínimo establecido.",
      content=ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
          ft.Icon(
            name=ft.icons.HELP_ROUNDED,
            color=constants.BLACK,
          ),
          ft.Text(
            value="¿Cuál es la función del stock mínimo?",
            size=18,
            color=constants.BLACK,
          )
        ]
      )
    )
    
    self.costField = CustomTextField(
      label="Costo del producto",
      field="number",
      expand=True,
      submitFunction=None,
      suffix_text="$",
      on_changeFunction=self.calculateFinalPrice
    )
    
    self.ivaField = CustomTextField(
      label="IVA",
      field="number",
      expand=True,
      suffix_text="%",
      submitFunction=None,
      on_changeFunction=self.calculateFinalPrice
    )
    
    self.gainField = CustomTextField(
      label="Ganancia esperada",
      field="number",
      expand=True,
      suffix_text="%",
      submitFunction=None,
      on_changeFunction=self.calculateFinalPrice
    )
    
    self.image = CustomImageSelectionContainer(
      page=self.page, 
    )
    
    self.categoryField = CustomDropdown(
      label="Categoría",
      expand=True,
      options=self.getCategoriesName(),
    )
    
    self.numberPrice = ft.Text(
      value="0$",
      size=18,
      color=constants.BLACK,
      weight=ft.FontWeight.W_700,
    )
    self.finalPrice = ft.Container(
      expand=True,
      padding=ft.padding.symmetric(horizontal=10, vertical=20),
      border_radius=ft.border_radius.all(10),
      alignment=ft.alignment.center_left,
      content=ft.Row(
        alignment=ft.MainAxisAlignment.START,
        controls=[
          ft.Text(
            value="Precio Final:",
            size=18,
            color=constants.BLACK,
          ),
          self.numberPrice,
        ]
      )
    )
    
    self.finishButton = CustomFilledButton(
      text="Crear producto",
      clickFunction=self.submitForm,
    )
    
    self.content = ft.Column(
      scroll=ft.ScrollMode.AUTO,
      alignment=ft.MainAxisAlignment.CENTER,
      height=800,
      width=600,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      spacing=20,
      controls=[
        ft.Column(
          alignment=ft.MainAxisAlignment.CENTER,
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            self.title,
            self.image,
          ]
        ),
        ft.Divider(color=constants.WHITE_GRAY),
        ft.Column(
          controls=[
            ft.Row(
              controls=[
                ft.Icon(
                  name=ft.icons.CATEGORY_ROUNDED,
                  color=constants.BLACK,  
                ),
                ft.Text(
                  value="Selección de categoría",
                  size=18,
                  color=constants.BLACK,
                ),
              ]
            ),
            ft.Row(
              controls=[
                self.categoryField,  
              ]
            ),
          ]
        ),
        ft.Divider(color=constants.WHITE_GRAY),
        ft.Column(
          controls=[
            ft.Row(
              controls=[
                ft.Icon(
                  name=ft.icons.INFO_OUTLINE_ROUNDED,
                  color=constants.BLACK,
                ),
                ft.Text(
                  value="Información del producto",
                  size=18,
                  color=constants.BLACK,
                )
              ]
            ),
            ft.Row(
              controls=[
                self.nameField,
                self.descriptionField,  
              ]
            ),
          ]
        ),
        ft.Divider(color=constants.WHITE_GRAY),
        ft.Column(
          controls=[
            ft.Row(
              controls=[
                ft.Icon(
                  name=ft.icons.NUMBERS_ROUNDED,
                  color=constants.BLACK,
                ),
                ft.Text(
                  value="Configuración de stock",
                  color=constants.BLACK,
                  size=18,
                )
              ]
            ),
            ft.Row(
              controls=[
                self.stockField,
                self.minimStockField,
              ]
            ),
          ]
        ),
        ft.Divider(color=constants.WHITE_GRAY),
        ft.Column(
          controls=[
            ft.Row(
              controls=[
                ft.Icon(
                  name=ft.icons.ATTACH_MONEY_ROUNDED,
                  color=constants.BLACK,
                ),
                ft.Text(
                  value="Costos",
                  color=constants.BLACK,
                  size=18,
                )
              ]
            ),
            ft.Row(
              controls=[
                self.costField,
                self.ivaField,
              ]
            ),
            ft.Row(
              controls=[
                self.gainField,
                self.finalPrice,
              ]
            ),
          ]
        ),
        self.finishButton,
      ]
    )
    super().__init__(operationContent=self.content)
  
  def getCategoriesName(self):
    try:
      with getDB() as db:
        categories = getCategories(db)
        categoriesNames = []
        
        for category in categories:
          categoriesNames.append(ft.dropdown.Option(category.name))
        return categoriesNames
    except Exception as err:
      raise
  
  def calculateFinalPrice(self):
    try:
      if not self.costField.value == "" and not self.ivaField.value == "" and not self.gainField.value == "":
        price = calculatePrice(
          cost=float(self.costField.value),
          iva=float(self.ivaField.value),
          gain=float(self.gainField.value),
        )
        if price:
          self.numberPrice.value = f"{price}$"
          self.numberPrice.update()
        
    except Exception as err:
      print(err)
      pass
  
  def submitForm(self, e):
    try:
      if evaluateForm(numbers=[self.costField, self.gainField], others=[self.nameField, self.categoryField]):
        if not int(self.minimStockField.field.value) > 0:
          self.actionFailed(message="El stock mínimo no puede ser 0")
          time.sleep(1.5)
          self.restartContainer()
        else:
          self.createProduct()
    except Exception as err:
      raise
  
  def createProduct(self):
    try:
      with getDB() as db:
        name = self.nameField.value.strip()
        category = getCategoryByName(db, self.categoryField.value.strip())
        description = self.descriptionField.value.strip()
        stock = int(self.stockField.fieldValue)
        minimStock = int(self.minimStockField.fieldValue)
        cost = float(self.costField.value)
        iva = float(self.ivaField.value)
        gain = float(self.gainField.value)
        
        print(f"Stock: {stock} - {type(stock)}, MinimStock: {minimStock} - {type(minimStock)}")
        
        product = createProduct(
          db=db,
          name=name,
          description=description,
          stock=stock,
          minStock=minimStock,
          cost=cost,
          iva=iva,
          gain=gain,
          idCategory=category.idCategory,
          imgPath=None
        )
        
        print(product.stock, product.minStock)
        
        if not self.image.selectedImagePath == None:
          imageManager = ImageManager()
          destinationPath = imageManager.storageImage(product.idCategory, self.image.selectedImagePath)
          product.imgPath = destinationPath
          db.commit()
        
        if product:
          print(f"Producto {product.idProduct} creado: {product.name}. Description: {product.description}. imgPath {product.imgPath}")
          
          self.actionSuccess("Producto creado")
          time.sleep(1.5)
          self.mainContainer.resetCurrentView()
    except DataAlreadyExists as err:
      self.actionFailed(err)
      time.sleep(1.5)
      self.restartContainer()
    except Exception as err:
      raise
  
class UpdateStockForm(ft.Stack):
  def __init__(self, idProduct, mainContainer, page, productInfoControl):
    super().__init__()
    self.idProduct = idProduct
    self.page = page
    self.mainContainer = mainContainer
    self.productInfoControl = productInfoControl
    
    self.expand = True
    
    with getDB() as db:
      product = getProductById(db, idProduct)
      
      self.titleText = ft.Text(
        value=f"Actualización del inventario de:\n\"{product.name}\"",
        size=32,
        color=constants.BLACK,
        weight=ft.FontWeight.W_700,
        text_align=ft.TextAlign.CENTER,
      )
      
      self.stockText = ft.Text(
        value=f"Stock actual: {product.stock}",
        size=18,
        color=constants.BLACK,
        weight=ft.FontWeight.W_700,
      )
      
      self.minStockText = ft.Text(
        value=f"Stock mínimo establecido: {product.minStock}",
        size=18,
        color=constants.BLACK,
        weight=ft.FontWeight.W_700,
      )
      
      self.stockField = CustomNumberField(
        label="Agregar al inventario",
        expand=True,
      )
      
      self.minStockField = CustomNumberField(
        label="Nuevo stock mínimo",
        expand=True,
        value=product.minStock,
      )
      
      self.finishButton = CustomFilledButton(
        text="Actualizar",
        clickFunction=self.submitForm,
      )
    
    self.operationContent = CustomOperationContainer(
      operationContent=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        width=800,
        height=200,
        controls=[
          ft.Row(
            expand=True,
            controls=[
              self.stockField,
              self.minStockField,
            ]
          ),
          self.finishButton,
        ]
      ),
    )
    
    self.controls = [
      ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[self.titleText]  
          ),
          self.operationContent,
        ]
      ),
      ft.Container(
        left=10,
        top=10,
        content=CustomReturnButton(
          function=lambda e: self.productInfoControl.returnToInfo(),
        )
      )
    ]
      
  def submitForm(self, e):
    try:
      if self.stockField.field.value == "0" or self.minStockField.field.value == "0":
        self.operationContent.actionFailed("Ningún campo puede ser igual a 0")
        time.sleep(1.5)
        self.operationContent.restartContainer()
      elif getCurrentUser() == None:
        self.operationContent.actionFailed("No se encontró el usuario.")
        time.sleep(1.5)
        self.operationContent.restartContainer()
      else:
        with getDB() as db:
          product = getProductById(db, self.idProduct)
          updatedProduct, register = updateProductStock(
            db=db, 
            product=product, 
            quantityAdded=int(self.stockField.field.value)
          )
          updatedProduct.minStock = int(self.minStockField.field.value)
          db.commit()
          db.refresh(updatedProduct)
          
          print(updatedProduct.stock, "/", updatedProduct.minStock, register.user.username, register.product.name,)
          if updatedProduct:
            self.operationContent.actionSuccess("Cambios guardados")
            time.sleep(1.5)
            self.productInfoControl.updateInfoControls(stock=True)
            self.productInfoControl.returnToInfo()
          else:
            self.operationContent.actionFailed("No se pudo actualizar el producto")
            time.sleep(1.5)
            self.operationContent.restartContainer()
    except Exception as err:
      print(err)
  
class UpdateInfoForm(ft.Stack):
  def __init__(self, page, idProduct, mainContainer, productInfoControl):
    super().__init__()
    self.page = page
    self.idProduct = idProduct
    self.mainContainer = mainContainer
    self.productInfoControl = productInfoControl
    
    self.expand = True
    
    with getDB() as db:
      product = getProductById(db, self.idProduct)
      
      self.title = ft.Text(
        value=f"Actualizar información de:\n\"{product.name}\"",
        size=32,
        color=constants.BLACK,
        weight=ft.FontWeight.W_700,
        text_align=ft.TextAlign.CENTER,
      )
      
      self.nameField = CustomTextField(
        label="Nombre",
        value=product.name,
        expand=True,
        submitFunction=self.submitForm,
        field="others"
      )
      
      self.descriptionField = CustomTextField(
        label="Descripción (opcional)",
        value=product.description,
        expand=True,
        submitFunction=self.submitForm,
        field="others"
      )
      
      self.categoryField = CustomDropdown(
        label="Categoría",
        expand=True,
        value=product.category.name,
        options=self.getCategoriesName(),
      )
      
      imageManager = ImageManager()
      self.image = CustomImageSelectionContainer(
        page=self.page,
        src=imageManager.getImagePath(product.imgPath),
      )
    
    self.finishButton = CustomFilledButton(
      text="Actualizar",
      clickFunction=self.submitForm
    )
    
    self.operationContent = CustomOperationContainer(
      operationContent=ft.Column(
        height=400,
        width=400,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[
          ft.Column(
            controls=[
              ft.Row(
                controls=[
                  ft.Icon(
                    name=ft.icons.CATEGORY_ROUNDED,
                    color=constants.BLACK,  
                  ),
                  ft.Text(
                    value="Selección de categoría",
                    size=18,
                    color=constants.BLACK,
                  ),
                ]
              ),
              ft.Row(
                controls=[
                  self.categoryField,  
                ]
              ),
            ]
          ),
          ft.Divider(color=constants.WHITE_GRAY),
          ft.Column(
            controls=[
              ft.Row(
                controls=[
                  ft.Icon(
                    name=ft.icons.INFO_OUTLINE_ROUNDED,
                    color=constants.BLACK,
                  ),
                  ft.Text(
                    value="Información del producto",
                    size=18,
                    color=constants.BLACK,
                  )
                ]
              ),
              ft.Row(
                controls=[
                  self.nameField,  
                ]
              ),
              ft.Row(
                controls=[
                  self.descriptionField,
                ]
              ),
            ]
          ),
          self.finishButton,
        ]
      )
    )
    
    self.controls=[
      ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
              self.title,
              self.image,
            ]
          ),
          ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            controls=[self.operationContent]
          ),
        ]
      ),
      ft.Container(
        left=10,
        top=10,
        content=CustomReturnButton(
          function=lambda e: self.productInfoControl.returnToInfo(),
        )
      )
    ]
  
  def getCategoriesName(self):
    try:
      with getDB() as db:
        categories = getCategories(db)
        categoriesNames = []
        
        for category in categories:
          categoriesNames.append(ft.dropdown.Option(category.name))
        return categoriesNames
    except Exception as err:
      raise
  
  def submitForm(self, e):
    try:
      if evaluateForm(others=[self.nameField, self.categoryField]):
        with getDB() as db:
          product = getProductById(db, self.idProduct)
          category = getCategoryByName(db, self.categoryField.value.strip())
          imageManager = ImageManager()
          print(type(self.descriptionField.value.strip()), "->", self.descriptionField.value.strip())
          
          updatedProduct = updateProductInfo(
            db=db,
            product=product,
            name=self.nameField.value.strip(),
            description=self.descriptionField.value.strip(),
            idCategory=category.idCategory,
          )
          
          if updatedProduct:
            product.imgPath = imageManager.updateImage(
              idData=product.idProduct, 
              oldImage=product.imgPath, 
              newImage=self.image.selectedImagePath,
            )
            db.commit()
            db.refresh(product)
            
            self.operationContent.actionSuccess("Producto actualizado")
            time.sleep(1.5)
            self.productInfoControl.updateInfoControls(info=True)
          else:
            self.operationContent.actionFailed("Algo salió mal")
    except Exception as err:
      print(err)
    
class UpdatePriceForm(ft.Stack):
  def __init__(self, page, idProduct, mainContainer, productInfoControl):
    super().__init__()
    self.page = page
    self.idProduct = idProduct
    self.mainContainer = mainContainer
    self.productInfoControl = productInfoControl
    
    self.expand = True
    
    with getDB() as db:
      product = getProductById(db, self.idProduct)
      
      self.title = ft.Text(
        value=f"Actualizar precios de:\n\"{product.name}\"",
        size=32,
        color=constants.BLACK,
        weight=ft.FontWeight.W_700,
        text_align=ft.TextAlign.CENTER,
      )
      
      self.costField = CustomTextField(
        label="Costo del producto",
        field="number",
        expand=True,
        value=round(product.cost, 2),
        submitFunction=None,
        suffix_text="$",
        on_changeFunction=self.calculateFinalPrice
      )
      
      self.ivaField = CustomTextField(
        label="IVA",
        field="number",
        value=round(product.iva, 2),
        expand=True,
        suffix_text="%",
        submitFunction=None,
        on_changeFunction=self.calculateFinalPrice
      )
      
      self.gainField = CustomTextField(
        label="Ganancia esperada",
        field="number",
        expand=True,
        value=round(product.gain, 2),
        suffix_text="%",
        submitFunction=None,
        on_changeFunction=self.calculateFinalPrice
      )
      
      self.numberPrice = ft.Text(
        value=f"{round(calculatePrice(cost=product.cost, iva=product.iva, gain=product.iva), 2)}$",
        size=18,
        color=constants.BLACK,
        weight=ft.FontWeight.W_700,
      )
      self.finalPrice = ft.Container(
        expand=True,
        padding=ft.padding.symmetric(horizontal=10, vertical=20),
        border_radius=ft.border_radius.all(10),
        alignment=ft.alignment.center_left,
        content=ft.Row(
          alignment=ft.MainAxisAlignment.START,
          controls=[
            ft.Text(
              value="Precio Final:",
              size=18,
              color=constants.BLACK,
            ),
            self.numberPrice,
          ]
        )
      )
      
    self.finishButton = CustomFilledButton(
      text="Actualizar",
      clickFunction=self.submitForm,
    )
    
    self.operationContent = CustomOperationContainer(
      operationContent=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        height=400,
        width=800,
        spacing=15,
        controls=[
          ft.Row(
            width=800,
            controls=[
              self.costField,
              self.ivaField,
            ]
          ),
          ft.Row(
            width=800,
            controls=[
              self.gainField,
              self.finalPrice
            ]
          ),
          self.finishButton,
        ]
      )
    )
      
    self.controls=[
      ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        controls=[
          ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            height=100,
            controls=[
              self.title,
            ]
          ),
          ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            controls=[
              self.operationContent
            ]
          )
        ]
      ),
      ft.Container(
        left=10,
        top=10,
        content=CustomReturnButton(
          function=lambda e: self.productInfoControl.returnToInfo(),
        )
      )
    ]
  
  def calculateFinalPrice(self):
    try:
      if not self.costField.value == "" and not self.ivaField.value == "" and not self.gainField.value == "":
        price = calculatePrice(
          cost=float(self.costField.value),
          iva=float(self.ivaField.value),
          gain=float(self.gainField.value),
        )
        if price:
          self.numberPrice.value = f"{price}$"
          self.numberPrice.update()
        
    except Exception as err:
      print(err)
  
  def submitForm(self, e):
    try:
      if evaluateForm(numbers=[self.costField, self.gainField]):
        with getDB() as db:
          product = getProductById(db, self.idProduct)
          
          product = updateProductPrices(
            db=db,
            product=product,
            cost=float(self.costField.value),
            iva=float(self.ivaField.value),
            gain=float(self.gainField.value)
          )
          
          if product:
            self.operationContent.actionSuccess("Producto actualizado")
            time.sleep(1.5)
            self.productInfoControl.updateInfoControls(prices=True)
          else:
            self.operationContent.actionFailed("Algo salió mal")
            time.sleep(1.5)
            self.productInfoControl.returnToInfo()
    except Exception as err:
      print(err)