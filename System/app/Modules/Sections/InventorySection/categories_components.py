import flet as ft 
import constants
from Modules.customControls import CustomUserIcon, CustomOperationContainer, CustomTextField, CustomAnimatedContainer, CustomNavigationOptions, CustomFilledButton, CustomDropdown, CustomDeleteButton, CustomAlertDialog, CustomImageContainer, CustomEditButton, CustomImageSelectionContainer
from config import getDB
import time
from DataBase.crud.category import getCategoryById, updateCategory, removeCategory
from utils.imageManager import ImageManager
from exceptions import DataAlreadyExists
from validation import evaluateForm

class CategoryContainer(ft.Container):
  def __init__(self, idCategory, name, description, infoContainer, mainContainer, imgPath=None):
    # super().__init__(col={"xl": 12, "xxl": 6})
    super().__init__()
    self.name = name
    self.idCategory = idCategory
    self.description = description
    self.imgPath = imgPath
    self.infoContainer = infoContainer
    self.mainContainer = mainContainer
    
    self.shadow = ft.BoxShadow(
      spread_radius=1,
      blur_radius=1,
      color=constants.WHITE_GRAY,
    )
    self.bgcolor = constants.WHITE
    self.border_radius = ft.border_radius.all(30)
    self.ink = True
    self.ink_color = constants.WHITE_GRAY
    self.on_click = self.showCategoryInfo
    
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
        size=20,
        weight=ft.FontWeight.W_600,
        overflow=ft.TextOverflow.ELLIPSIS,
      ),
    )
    
    self.descriptionText = CustomAnimatedContainer(
      actualContent=ft.Text(
        value=self.description,
        color=constants.BLACK,
        size=20,
        overflow=ft.TextOverflow.ELLIPSIS,
      ),
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
            self.descriptionText
          ]
        )
      ]
    )
    
  def showCategoryInfo(self, e):
    newContent = CategoryInfo(
      imgPath=self.imgPath,
      name=self.name,
      idCategory=self.idCategory,
      description=self.description,
      infoContainer=self.infoContainer,
      categoryContainer=self,
      mainContainer=self.mainContainer,
      page=self.page,
    )
    
    if not self.infoContainer.height == 400:
      self.infoContainer.changeStyle(height=400, width=700, shadow=ft.BoxShadow(
        blur_radius=5,
        spread_radius=1,
        color=constants.BLACK_INK,
      ))
    self.infoContainer.setNewContent(newContent)

class CategoryInfo(ft.Stack):
  def __init__(self, page, idCategory, imgPath, name, description, infoContainer, categoryContainer, mainContainer):
    super().__init__()
    self.page = page
    self.imgPath = imgPath
    self.name = name
    self.idCategory = idCategory
    self.description = description
    self.infoContainer = infoContainer
    self.categoryContainer = categoryContainer
    self.mainContainer = mainContainer
    
    self.expand = True
    
    self.imageContainer = CustomImageContainer(
      src=self.imgPath,
      border_radius=30,
    )
    
    self.nameText = ft.Text(
      value=self.name,
      size=24,
      color=constants.BLACK,
      weight=ft.FontWeight.W_700,
    )
    
    self.descriptionText = ft.Text(
      value=self.description,
      size=20,
      color=constants.BLACK,
      max_lines=2,
      overflow=ft.TextOverflow.ELLIPSIS,
    )
    
    self.editButton = CustomEditButton(
      function=self.editCategory
    )
    
    self.deleteButton = CustomDeleteButton(
      function=self.deleteCategory,
      page=self.page,
    )
    
    self.controls = [
      ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=5,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        width=600,
        controls=[
          self.imageContainer,
          self.nameText,
          self.descriptionText
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
  
  def deleteCategory(self):
    try:
      with getDB() as db:
        category = getCategoryById(db, self.idCategory)
        
        if removeCategory(db, category):
          self.mainContainer.resetCurrentView()
    except Exception as err:
      print(err)
      
  def editCategory(self, e):
    try:
      self.mainContainer.editItemForm(
        CategoryEdit(
          page=self.page,
          idCategory=self.idCategory,
          name=self.name,
          description=self.description,
          imgPath=self.imgPath,
          mainContainer=self.mainContainer,
        )
      )
    except Exception as err:
      print(err)
      
class CategoryEdit(ft.Stack):
  def __init__(self, page, idCategory, name, description, imgPath, mainContainer):
    super().__init__()
    self.page = page
    self.idCategory = idCategory
    self.name = name
    self.description = description
    self.imgPath = imgPath
    self.mainContainer = mainContainer
    
    self.titleText = ft.Row(
      alignment=ft.MainAxisAlignment.CENTER,
      controls=[
        ft.Text(
          value=self.name,
          size=32,
          weight=ft.FontWeight.W_700,
          text_align=ft.TextAlign.CENTER,
          color=constants.BLACK,
        )
      ]
    )
    
    self.imageEditContainer = CustomImageSelectionContainer(
      page=self.page,
      src=self.imgPath,
    )
    
    self.nameField = CustomTextField(
      label="Nombre de la categoría",
      field="others",
      expand=True,
      submitFunction=self.submitForm,
      value=self.name
    )
    
    self.descriptionField = CustomTextField(
      label="Descripción (opcional)",
      field="others",
      expand=True,
      submitFunction=self.submitForm,
      value=self.description,
    )
    
    self.finishButton = ft.Row(
      alignment=ft.MainAxisAlignment.CENTER,
      controls=[
        CustomFilledButton(
          text="Guardar cambios",
          clickFunction=self.submitForm,
        )
      ]
    )
    
    self.operationContainer = CustomOperationContainer(
      operationContent=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        height=400,
        width=700,
        controls=[
          ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            # expand=True,
            controls=[
              self.imageEditContainer,
            ]
          ),
          ft.Row(
            # expand=True,
            controls=[
              self.nameField,
              self.descriptionField
            ]
          ),
          self.finishButton
        ]
      )
    )
    
    self.controls = [
      ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[
          ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[self.titleText]
          ),
          ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[self.operationContainer,]
          ),
        ]
      ),
    ]
  
  def submitForm(self, e):
    try:
      with getDB() as db:
        if evaluateForm(others=[self.nameField]):
          currentCategory = getCategoryById(db, self.idCategory)
          
          updatedCategory = updateCategory(
            db=db, 
            category=currentCategory, 
            name=self.nameField.value,
            description=self.descriptionField.value,
            imgPath=self.imageEditContainer.selectedImagePath,
          )
          
          if updatedCategory:
            self.operationContainer.actionSuccess("Categoría Actualizada")
            time.sleep(1.5)
            self.mainContainer.resetCurrentView()
          else:
            self.operationContainer.actionFailed("Algo salió mal")
            time.sleep(1.5)
            self.operationContainer.resetContainer()
    except DataAlreadyExists as err:
      self.operationContainer.actionFailed(err)
      time.sleep(1.5)
      self.operationContainer.restartContainer()
    except Exception as err:
      print(err)