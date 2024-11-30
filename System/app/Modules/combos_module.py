import flet as ft
from Modules.customControls import CustomPrincipalContainer, CustomSimpleContainer, CustomOperationContainer, CustomAnimatedContainer, CustomOutlinedButton, CustomImageSelectionContainer, CustomNumberField, CustomTooltip, CustomFilledButton, CustomTextField, CustomAutoComplete, CustomDropdown, CustomAlertDialog, CustomReturnButton, CustomItemsSelector
import constants
from config import getDB
from validation import evaluateForm
from DataBase.crud.product import createProduct, getProductByName, getProductById, calculatePrice
from DataBase.crud.combo import createCombo, getComboById, getComboByName, getCombos, updateComboInfo, updateComboDetails, calculateComboCost, calculateComboGain
from DataBase.crud.product_combo import registerOperation
import threading
from utils.imageManager import ImageManager
from exceptions import DataAlreadyExists, InvalidData
from utils.sessionManager import getCurrentUser

class ComboForm(CustomOperationContainer):
  def __init__(self, page, mainContainer):
    self.page = page 
    self.mainContainer = mainContainer
    
    self.title = ft.Row(
      alignment=ft.MainAxisAlignment.CENTER,
      controls=[
        ft.Text(
          value="Nuevo Combo",
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
    
    self.image = CustomImageSelectionContainer(
      page=self.page,
      src=None,
    )
    
    self.productsText = ft.Row(
      controls=[
        ft.Icon(
          name=ft.icons.COFFEE_ROUNDED,
          color=constants.BLACK,
        ),
        ft.Text(
          value="Selección de productos",
          size=20,
          color=constants.BLACK,
        )
      ]
    )
    
    self.productsSelector = CustomItemsSelector(
      page=self.page,
    )
    
    self.priceField = CustomTextField(
      label="Precio",
      field="number",
      expand=True,
      suffix_text="$",
      submitFunction=None,
      on_changeFunction=None,
    )
    
    self.finishButton = CustomFilledButton(
      text="Crear Combo",
      clickFunction=self.submitForm,
    )
    
    self.content = ft.Column(
      scroll=ft.ScrollMode.AUTO,
      alignment=ft.MainAxisAlignment.CENTER,
      expand=True,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      spacing=20,
      controls=[
        ft.Column(
          alignment=ft.MainAxisAlignment.CENTER,
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            self.title,
            self.image
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
                  value="Información del combo",
                  size=20,
                  color=constants.BLACK,
                )
              ]
            ),
            ft.Row(
              controls=[self.nameField]
            )
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
                  value="Precio Final",
                  size=20,
                  color=constants.BLACK,
                )
              ]
            ),
            ft.Row(
              controls=[self.priceField]
            )
          ]
        ),
        ft.Divider(color=constants.WHITE_GRAY),
        ft.Column(
          controls=[
            self.productsText,
            ft.Container(
              height=500, 
              width=800,
              alignment=ft.alignment.center,
              content=self.productsSelector,
            ),
          ]
        ),
        self.finishButton,
      ]
    )
    
    super().__init__(operationContent=self.content)
    
  def submitForm(self, e):
    try:
      if evaluateForm(others=[self.nameField], numbers=[self.priceField]) and self.productsSelector.validateAllItemFields():
        with getDB() as db:
          imageManager = ImageManager()
          name = self.nameField.value.strip()
          
          imgPath = self.image.selectedImagePath
          
          products, combos = self.productsSelector.getItemsWithQuantity()
          price = self.productsSelector.price
  
          combo = createCombo(
            db=db,
            name=self.nameField.value.strip(),
            cost=self.productsSelector.price,
            price=float(self.priceField.value.strip()),
            imgPath=self.image.selectedImagePath
          )
          
          if combo:
            for product in products:
              register = registerOperation(
                db=db,
                idProduct=product["id"],
                idCombo=combo.idCombo,
                productQuantity=product["quantity"]
              )
              
              print(f"{register.combo.name} - {register.product.name}")
              self.actionSuccess("Combo creado.")
              threading.Timer(1.5, self.mainContainer.resetCurrentView).start()
    except DataAlreadyExists as err:
      self.actionFailed(err)
      threading.Timer(1.5, self.restartContainer).start()
    except InvalidData as err:
      self.actionFailed(err)
      threading.Timer(1.5, self.restartContainer).start()
    except:
      raise
    
class UpdateInfoForm(ft.Stack):
  def __init__(self, page, idCombo, mainContainer, comboInfoControl):
    super().__init__()
    self.page = page
    self.idCombo = idCombo
    self.mainContainer = mainContainer
    self.comboInfoControl = comboInfoControl
    
    self.expand = True
    
    with getDB() as db:
      combo = getComboById(db, self.idCombo)
      
      self.title = ft.Text(
        value=f"Actualizar información de:\n\"{combo.name}\"",
        size=32,
        color=constants.BLACK,
        weight=ft.FontWeight.W_700,
        text_align=ft.TextAlign.CENTER,
      )
      
      self.nameField = CustomTextField(
        label="Nombre",
        value=combo.name,
        expand=False,
        submitFunction=None,
        field="others",
      )
      
      self.priceField = CustomTextField(
        label="Precio",
        value=round(combo.price, 2),
        expand=False,
        submitFunction=None,
        field="number",
        suffix_text="$"
      )
      
      cost = 0
      for register in combo.products:
        cost += register.product.cost * register.productQuantity
        
      self.costText = ft.Text(
        value=f"Costo de los productos: {round(cost, 2)}$",
        size=20,
        color=constants.BLACK,
        text_align=ft.TextAlign.CENTER,
      )
      
      imageManager = ImageManager()
      self.image = CustomImageSelectionContainer(
        page=self.page,
        src=imageManager.getImagePath(combo.imgPath),
      )
      
    self.finishButton = CustomFilledButton(
      text="Actualizar",
      clickFunction=self.submitForm,
    )
    
    self.operationContent = CustomOperationContainer(
      operationContent=ft.Column(
        height=400,
        width=400,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          ft.Row(
            controls=[
              ft.Row(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                  self.image,
                ]
              ),
              ft.Column(
                expand=True,
                controls=[
                  self.nameField,
                  self.priceField
                ]
              )
            ]
          ),
          self.costText,
          self.finishButton,
        ]
      )
    )
    
    self.controls=[
      ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
              ft.Row(
                  alignment=ft.MainAxisAlignment.CENTER,
                  vertical_alignment=ft.CrossAxisAlignment.CENTER,
                  controls=[self.title]
              ),
              ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[self.operationContent,]
              )
            ]
          )
        ]
      ),
      ft.Container(
        left=10,
        top=10,
        content=CustomReturnButton(
          function=lambda e: self.comboInfoControl.returnToInfo(),
        )
      )
    ]
  
  def submitForm(self, e):
    try:
      if evaluateForm(others=[self.nameField], numbers=[self.priceField]):
        with getDB() as db:
          combo = getComboById(db, self.idCombo)
          
          updatedCombo = updateComboInfo(
            db=db,
            combo=combo,
            name=self.nameField.value.strip(),
            price=float(self.priceField.value),
            imgPath=self.image.selectedImagePath,
          )
          
          if updatedCombo:
            self.operationContent.actionSuccess("Combo actualizado")
            threading.Timer(1.5, self.comboInfoControl.updateInfoControls).start()
    except DataAlreadyExists as err:
      self.operationContent.actionFailed(err)
      threading.Timer(1.5, self.operationContent.restartContainer).start()
    except Exception as err:
      raise