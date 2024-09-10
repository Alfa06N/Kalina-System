import flet as ft
import constants
from Modules.customControls import CustomUserIcon, CustomOperationContainer, CustomTextField, CustomAnimatedContainer, CustomNavigationOptions, CustomFilledButton, CustomDropdown, CustomDeleteButton, CustomAlertDialog, CustomImageSelectionContainer, CustomImageContainer
import time
from exceptions import InvalidData, DataAlreadyExists
from config import getDB
from validation import evaluateForm
from DataBase.crud.category import createCategory, getCategoryByName
from utils.imageManager import ImageManager

class CategoryForm(CustomOperationContainer):
  def __init__(self, page, mainContainer):
    self.page = page 
    self.mainContainer = mainContainer
    
    self.title = ft.Row(
      alignment=ft.MainAxisAlignment.CENTER,
      controls=[
        ft.Text(
          value="Nueva Categoría",
          size=42,
          color=constants.BLACK,
          weight=ft.FontWeight.BOLD,
          text_align=ft.TextAlign.CENTER,
        )
      ]
    )
    
    self.nameField = CustomTextField(
      label="Nombre",
      field="others",
      submitFunction=self.submitForm,
      expand=True,
    )
    
    self.descriptionField = CustomTextField(
      label="Descripción (Opcional)",
      field="others",
      submitFunction=self.submitForm,
      expand=True,
    )
    
    self.image = CustomImageSelectionContainer(
      page=self.page, 
    )
    
    self.button = CustomFilledButton(
      text="Crear",
      clickFunction=self.submitForm,
    )
    
    self.columnContent = ft.Column(
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      height=600,
      width=700,
      controls=[
        ft.Column(
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          alignment=ft.MainAxisAlignment.CENTER,
          spacing=20,
          controls=[
            self.title,
            self.image,
          ]
        ),
        ft.Column(
          expand=True,
          controls=[
            ft.Row(
              expand=True,
              vertical_alignment=ft.CrossAxisAlignment.CENTER,
              controls=[
                self.nameField,
                self.descriptionField,
              ]
            ),
            ft.Row(
              expand=True,
              vertical_alignment=ft.CrossAxisAlignment.CENTER,
              alignment=ft.MainAxisAlignment.CENTER,
              controls=[
                self.button
              ]
            )
          ]
        )
      ]
    )
    super().__init__(operationContent=self.columnContent)
  
  def submitForm(self, e):
    try:
      if evaluateForm(others=[self.nameField]):
        
        with getDB() as db:
          category = createCategory(
            db=db,
            name=self.nameField.value,
            description=self.descriptionField.value,
            imgPath=None,
          )
          
          if not self.image.selectedImagePath == None:
            imageManager = ImageManager()
            destinationPath = imageManager.storageImage(category.idCategory, self.image.selectedImagePath)
            category.imgPath = destinationPath
            db.commit()
          
          print(f"{category.idCategory} {category.name}: {category.description} ({category.imgPath})")

        self.actionSuccess("Categoría creada")
        time.sleep(1.5)
        self.mainContainer.resetInfoContainer()
        self.mainContainer.fillItemsContainer()
    except Exception as err:
      print(err)
      raise